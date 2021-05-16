import BaseHTTPServer
import SocketServer
import json
import random
import re
import uuid
from multiprocessing import Queue, Process

from django.test import TestCase

from mail.models import Message
from users.models import User
from common import AnyTelegram, TelegramRenderer, TelegramSender
from test_data import get_mock_update


class TelegramApiServerMock(Process):
    LISTEN_ADDR = '127.0.0.1'
    LISTEN_PORT = 29668 + random.randint(0, 200)

    class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
        def api_get_me(self):
            self.server.trapped_requests.put(('getMe', dict()))
            user = {
                'id': '1234567890',
                'is_bot': True,
                'first_name': 'bot_first_name',
                'last_name': 'bot_last_name',
                'username': 'bot',
                'language_code': 'ru',
                'can_join_groups': False,
                'can_read_all_group_messages': False,
                'supports_inline_queries': False
            }
            resp = {
                'ok': True,
                'result': user,
            }
            resp_text = json.dumps(resp)
            self.send_response(200)
            self.send_header('content-length', len(resp_text))
            self.end_headers()
            self.wfile.write(resp_text)

        def api_send_message(self):
            request = json.load(self.rfile)
            self.server.trapped_requests.put(('sendMessage', request))
            message = {
                'message_id': int(random.random()),
                'date': 0,
                'chat': {
                    'id': request['chat_id'],
                    'type': 'private',
                }
            }
            resp = {
                'ok': True,
                'result': message,
            }
            resp_text = json.dumps(resp)
            self.send_response(200)
            self.send_header('content-length', len(resp_text))
            self.end_headers()
            self.wfile.write(resp_text)

        @classmethod
        def strip_token(cls, path):
            return re.match(r'/.+/(.+)$', path).group(1)

        def do_GET(self):  # NOQA
            req = self.strip_token(self.path)
            if req.startswith('getMe'):
                return self.api_get_me()
            else:
                self.send_response(501)
                self.end_headers()

        def do_POST(self):  # NOQA
            req = self.strip_token(self.path)
            if req.startswith('sendMessage'):
                return self.api_send_message()
            else:
                self.send_response(501)
                self.end_headers()

    def __init__(self):
        super(TelegramApiServerMock, self).__init__(target=self.main)
        self.daemon = True
        self.server = None
        self.trapped_requests = Queue()

    def get_base_url(self):
        return 'http://{}:{}/'.format(self.LISTEN_ADDR, self.LISTEN_PORT)

    def main(self):
        server_address = (self.LISTEN_ADDR, self.LISTEN_PORT)
        self.server = SocketServer.TCPServer(server_address, self.Handler)
        self.server.allow_reuse_address = True
        self.server.submit_error = False
        self.server.trapped_requests = self.trapped_requests
        self.server.serve_forever()


class AnyTelegramTests(TestCase):
    api_server = None

    @classmethod
    def setUpClass(cls):
        super(AnyTelegramTests, cls).setUpClass()
        cls.api_server = TelegramApiServerMock()
        cls.api_server.start()

    def setUp(self):
        super(AnyTelegramTests, self).setUpClass()

        self.api_client = AnyTelegram(base_url=self.api_server.get_base_url())

        self.first_student = User.objects.create_user(
            username='first_student', password='password')
        self.second_student = User.objects.create_user(
            username='second_student', password='password')

    def test_non_null_link_secret(self):
        self.assertIsNotNone(self.first_student.profile.telegram_link_secret)
        self.assertIsNotNone(self.second_student.profile.telegram_link_secret)

    def test_unique_link_secret(self):
        self.assertNotEqual(
            self.first_student.profile.telegram_link_secret,
            self.second_student.profile.telegram_link_secret
        )

    def test_reply_start(self):
        update = get_mock_update('bcskda_start')
        self.api_client.process_update(json.dumps(update))
        expected_trapped = [
            ('getMe', dict()),
            ('sendMessage', {
                u'chat_id': u'463992304',
                u'disable_notification': u'False',
                u'text': u'Visit your profile to get the secret, then call /link <secret>'
            })
        ]
        self.assertTrappedCalls(expected_trapped)

    def test_link_valid(self):
        self.first_student.profile.telegram_link_secret = uuid.UUID('53cd4396-8b96-45a7-a123-11f1107b56c7')
        self.first_student.profile.save()

        update = get_mock_update('link_valid')
        self.api_client.process_update(json.dumps(update))
        expected_trapped = [
            ('getMe', dict()),
            ('sendMessage', {
                u'chat_id': u'463992304',
                u'disable_notification': u'False',
                u'text': u'Success!'
            })
        ]
        self.assertTrappedCalls(expected_trapped)

    def test_link_invalid(self):
        update = get_mock_update('link_invalid')
        self.api_client.process_update(json.dumps(update))
        expected_trapped = [
            ('getMe', dict()),
            ('sendMessage', {
                u'chat_id': u'463992304',
                u'disable_notification': u'False',
                u'text': u'Invalid secret'
            })
        ]
        self.assertTrappedCalls(expected_trapped)

    def assertTrappedCalls(self, expected):
        trapped = []
        while not self.api_server.trapped_requests.empty():
            trapped.append(self.api_server.trapped_requests.get())
        self.assertListEqual(expected, trapped)


class TelegramRendererTests(TestCase):
    def setUp(self):
        self.renderer = TelegramRenderer('example.com')

        self.sender = User.objects.create_user(
            username='sender', password='sender')
        self.sender.first_name = 'SenderFirstName'
        self.sender.last_name = 'SenderLastName'
        self.sender.save()

        self.recipient = User.objects.create_user(
            username='recipients', password='recipients')
        self.recipient.profile.telegram_uid = "463992304"
        self.recipient.first_name = 'RecipientFirstName'
        self.recipient.last_name = 'RecipientLastName'
        self.recipient.save()

        self.message_first = Message()
        self.message_first.sender = self.sender
        self.message_first.title = "title_first"
        self.message_first.text = "text_first"
        self.message_first.save()

        self.message_second = Message()
        self.message_second.sender = self.sender
        self.message_second.title = "title_second"
        self.message_second.text = "text_second"
        self.message_second.save()

        self.message_html = Message()
        self.message_html.sender = self.sender
        self.message_html.title = u"""<i>HTML</i>-formatted __message__\n""" \
                                  u"""Second line of subject"""
        self.message_html.text = "<b>Semi-bold <u>and underscored</u></b> text, <= 1 line />\n" + \
                                 "Quotes (', \")  and amp & are also fine"
        self.message_html.save()

    def test_notification_one_message(self):
        markdown, recipient_uid = self.renderer.render_notification(
            self.recipient.profile, [self.message_first])
        md_expected = u'''__u_vas_soobshenij 1 novoe_soobshenie__\n''' \
                      '''posmotret_soobshenija:\n''' \
                      '''example.com/mail/\n''' \
                      '''1. SenderFirstName SenderLastName -- _title_first_'''
        self.assertEqual(md_expected, markdown)
        self.assertEqual(self.recipient.profile.telegram_uid, recipient_uid)

    def test_notification_two_messages(self):
        markdown, recipient_uid = self.renderer.render_notification(
            self.recipient.profile, [self.message_first, self.message_second])
        md_expected = u'''__u_vas_soobshenij 2 novyh_soobshenija__\n''' \
                      '''posmotret_soobshenija:\n''' \
                      '''example.com/mail/\n''' \
                      '''1. SenderFirstName SenderLastName -- _title_first_\n''' \
                      '''2. SenderFirstName SenderLastName -- _title_second_'''
        self.assertEqual(md_expected, markdown)
        self.assertEqual(self.recipient.profile.telegram_uid, recipient_uid)

    def test_fulltext_one_recipient_simple(self):
        result = self.renderer.render_fulltext(
            self.message_first, [self.recipient])
        plaintext_expected = u'''New message\n''' \
                             u'''From: SenderFirstName SenderLastName\n''' \
                             u'''Subject: title_first\n''' \
                             u'''\n''' \
                             u'''text_first'''
        result_expected = [(plaintext_expected, self.recipient.profile.telegram_uid)]
        self.assertListEqual(result_expected, result)

    def test_fulltext_one_recipient_html(self):
        result = self.renderer.render_fulltext(
            self.message_html, [self.recipient])
        plaintext_expected = u'''New message\n''' \
                             u'''From: SenderFirstName SenderLastName\n''' \
                             u'''Subject: <i>HTML</i>-formatted __message__ Second line of subject\n''' \
                             u'''\n''' \
                             u'''Semi-bold and underscored text, <= 1 line />\n''' \
                             u'''Quotes (', \")  and amp & are also fine'''
        result_expected = [(plaintext_expected, self.recipient.profile.telegram_uid)]
        self.assertListEqual(result_expected, result)


class TelegramSenderTests(TestCase):
    api_server = None

    @classmethod
    def setUpClass(cls):
        super(TelegramSenderTests, cls).setUpClass()
        cls.api_server = TelegramApiServerMock()
        cls.api_server.start()

    def setUp(self):
        super(TelegramSenderTests, self).setUpClass()

        self.api_client = AnyTelegram(base_url=self.api_server.get_base_url())
        self.sender = TelegramSender(self.api_client)

        self.message_first = ('first_plain_text_message', 8664)
        self.message_second = ('second_plain_text_message', 390)
        self.message_html = ('plain_from_html_message', 51107)

    def test_notification(self):
        n_sent = self.sender.mass_send([self.message_first])
        self.assertEqual(1, n_sent)

        expected_trapped = [
            ('getMe', dict()),
            ('sendMessage', {
                u'chat_id': u'8664',
                u'disable_notification': u'False',
                u'text': u'first_plain_text_message'
            })
        ]
        self.assertTrappedCalls(expected_trapped)

    def assertTrappedCalls(self, expected):
        trapped = []
        while not self.api_server.trapped_requests.empty():
            trapped.append(self.api_server.trapped_requests.get())
        self.assertListEqual(expected, trapped)
