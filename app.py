# coding=utf-8
import json
import os
import re
import sys

from flask import Flask, request, make_response, render_template, redirect
from flask.ext.cors import cross_origin
import requests
import jieba.analyse
import numpy as np
from sklearn.externals import joblib

from passage_classifier.vector_builder import VectorBuilder
from wechat_analyzer import TaggingUtils
from wechat_analyzer.demo_related import demo_main
from wechat_analyzer.web_content_extractor import get_content

# todo demo only
from wechat_analyzer.basic_class.Article import Article
from wechat_analyzer.basic_class.Reaction import Reaction
from wechat_analyzer.basic_class.WechatUser import WechatUser

reload(sys)
sys.setdefaultencoding('utf-8')

project_path = os.path.dirname(__file__)
sys.path.append(project_path)
app = Flask(__name__)
vb = VectorBuilder()
nbclf = joblib.load('%s/data/models/nbclf.model' % project_path)  # for mac pycharm


# nbclf = joblib.load('./data/models/nbclf.model') # for linux os


# logger = logging.getLogger('logentries')
# logger.setLevel(logging.INFO)
# Note if you have set up the logentries handler in Django, the following line is not necessary
# lh = logentries.LogentriesHandler(config_token.LOGENTRIES_TOKEN)
# fm = logging.Formatter('%(asctime)s : %(levelname)s, %(message)s',
#                        '%a %b %d %H:%M:%S %Y')
# lh.setFormatter(fm)
# logger.addHandler(lh)
#
# Import bugsnag
#
# Configure Bugsnag
#
# Attach Bugsnag to Flask's exception handler
# handle_exceptions(app)
@app.route('/status', methods=['GET'])
def check_status():
    return 'The server senz-text is running'


@app.route('/demo', methods=['GET'])
def demo():
    return render_template('index.html')


@app.route('/tags', methods=['POST'])
def get_keywords():
    raw_in = str(request.data).replace('\r\n', '')
    raw_in = raw_in.replace('\n', '')
    raw_in = raw_in.replace('\t', '')
    req_data = json.loads(raw_in)
    content = req_data.get('content')
    keyword_num_str = req_data.get('keyword_num')
    if keyword_num_str:
        keyword_num = int(keyword_num_str)
    else:
        keyword_num = 10
    tags = jieba.analyse.extract_tags(content, topK=keyword_num)
    resp = make_response(json.dumps({'code': 0, 'tags': tags}, ensure_ascii=False), 200)
    return resp


@app.route('/predict', methods=['POST'])
def classify_passage():
    raw_in = str(request.data).replace('\r\n', '')
    raw_in = raw_in.replace('\n', '')
    raw_in = raw_in.replace('\t', '')
    req_data = json.loads(raw_in)
    content = req_data.get('content')
    pred_nb = nbclf.predict(np.array(vb.build_single_vec(content)))
    class_dict = {1: u'car', 2: u'finance', 3: u'tech',
                  4: u'health', 5: u'sport', 6: u'travel',
                  7: u'education', 8: 'jobs', 9: u'culture', 10: u'military'}
    resp = make_response(json.dumps({'code': 0, 'class': class_dict[pred_nb[0]]}), 200)
    return resp


@app.route('/predict_boson', methods=['POST'])
def classify_passage_boson():
    raw_in = str(request.data).replace('\r\n', '')
    raw_in = raw_in.replace('\n', '')
    raw_in = raw_in.replace('\t', '')
    req_data = json.loads(raw_in)
    content = req_data.get('content')
    top_k = req_data.get('top_k')
    print 'top_k=%s' % top_k
    classify_result = requests.post('http://bosonnlp.com/analysis/category', {'data': content}).content
    keyword_result = json.loads(
        requests.post('http://bosonnlp.com/analysis/key?top_k=%s' % top_k, {'data': content}).content)
    class_dict = {0: u'体育', 1: u'教育', 2: u'财经', 3: u'社会',
                  4: u'娱乐', 5: u'军事', 6: u'国内',
                  7: u'科技', 8: '互联网', 9: u'房产', 10: u'国际',
                  11: u'女人', 12: u'汽车', 13: u'游戏'}
    classify_result = int(re.compile('\d+').findall(classify_result)[0])
    jieba_textrank = jieba.analyse.textrank(content, )
    jieba_keywords = jieba.analyse.extract_tags(content, allowPOS=['n', 'vn', 'ns', 'v'])
    resp = make_response(
        json.dumps({'code': 0, 'class': class_dict[classify_result], 'keyword': keyword_result,
                    'jieba_textrank': jieba_textrank, 'jieba_keywords': jieba_keywords}, ensure_ascii=False),
        200)
    return resp


@app.route('/predict_boson_url', methods=['POST'])
@cross_origin()
def classify_passage_boson_url():
    url = request.form['url']
    content = get_content(url)
    # print 'top_k=%s' % top_k
    classify_result = requests.post('http://bosonnlp.com/analysis/category', {'data': content}).content
    keyword_result = json.loads(
        requests.post('http://bosonnlp.com/analysis/key?top_k=%s' % 100, {'data': content}).content)
    class_dict = {0: u'体育', 1: u'教育', 2: u'财经', 3: u'社会',
                  4: u'娱乐', 5: u'军事', 6: u'国内',
                  7: u'科技', 8: '互联网', 9: u'房产', 10: u'国际',
                  11: u'女人', 12: u'汽车', 13: u'游戏'}
    print classify_result
    classify_result = int(re.compile('\d+').findall(classify_result)[0])
    jieba_textrank = jieba.analyse.textrank(content, topK=15)
    jieba_keywords = jieba.analyse.extract_tags(content, allowPOS=['n', 'vn', 'ns', 'v'], topK=15)
    topic_list = TaggingUtils.passage_second_level_classify(content)
    resp = make_response(
        json.dumps({'code': 0, 'class': class_dict[classify_result], 'keyword': keyword_result,
                    'jieba_textrank': jieba_textrank, 'jieba_keywords': jieba_keywords,
                    'topic_list': topic_list},
                   ensure_ascii=False),
        200)
    return resp


# todo wechat demo parts, delete later
article_map = demo_main.init_articles()
user_map = {}


# user_vec_map = {}

@app.route('/wechat_articles', methods=['GET'])
def wechat_demo_get_articles():
    a_list = []
    for a in article_map:
        article = article_map[a]
        a_list.append({'a_id': article.a_id, 'a_tags': article.a_tags})
    resp = make_response(json.dumps(a_list), 200)
    return resp


@app.route('/user_analyse', methods=['GET'])
def redirect_user_req():
    params = request.args
    openid = params['openid']
    if openid not in user_map:
        user_map[openid] = WechatUser('123', [], {}, {}, {})
    a_id = params['a_id']
    # counting
    print a_id
    wechatuser = user_map[openid]
    temp_a_namemap = {'tfboy': u'TFBOYS为什么这样红 | 大象公会.txt', 'media': u'【推荐】注意力时代不可不知的新媒体8人.txt',
                      'sportclass': u'体育与阶层 | 大象公会.txt', 'prod': u'无人见过我们真正的产品 | 大象公会.txt',
                      'wenzhou': u'温州话能成为军事密码么 | 大象公会.txt', 'qiuyi': u'球衣往事 | 大象公会.txt'}
    reaction = Reaction('333', 'read', temp_a_namemap[a_id], '123')
    wechatuser.user_tag_score_vec = wechatuser.user_tagging([reaction], demo_main.weight_map, a_map=article_map)
    # url redirect
    a_url_map = {
        'tfboy': 'http://mp.weixin.qq.com/s?__biz=MzI1NTAxMTQwNQ==&mid=209956548&idx=1&sn=cc52b85072fefa296a7c5cb82dc62d34&scene=0&key=dffc561732c22651ddec47d91a219c794d0b204ef1258177ff8c11b3a77ba4188a6f8460a018e3f3e4bce4f5d8842b1f&ascene=0&uin=NDEyNTkyMzIw&devicetype=iMac+MacBookAir7%2C2+OSX+OSX+10.10.5+build(14F27)&version=11020201&pass_ticket=TzKtzXhA0l8eQjH%2F6GQzDu0eUG3q2CfimIMMueJ6COMF%2FlRyv63DyQgfdczmq0lj',
        'media': 'http://mp.weixin.qq.com/s?__biz=MzI1NTAxMTQwNQ==&mid=209956583&idx=1&sn=136dd5735898adb03dc017af6a4ad1a5#rd',
        'sportclass': 'http://mp.weixin.qq.com/s?__biz=MzI1NTAxMTQwNQ==&mid=209956618&idx=1&sn=34d1f00231abc79bb6d5e530e681f8f2#rd',
        'prod': 'http://mp.weixin.qq.com/s?__biz=MzI1NTAxMTQwNQ==&mid=209956649&idx=1&sn=f25062f29eb6bc779bf1b15a3690603c#rd',
        'wenzhou': 'http://mp.weixin.qq.com/s?__biz=MzI1NTAxMTQwNQ==&mid=209956662&idx=1&sn=da827726c75655d826be3c348bc88549#rd',
        'qiuyi': 'http://mp.weixin.qq.com/s?__biz=MzI1NTAxMTQwNQ==&mid=209956662&idx=1&sn=da827726c75655d826be3c348bc88549#rd'}
    return redirect(a_url_map[a_id], code=302)


@app.route('/show_user_vec', methods=['GET'])
def show_user_vec():
    temp_user_vec_map = {}
    for user_key in user_map:
        temp_user_vec_map[user_key] = user_map[user_key].user_tag_score_vec

    return json.dumps(temp_user_vec_map, ensure_ascii=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, debug=True)
