
import requests_html

try:
    import telegram
except:
    telegram = None

# bot = telegram.Bot('')
# bot.sendMessage()


class Bot(object):

    TG = 1
    DIS = 2
    WX = 3

    def __init__(self, bot_type):
        assert bot_type in [1, 2, 3]
        self.bot_type = bot_type
        self.bot = None

    def init_bot(self, option):
        if self.bot_type == self.TG:
            assert telegram
            bot = telegram.Bot(option['token'])
        elif self.bot_type == self.DIS:
            bot = requests_html.HTMLSession()
        elif self.bot_type == self.WX:
            bot = requests_html.HTMLSession()
        else:
            raise Exception('')

    def send_message(self, user, message):
        if self.bot_type == self.TG:
            pass
        elif self.bot_type == self.DIS:
            pass
        elif self.bot_type == self.WX:
            pass
        else:
            raise Exception('')
