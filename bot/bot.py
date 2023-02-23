
import os
import time
import requests_html


class Bot(object):

    TG = 1
    DIS = 2
    WX = 3

    def __init__(self, bot_type):
        assert bot_type in [1, 2, 3]
        self.bot_type = bot_type
        self.requests = requests_html.HTMLSession()
        self.token = ''
        self.user = ''
        self.proxies = {
            'http': '',
            'https': '',
        }

    def set_proxies(self, port: str):
        self.proxies = {
            'http': 'http://127.0.0.1:' + port,
            'https': 'http://127.0.0.1:' + port,
        }

    def init_bot(self, option):
        if self.bot_type == self.TG:
            self.token = option['token']
            self.user = option['chat_id']
        elif self.bot_type == self.DIS:
            self.token = option['token']
            self.user = option['chat_id']
        elif self.bot_type == self.WX:
            self.user = option['chat_id']
        else:
            raise Exception('未知的机器人类型')

    def send_message(self, message):
        if self.bot_type == self.TG:
            data = {
                'chat_id': self.user,
                'text': message
            }
            self.requests.post(f'https://api.telegram.org/bot{self.token}/sendMessage', json=data, proxies=self.proxies)
        elif self.bot_type == self.DIS:
            headers = {
                'authorization': self.token
            }
            data = {
                'content': message,
                'nonce': str((int(time.time() * 1000) - 1420070400000) << 22),
                'tts': False
            }
            self.requests.post(f'https://discord.com/api/v9/channels/{self.user}/messages', headers=headers, json=data, proxies=self.proxies)
        elif self.bot_type == self.WX:
            data = {
                "msgtype": "text",
                "text": {
                    "content": message,
                    "mentioned_list": ["@all"]
                }
            }
            self.requests.post(f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={self.user}', json=data, proxies=self.proxies)
        else:
            raise Exception('未知的机器人类型')
