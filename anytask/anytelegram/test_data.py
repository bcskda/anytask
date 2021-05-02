def get_mock_update(key):
    assert key == 'bcskda_start'
    return {
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
