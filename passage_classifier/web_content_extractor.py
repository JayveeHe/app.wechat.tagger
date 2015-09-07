import requests
from bs4 import BeautifulSoup
from gensim_utils.lda_utils import get_topics

__author__ = 'jayvee'


def get_content(web_url):
    content = requests.get(web_url).content
    soup = BeautifulSoup(content)
    text = ''
    #
    for div in soup.select('div'):
        text += div.text + '\n'
    return text


if __name__ == '__main__':
    text = get_content('https://mp.weixin.qq.com/s?__biz=MzA5NjY2NTcxOA==&mid=208619922&idx=1&sn=29c8d227f5bcfe18d2514d5a674b18e5&scene=0&key=dffc561732c226510d998bd1bf72c4e63bcb74d2e075363e302e59c49f914dc291bb026b43a0771f55b1cae47f8f985c&ascene=0&uin=NDEyNTkyMzIw&devicetype=iMac+MacBookAir7%2C2+OSX+OSX+10.10.4+build(14E46)&version=11020201&pass_ticket=b8JW%2BAOpQwNn2S%2BcKZnE8iHSMVblW55JgqFaSocY762AWr%2B6wGEbGwldviMSS%2BDk')
    for i in get_topics(text,10):
        print i
