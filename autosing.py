# -*- coding: utf8 -*-

"""
cron: 30 5,12,18 * * *
new Env('福利吧签到');
"""

import requests
import re
import os, sys

def load_send():
    global send
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    if os.path.exists(cur_path + "/sendNotify.py"):
        try:
            from sendNotify import send
        except:
            send=False
            print("加载通知服务失败~")
    else:
        send=False
        print("加载通知服务失败~")
load_send()

def start(cookie, username):
    try:
        s = requests.session()

        flb_url = get_addr()
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Accept - Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'cache-control': 'max-age=0',
                   'Host': flb_url,
                   'Upgrade-Insecure-Requests': '1',
                   'Cookie': cookie,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62'}

        # 访问Pc主页
        user_info = s.get('https://' + flb_url + '/forum.php?mobile=no', headers=headers).text
        user_name = re.search(r'title="访问我的空间">(.*?)</a>', user_info)
        print(user_name)
        if user_name.group(1) != username:
            raise Exception("【福利吧】cookie失效???????")
        # 获取签到链接,并签到
        qiandao_url = re.search(r'}function fx_checkin(.*?);', user_info).group(1)
        qiandao_url = qiandao_url[47:-2]
        print(qiandao_url)
        # 签到
        s.get('https://' + flb_url + '/' + qiandao_url, headers=headers).text

        # 获取积分
        user_info = s.get('https://' + flb_url + '/forum.php?mobile=no', headers=headers).text

        current_money = re.search(r'<a.*? id="extcreditmenu".*?>(.*?)</a>', user_info).group(1)
        sing_day = re.search(r'<div class="tip_c">(.*?)</div>', user_info).group(1)
        log_info = "{}当前{}".format(sing_day, current_money)
        print(log_info)
        send(log_info)

    except Exception as e:
        print("签到失败，失败原因:"+str(e))
        send(str(e))


def get_addr():
    pub_page = "https://fuliba-1251744788.file.myqcloud.com"
    ret = requests.get(pub_page)
    ret.encoding = "utf-8"
    bbs_addr = re.findall(r'<a href=.*?><i>https://(.*?)</i></a>', ret.text)[1]
    return bbs_addr


if __name__ == '__main__':
    # cookie = "此处填入COOKIE"
    # username = "此处填入用户名"
    cookie = os.getenv("FUBA")
    user_name = os.getenv("FUBAUN")
    start(cookie, user_name)
