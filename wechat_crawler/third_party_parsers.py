# coding=utf-8
import codecs
import random
from bs4 import BeautifulSoup
import requests
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'jayvee'


def parse_public_account(account_id, max_page=None, start_index=0):
    """
    public account article parser, using http://chuansong.me
    :param account_id:
    :return:
    """
    # basic configure
    base_url = 'http://chuansong.me/account/'
    combined_url = base_url + account_id
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9'}
    )

    # start crawl
    page_count = 0
    page_html = s.get(combined_url + '?start=%s' % (start_index + page_count * 12)).content
    soup = BeautifulSoup(page_html)
    links = soup.select('a.question_link')
    article_list = []
    while len(links) > 0 and (page_count < max_page or not max_page):
        print 'crawling page:%s, start index = %s' % (page_count, start_index + page_count * 12)
        for i in links:
            chuansong_url = 'http://chuansong.me%s' % i.attrs['href']
            print chuansong_url
            article_json = get_chuansongmen_content(chuansong_url)
            post_title = article_json['post_title'].replace('/', '、')
            print 'saving %s' % post_title
            # file name validation
            try:
                aout = codecs.open(u'./crawl_data/大象公会/%s.txt' % post_title, 'w', encoding='utf8')
                aout.write(json.dumps(article_json, ensure_ascii=False))
            except IOError, ie:
                print ie
                print 'skipped article:%s' % post_title
                continue
            article_list.append(article_json)
            time.sleep(random.random() * 2 + 1)
        print 'page %s done, sleep 5 sec to avoid being banned' % page_count
        time.sleep(5)
        page_count += 1
        page_html = s.get(combined_url + '?start=%s' % (start_index + page_count * 12)).content
        soup = BeautifulSoup(page_html)
        links = soup.select('a.question_link')
    print soup.text
    return article_list


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
        post_title = soup.select('#activity-name')[0].text.strip()
        post_date = soup.select('#post-date')[0].text.strip()
        post_user = soup.select('#post-user')[0].text.strip()
        for p in soup.select('p'):
            text += p.text.strip() + '\n'
        return {'post_content': text, 'post_date': post_date, 'post_user': post_user, 'post_title': post_title}
    except Exception, e:
        print e
        return None


def get_chuansongmen_content(chuansong_url):
    """
    chuansongmen parser
    :param chuansong_url:
    :return:
    """
    for i in xrange(3):
        try:
            s = requests.session()
            s.headers.update({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9'}
            )
            raw_html = s.get(chuansong_url).content
            soup = BeautifulSoup(raw_html)

            post_title = soup.select('#activity-name')[0].text.strip()
            post_date = soup.select('#post-date')[0].text.strip()
            post_user = soup.select('#post-user')[0].text.strip()
            content = ''
            # 有些公众号的文本格式比较丰富，有些则是简单的，在这里需要做一个判断
            rich_contents = soup.select('div[class=rich_media_content] p')
            if len(rich_contents) > 0:
                for p in soup.select('div[class=rich_media_content] p'):
                    if not p.has_attr('style'):
                        content += p.text
            else:
                for p in soup.select('p'):
                    # if not p.has_attr('style'):
                    content += p.text

            return {'post_content': content, 'post_date': post_date, 'post_user': post_user, 'post_title': post_title}
        except requests.Timeout, to:
            print to
            continue
        except Exception, e:
            print e
            # print raw_html
            print 'times:%s, retry in 5 sec....' % i
            time.sleep(5)
            continue


if __name__ == '__main__':
    import json

    # print json.dumps(get_chuansongmen_content('http://chuansong.me/n/1690024'), ensure_ascii=False)
    # result = parse_public_account('idxgh2013',max_page=5, start_index=348)
    # for i in result:
    #     fout = open('./crawl_data/%s.txt' % (i['post_title']), 'w')
    #     fout.write(json.dumps(i, ensure_ascii=False))
    print json.dumps(get_chuansongmen_content('http://chuansong.me/n/1705764'),ensure_ascii=False)
