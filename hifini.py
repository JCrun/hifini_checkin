"""
cron: 0 9 * * *
new Env('hifini签到');
"""
from lxml import etree
import requests
import json
import time
import os
import re
import sys
import random



def randomuserAgent():
    global uuid,addressid,iosVer,iosV,clientVersion,iPhone,area,ADID,lng,lat
    uuid=''.join(random.sample(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','a','b','c','z'], 40))
    addressid = ''.join(random.sample('1234567898647', 10))
    iosVer = ''.join(random.sample(["15.1.1","14.5.1", "14.4", "14.3", "14.2", "14.1", "14.0.1"], 1))
    iosV = iosVer.replace('.', '_')
    clientVersion=''.join(random.sample(["10.3.0", "10.2.7", "10.2.4"], 1))
    iPhone = ''.join(random.sample(["8", "9", "10", "11", "12", "13"], 1))
    area=''.join(random.sample('0123456789', 2)) + '_' + ''.join(random.sample('0123456789', 4)) + '_' + ''.join(random.sample('0123456789', 5)) + '_' + ''.join(random.sample('0123456789', 4))
    ADID = ''.join(random.sample('0987654321ABCDEF', 8)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 12))
    lng='119.31991256596'+str(random.randint(100,999))
    lat='26.1187118976'+str(random.randint(100,999))
    UserAgent=''
    if not UserAgent:
        return f'jdapp;iPhone;10.0.4;{iosVer};{uuid};network/wifi;ADID/{ADID};model/iPhone{iPhone},1;addressid/{addressid};appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS {iosV} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1'
    else:
        return UserAgent

#以上部分参考Curtin的脚本：https://github.com/curtinlv/JD-Script

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


def printf(text):
    print(text)
    sys.stdout.flush()

def get_remarkinfo():
    url='http://127.0.0.1:5600/api/envs'
    try:
        with open('/ql/config/auth.json', 'r') as f:
            token=json.loads(f.read())['token']
        headers={
            'Accept':'application/json',
            'authorization':'Bearer '+token,
            }
        response=requests.get(url=url,headers=headers)

        for i in range(len(json.loads(response.text)['data'])):
            if json.loads(response.text)['data'][i]['name']=='JD_COOKIE':
                try:
                    if json.loads(response.text)['data'][i]['remarks'].find('@@')==-1:
                        remarkinfos[json.loads(response.text)['data'][i]['value'].split(';')[1].replace('pt_pin=','')]=json.loads(response.text)['data'][i]['remarks'].replace('remark=','')
                    else:
                        remarkinfos[json.loads(response.text)['data'][i]['value'].split(';')[1].replace('pt_pin=','')]=json.loads(response.text)['data'][i]['remarks'].split("@@")[0].replace('remark=','').replace(';','')
                except:
                    pass
    except:
        print('读取auth.json文件出错，跳过获取备注')

def qiandao(ck):

    url='https://www.hifini.com/sg_sign.htm'
    headers = {
        'authority': 'www.hifini.com',
        'accept': 'text/plain, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en-HK;q=0.8,en;q=0.7,zh-HK;q=0.6',
        # 'content-length': '0',
        'cookie': ck,
        'dnt': '1',
        'origin': 'https://www.hifini.com',
        'referer': 'https://www.hifini.com/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': UserAgent,
        'x-requested-with': 'XMLHttpRequest',
    }
    response=requests.post(url=url,headers=headers)
    # response.text = {
    #     "code": "0",
    #     "message": "成功签到！今日排名20328，总奖励1金币！"
    # }r
    isnull=True
    if response.text.find('成功签到')!=-1:
        isnull=False
        printf('【签到成功】'+response.text)
    else:
        printf('【签到失败】'+response.text)
    if send:
        if isnull:
            send('【hifini签到】','【签到失败】'+response.text)
        else:
            send('【hifini签到】','【签到成功】'+response.text)

def get_coin_num():
    url='https://www.hifini.com/my.htm'
    headers = {
        'authority': 'www.hifini.com',
        'accept': 'text/plain, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en-HK;q=0.8,en;q=0.7,zh-HK;q=0.6',
        # 'content-length': '0',
        'cookie': ck,
        'dnt': '1',
        'origin': 'https://www.hifini.com',
        'referer': 'https://www.hifini.com/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': UserAgent,
        'x-requested-with': 'XMLHttpRequest',
    }
    response = requests.post(url=url, headers=headers)
    text = response.text
    pattern = etree.HTML(text)
    coin_num = pattern.xpath('//span[@class="text-muted"]/em/text()')[0]
    return coin_num

if __name__ == '__main__':
    remarkinfos={}
    try:
        get_remarkinfo()
    except:
        pass
    try:
        cks = os.environ["HIFINI_COOKIE"].split("&")
    except:
        f = open("/jd/config/config.sh", "r", encoding='utf-8')
        cks = re.findall(r'Cookie[0-9]*="(bbs_sid=.*?;bbs_token=.*?;cookie_test=.*?;)"', f.read())
        f.close()
    for ck in cks:
        ck = ck.strip()
        if ck[-1] != ';':
            ck += ';'

        UserAgent=randomuserAgent()
        qiandao(ck)
        time.sleep(5)
        coin_num = get_coin_num()
        printf('【金币数量】'+coin_num)
        if send:
            send('【hifini签到】','【金币数量】'+coin_num)
        time.sleep(5)
    printf('【签到结束】')
    if send:
        send('【hifini签到】','【签到结束】')
    sys.exit(0)
