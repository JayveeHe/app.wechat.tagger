import codecs
import json
import random
import requests
from bs4 import BeautifulSoup
import time

__author__ = 'jayvee'


def get_content(web_url):
    content = requests.get(web_url).content
    soup = BeautifulSoup(content)
    text = ''
    # post time
    for div in soup.select('div'):
        text += div.text + '\n'
    return text


def get_wechat_content(wechat_url):
    """
    wechat parser
    :param wechat_url:
    :return:
    """
    content = requests.get(wechat_url).content
    soup = BeautifulSoup(content)
    text = ''
    # post time
    try:
        post_title = soup.select('h2#activity-name')[0].text.strip()
        post_date = soup.select('em#post-date')[0].text.strip()
        post_user = soup.select('a#post-user')[0].text.strip()
        for p in soup.select('p'):
            text += p.text.strip() + '\n'
        return {'post_content': text, 'post_date': post_date, 'post_user': post_user, 'post_title': post_title}
    except Exception, e:
        print e
        return None


def save_text_by_urls_file(urls_file_path):
    urls = open(urls_file_path, 'r').read().split('\n')
    count = 0
    for url in urls:
        # if count < 96:
        #     count += 1
        #     continue
        fout = codecs.open('./wechat_data/articles/%s.txt' % count, 'w', encoding='utf8')
        wc = get_wechat_content(url)
        if wc:
            fout.write(json.dumps(wc, ensure_ascii=False))
            print count
            count += 1
        else:
            continue
        time.sleep(random.random() * 1)
    print '%s text files saved!' % count


if __name__ == '__main__':
    # text = get_content('https://mp.weixin.qq.com/s?__biz=MzA5NjY2NTcxOA==&mid=208619922&idx=1&sn=29c8d227f5bcfe18d2514d5a674b18e5&scene=0&key=dffc561732c226510d998bd1bf72c4e63bcb74d2e075363e302e59c49f914dc291bb026b43a0771f55b1cae47f8f985c&ascene=0&uin=NDEyNTkyMzIw&devicetype=iMac+MacBookAir7%2C2+OSX+OSX+10.10.4+build(14E46)&version=11020201&pass_ticket=b8JW%2BAOpQwNn2S%2BcKZnE8iHSMVblW55JgqFaSocY762AWr%2B6wGEbGwldviMSS%2BDk')
    # for i in get_topics(text,10):
    #     print i

    save_text_by_urls_file('./wechat_data/weixin_urls.txt')
