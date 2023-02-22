
import requests_html

try:
    import telegram
except:
    telegram = None


class Bot(object):

    TG = 1
    DIS = 2
    WX = 3

    def __init__(self, bot_type):
        assert bot_type in [1, 2, 3]
        self.bot_type = bot_type
        self.bot = None
        self.token = ''
        self.user = ''

    def init_bot(self, option):
        if self.bot_type == self.TG:
            assert telegram
            self.token = option['token']
            self.user = option['chat_id']
            self.bot = telegram.Bot(self.token)
        elif self.bot_type == self.DIS:
            self.bot = requests_html.HTMLSession()
        elif self.bot_type == self.WX:
            self.bot = requests_html.HTMLSession()
        else:
            raise Exception('未知的机器人类型')

    def send_message(self, message):
        assert self.bot
        if self.bot_type == self.TG:
            self.bot.sendMessage(self.user, message)
        elif self.bot_type == self.DIS:
            pass
        elif self.bot_type == self.WX:
            pass
        else:
            raise Exception('未知的机器人类型')
