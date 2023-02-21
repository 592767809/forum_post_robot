
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

    def init_bot(self, option):
        pass

    def send_message(self):
        if self.bot_type == self.TG:
            pass
        elif self.bot_type == self.DIS:
            pass
        elif self.bot_type == self.WX:
            pass
        else:
            raise Exception('')
