import BaseHTTPServer
import SocketServer
import json
import threading
from Queue import Queue

from django.test import TestCase

from users.models import User, UserProfile
from common import AnyTelegram
from test_data import get_mock_update


class TelegramApiServerMock(threading.Thread):
    LISTEN_ADDR = '127.0.0.1'
    LISTEN_PORT = 29668

    class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
        def do_GET(self):  # NOQA
            req = self.path
            self.server.trapped_requests.put(req)
            self.send_response(501)
            self.end_headers()

        def do_POST(self):  # NOQA
            req = self.path
            self.server.trapped_requests.put(req)
            self.send_response(501)
            self.end_headers()

    def __init__(self):
        super(TelegramApiServerMock, self).__init__()
        self.server = None
        self.trapped_requests = Queue()

    def get_base_url(self):
        return 'http://{}:{}/'.format(self.LISTEN_ADDR, self.LISTEN_PORT)

    def run(self):
        server_address = (self.LISTEN_ADDR, self.LISTEN_PORT)
        self.server = SocketServer.TCPServer(server_address, self.Handler)
        self.server.allow_reuse_address = True
        self.server.submit_error = False
        self.server.trapped_requests = self.trapped_requests
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()


class AnyTelegramTests(TestCase):
    api_server = None

    @classmethod
    def setUpClass(cls):
        super(AnyTelegramTests, cls).setUpClass()
        cls.api_server = TelegramApiServerMock()
        cls.api_server.start()

    @classmethod
    def tearDownClass(cls):
        cls.api_server.stop()
        super(AnyTelegramTests, cls).tearDownClass()

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
        result = self.api_client.process_update(json.dumps(update))
        trapped = []
        while not self.api_server.trapped_requests.empty():
            trapped.append(self.api_server.trapped_requests.get())
        self.assertIsNone(result)
        self.assertListEqual([], trapped)
