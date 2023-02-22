
import time
import json
import requests_html
from Crypto.Hash import MD5
from urllib import parse

proxies = {
    'http': None,
    'https': None
}

def main(item):
    requests = requests_html.HTMLSession()
    playlist = []
    inx = 0
    have_more = True
    vid = item['链接'].split('/id_')[-1].split('.')[0]
    while have_more:
        url = 'https://log.mmstat.com/eg.js'
        response = requests.get(url, proxies=proxies)
        cna = response.headers['ETag'][1:-1]
        requests.cookies.set('cna', cna)
        appKey = '24679788'  # 定值
        t = str(int(time.time()))
        sign = t + '&' + appKey + '&' + json.dumps({}, separators=(',', ':'))
        sign = MD5.new(sign.encode()).hexdigest()
        parms = {
            'appKey': appKey,
            't': t,
            'sign': sign,
            'data': json.dumps({}, separators=(',', ':'))
        }
        url = 'https://acs.youku.com/h5/mtop.youku.subscribe.service.subscribe.favourite.batchisfav/3.0/?' + parse.urlencode(parms)
        requests.get(url, proxies=proxies)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        tk = requests.cookies.get('_m_h5_tk').split('_')[0]
        params = {
            'scene': 'component',
            'utdid': cna,
            'platform': 'pc',
            'nextSession': '{"componentId":"61518","level":"2","itemPageNo":"0","lastItemIndex":"0","itemStartStage":' + str(inx) + ',"itemEndStage":' + str(inx + 100) + '}',
            'videoId': vid,
        }
        system_info = {
            'os': 'pc',
            'device': 'pc',
            'ver': '1.0.0',
            'appPackageKey': 'pcweb',
            'appPackageId': 'pcweb'
        }
        data = {
            'ms_codes': '2019030100',
            'params': json.dumps(params, separators=(',', ':')),
            'system_info': json.dumps(system_info, separators=(',', ':'))
        }
        appKey = '24679788'
        t = str(int(time.time()))
        sign = tk + '&' + t + '&' + appKey + '&' + json.dumps(data, separators=(',', ':'))
        sign = MD5.new(sign.encode()).hexdigest()
        parms = {
            'appKey': appKey,
            't': t,
            'sign': sign,
            'data': json.dumps(data, separators=(',', ':'))
        }
        url = 'https://acs.youku.com/h5/mtop.youku.columbus.gateway.new.execute/1.0/?' + parse.urlencode(parms)
        response = requests.get(url, headers=headers, proxies=proxies).json()
        session = json.loads(response['data']['2019030100']['data']['data']['session'])
        if session['lastItemIndex'] == '100':
            inx += 100
        else:
            have_more = False
        for vid in response['data']['2019030100']['data']['nodes']:
            if vid['data']['videoType'] == '正片':
                url = 'https://v.youku.com/v_show/id_' + vid['data']['action']['value'] + '.html'
                playlist.append(url)
    if len(playlist) > item['追剧日历'][0]:
        return True
    else:
        return False


if __name__ == '__main__':
    main({'链接': 'https://v.youku.com/v_show/id_XNTk0MDcyMzQyNA==.html', '更新时间': '19:01:02', '追剧日历': [11, 12], '偏移时间': 0})