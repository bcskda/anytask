updates = dict()

updates['bcskda_start'] = {
    "update_id": 839623864,
    "message": {
        "message_id": 27,
        "from": {
            "id": 463992304,
            "is_bot": False,
            "first_name": "\u0414\u043c\u0438\u0442\u0440\u0438\u0439",
            "last_name": "\u041a\u0443\u043f\u0446\u043e\u0432",
            "username": "bcskda",
            "language_code": "ru"
        },
        "chat": {
            "id": 463992304,
            "first_name": "\u0414\u043c\u0438\u0442\u0440\u0438\u0439",
            "last_name": "\u041a\u0443\u043f\u0446\u043e\u0432",
            "username": "bcskda",
            "type": "private"
        },
        "date": 1619899621,
        "text": "/start",
        "entities": [
            {
                "offset": 0,
                "length": 6,
                "type": "bot_command"
            }
        ]
    }
}

updates['link_valid'] = {
    "update_id": 839623868,
    "message": {
        "message_id": 32, "from": {
            "id": 463992304, "is_bot": False,
            "first_name": "\u0414\u043c\u0438\u0442\u0440\u0438\u0439",
            "last_name": "\u041a\u0443\u043f\u0446\u043e\u0432",
            "username": "bcskda", "language_code": "ru"
        },
        "chat": {
            "id": 463992304,
            "first_name": "\u0414\u043c\u0438\u0442\u0440\u0438\u0439",
            "last_name": "\u041a\u0443\u043f\u0446\u043e\u0432", "username": "bcskda",
            "type": "private"
        }, "date": 1619900327,
        "text": "/link 53cd4396-8b96-45a7-a123-11f1107b56c7",
        "entities": [{
            "offset": 0, "length": 5, "type": "bot_command"
        }]
    }
}

updates['link_invalid'] = {
    "update_id": 839623868,
    "message": {
        "message_id": 32, "from": {
            "id": 463992304, "is_bot": False,
            "first_name": "\u0414\u043c\u0438\u0442\u0440\u0438\u0439",
            "last_name": "\u041a\u0443\u043f\u0446\u043e\u0432",
            "username": "bcskda", "language_code": "ru"
        },
        "chat": {
            "id": 463992304,
            "first_name": "\u0414\u043c\u0438\u0442\u0440\u0438\u0439",
            "last_name": "\u041a\u0443\u043f\u0446\u043e\u0432", "username": "bcskda",
            "type": "private"
        }, "date": 1619900327,
        "text": "/link 00000000-1111-2222-3333-444444444444",
        "entities": [{
            "offset": 0, "length": 5, "type": "bot_command"
        }]
    }
}


def get_mock_update(key):
    return updates[key]
