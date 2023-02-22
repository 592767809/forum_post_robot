
import time
import queue
import threading
import traceback
from urllib import parse
from bot.bot import Bot
from config import config
from watch_calendar.timer import calendar_dict
from worker import youku


class Consumer(threading.Thread):

    def __init__(self, work_queue, bot):
        super().__init__()
        self.work_queue = work_queue
        self.bot = bot
        self.timer = 600

    def run(self):
        while True:
            if self.work_queue.empty():
                break
            else:
                item: dict = self.work_queue.get()
                locale_time = time.strftime("%H:%M:%S", time.localtime())
                locale_time = time.strptime(locale_time, '%H:%M:%S')
                locale_time = locale_time.tm_hour * 3600 + locale_time.tm_min * 60 + locale_time.tm_sec
                if locale_time > 84600:
                    break
                server_time = time.strptime(item['更新时间'], '%H:%M:%S')
                server_time = server_time.tm_hour * 3600 + server_time.tm_min * 60 + server_time.tm_sec + item['偏移时间']
                if locale_time >= server_time:
                    if check_renew(item):
                        message = item['标题'] + ' 已更新 '
                        if len(item['追剧日历']) > 1:
                            message += f'第 {item["追剧日历"][0]} 到 {item["追剧日历"][-1]} 集 '
                        else:
                            message += f'第 {item["追剧日历"][0]} 集 '
                        message += '快去更新吧！'
                        self.bot.send_message(message)
                        break
                    else:
                        item['偏移时间'] += self.timer  # 下次检查的秒数
                time.sleep(self.timer // 10)
                self.work_queue.put(item)


def check_renew(item):
    try:
        params = parse.urlparse(item['链接'])
        if params.hostname == 'v.youku.com':
            return youku.main(item)
        else:
            raise Exception('未知的链接类型：' + item['链接'])
    except:
        print(traceback.format_exc())
        return False


def main():
    bot = Bot(Bot.TG)
    # bot.set_proxies('7890')  # 如果需要代理就取消注释
    bot.init_bot({
        'token': config.bot_token,
        'chat_id': config.chat_id
    })
    work_queue = queue.Queue(maxsize=0)
    thread_list = []
    print('监控目录：')
    for item in calendar_dict:
        item['偏移时间'] = 0
        item['追剧日历'] = item['追剧日历'][time.strftime("%Y-%m-%d", time.localtime())]

        locale_time = time.strftime("%H:%M:%S", time.localtime())
        locale_time = time.strptime(locale_time, '%H:%M:%S')
        locale_time = locale_time.tm_hour * 3600 + locale_time.tm_min * 60 + locale_time.tm_sec

        server_time = time.strptime(item['更新时间'], '%H:%M:%S')
        server_time = server_time.tm_hour * 3600 + server_time.tm_min * 60 + server_time.tm_sec

        if locale_time >= server_time:
            item['更新时间'] = time.strftime("%H:%M:%S", time.localtime())

        work_queue.put(item)
        print(f'{item["标题"]} 第 {item["追剧日历"][0]} 到 {item["追剧日历"][-1]} 集')

    for t in range(work_queue.qsize()):
        thread = Consumer(work_queue, bot)
        thread.start()
        thread_list.append(thread)

    for t in thread_list:
        t.join()


if __name__ == '__main__':
    main()