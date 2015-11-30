# coding=utf-8
import hashlib
import json
import os
import re
import sys
import datetime
import time
from urllib import urlencode

from flask import Flask, request, make_response, render_template, redirect
from flask.ext.cors import cross_origin
import requests
import jieba.analyse
import numpy as np
from sklearn.externals import joblib

from passage_classifier.vector_builder import VectorBuilder
from tencent_qcloud_classifier import wenzhi_utils
from wechat_analyzer import tagging_utils, DAO_utils
from wechat_analyzer.content_extractor import Extractor
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
    topic_list = tagging_utils.passage_second_level_classify(content)
    resp = make_response(
        json.dumps({'code': 0, 'class': class_dict[classify_result], 'keyword': keyword_result,
                    'jieba_textrank': jieba_textrank, 'jieba_keywords': jieba_keywords,
                    'topic_list': topic_list},
                   ensure_ascii=False),
        200)
    return resp


# 后端统计逻辑
# @app.route('/show_user_vec', methods=['GET'])
# def show_user_vec():
#     temp_user_vec_map = {}
#     for user_key in user_map:
#         temp_user_vec_map[user_key] = user_map[user_key].user_tag_score_vec
#
#     return json.dumps(temp_user_vec_map, ensure_ascii=False)

@app.route('/api/v1/record', methods=['GET'])
def record_reactions():
    """
    用于记录交互行为
    :return:
    """
    try:
        user_id = request.args['openid']
        media_id = request.args['media_id']
        thumb_id = request.args['thumb_id']
        article_id = hashlib.md5(media_id + thumb_id).hexdigest()
        article = DAO_utils.mongo_get_article(article_id)
        redirect_url = article.a_url
        # if code:
        #     token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        #     raw_auth_result = requests.get(token_url, {'appid': APPID, 'secret': SECRET, 'code': code})
        #     auth_result = json.loads(raw_auth_result)
        #     user_id = auth_result.get('openid')
        reaction_id = hashlib.md5(user_id + article_id + str(time.time())).hexdigest()
        reaction = Reaction(reaction_id=reaction_id, reaction_type='read', reaction_a_id=article_id,
                            reaction_user_id=user_id,
                            reaction_date=datetime.datetime.utcnow())
        # todo db连接是否需要长期保持?
        DAO_utils.mongo_insert_reactions(reaction)
        # else:
        #     print 'user did not agree to auth'
        return redirect(redirect_url)
    except Exception, e:
        print e
        return make_response(json.dumps({'code': 1, 'msg': str(e)}), 500)


@app.route('/api/v1/article', methods=['POST'])
def post_article():
    """
    发表新文章后，首先调用该函数进行文章分析和数据库存入
    :return:
    """
    try:
        jdata = json.loads(request.data)
        media_id = jdata['media_id']
        items = jdata['items']
        update_time = jdata['update_time']
        # admin_id = jdata['admin_id']
        for item in items:
            article_title = item['article_title']
            article_content = item['article_content']
            article_thumb_id = item['article_thumb_id']
            article_id = hashlib.md5(media_id + article_thumb_id).hexdigest()
            article_url = item['article_url']
            article_post_user = item['article_post_user']
            article_post_date = update_time
            a_topiclist = tagging_utils.passage_second_level_classify(article_content)
            atags = {}
            for topic in a_topiclist:
                atags[topic['topic_tag']] = topic['topic_prob']
            article = Article(a_id=article_id, a_title=article_title, post_user=article_post_user,
                              post_date=article_post_date, a_tags=atags, a_url=article_url, a_content=article_content)
            DAO_utils.mongo_insert_article(article)
        resp = make_response(json.dumps({'code': 0, 'msg': 'success'}), 200)
    except KeyError, ke:
        print ke
        resp = make_response(
            json.dumps({'code': 103,
                        'msg': 'request key error, details=%s' % str(ke)}), 500)
    except DAO_utils.DAOException, de:
        print de
        resp = make_response(json.dumps({'code': 0, 'msg': 'success,article already existed'}), 200)
    except Exception, e:
        print e
        resp = make_response(json.dumps({'code': 1, 'msg': str(e)}), 500)
    return resp


@app.route('/api/v1/article/<article_id>')
def get_article(article_id):
    """
    根据文章id获取文章信息
    :return:
    """
    try:
        # params = request.args
        # article_id = params['article_id']
        inst_article = DAO_utils.mongo_get_article(article_id)
        json_article = inst_article.get_json_object()
        resp = make_response(json.dumps({'code': 0, 'article': json_article}), 200)
    except KeyError, ke:
        print ke
        resp = make_response(
            json.dumps({'code': 103,
                        'msg': 'request key error, details=%s' % str(ke)}), 500)
    except Exception, e:
        print e
        resp = make_response(json.dumps({'code': 1, 'msg': str(e)}), 500)
    return resp


@app.route('/api/v1/user', methods=['POST'])
def new_user():
    """
    每当有用户新关注后，回调该函数，将用户信息存入
    :return:
    """
    try:
        jdata = json.loads(request.data)
        user_id = jdata['openid']
        wechat_user = WechatUser(user_id)
        DAO_utils.mongo_insert_user(wechat_user)
        resp = make_response(json.dumps({'code': 0, 'msg': 'success'}), 200)
    except KeyError, ke:
        print ke
        resp = make_response(
            json.dumps({'code': 103,
                        'msg': 'request key error, details=%s' % str(ke)}), 500)
    except Exception, e:
        print e
        resp = make_response(json.dumps({'code': 1, 'msg': str(e)}), 500)
    return resp


@app.route('/api/v1/tagging', methods=['GET'])
def start_user_tagging():
    """
    根据所有未标注过的交互记录，对用户进行tagging
    :return:
    """
    try:
        reaction_list = DAO_utils.mongo_get_reactions()
        reaction_type_weight = DAO_utils.mongo_get_reaction_type_weight()
        a_u_map = DAO_utils.mongo_get_a_u_tagmap()
        count = tagging_utils.user_tagging_by_reactionlist(reaction_list, reaction_type_weight, a_u_map)
        return json.dumps({'code': 0, 'msg': 'handled %s reactions' % count})
    except Exception, e:
        return json.dumps({'code': 1, 'msg': 'unknown error, details = %s' % str(e)})


@app.route('/api/v1/openid', methods=['POST'])
def get_openidlist_by_tag():
    try:
        req_data = json.loads(request.data)
        taglist = req_data['tagList']
        openid_list = DAO_utils.mongo_get_openid_by_tags(taglist)
        return json.dumps({'code': 0, 'openid_list': openid_list})
    except Exception, e:
        print e
        return json.dumps({'code': 1, 'msg': 'unknown error, details = %s' % str(e)})


@app.route('/api/v1/taglist', methods=['GET'])
def get_all_taglist():
    try:
        taglist = DAO_utils.mongo_get_all_taglist()
        return json.dumps({'code': 0, 'tagList': taglist}, ensure_ascii=False)

    except Exception, e:
        print e
        return json.dumps({'code': 1, 'msg': 'unknown error, details = %s' % str(e)})


@app.route('/api/v1/analyse_article', methods=['POST'])
def analyzse_article():
    """
    抽离文章分析接口
    :return:
    """
    req_data = json.loads(request.data)
    content_list = req_data.get('article_content')
    article_content = req_data.get('article_content')
    result = wenzhi_utils.wenzhi_analysis(article_content)
    # topic_list = tagging_utils.passage_second_level_classify(web_content)
    tag_result = []
    if result['code'] == 0:
        for class_item in result['classes']:
            class_type = class_item['class']
            class_prob = class_item['conf']
            tag_result.append({'tag': class_type, 'prob': class_prob})
    return json.dumps({'code': 0, 'tag_result': tag_result}, ensure_ascii=False)
    # return resp


@app.route('/api/v1/analyse_url', methods=['POST'])
def analyse_artivle_url():
    try:
        req_data = json.loads(request.data)
        url = req_data['url']
        # user_id = req_data['openid']
        result = wenzhi_utils.wenzhi_analyse_url(url)
        # topic_list = tagging_utils.passage_second_level_classify(web_content)
        tag_result = []
        if result['code'] == 0:
            for class_item in result['classes']:
                class_type = class_item['class']
                class_prob = class_item['conf']
                tag_result.append({'tag': class_type, 'prob': class_prob})
        return json.dumps({'code': 0, 'tag_result': tag_result}, ensure_ascii=False)
    except Exception, e:
        print e
        # print result
        return json.dumps({'code': 1, 'msg': 'unknown error, details = %s' % str(e)})


@app.route('/api/v1/tagging/article_id')
def tagging_by_article():
    try:
        req_data = json.loads(request.data)
        user_id = req_data['user_id']
        admin_id = req_data['admin_id']
        article_id = req_data['article_id']
        reaction_type_weight = DAO_utils.mongo_get_reaction_type_weight()

        result = tagging_utils.user_tagging_by_article(article_id=article_id, admin_id=admin_id, user_id=user_id,
                                                       reaction_type_weight=reaction_type_weight)
        resp = make_response(json.dumps({'code': 0, 'result': result}), 200)
    except Exception, e:
        print e
        resp = make_response(json.dumps({'code': 1, 'msg': 'unknown error, details = %s' % str(e)}), 400)
    return resp


@app.route('/api/v1/tagging/article_url', methods=['POST'])
def tagging_by_url():
    try:
        req_data = json.loads(request.data)
        user_id = req_data['user_id']
        admin_id = req_data['admin_id']
        article_url = req_data['article_url']
        reaction_type_weight = DAO_utils.mongo_get_reaction_type_weight()

        result = tagging_utils.user_tagging_by_url(article_url=article_url, admin_id=admin_id, user_id=user_id,
                                                   reaction_type_weight=reaction_type_weight)
        resp = make_response(json.dumps({'code': 0, 'result': result}), 200)
    except Exception, e:
        print e
        resp = make_response(json.dumps({'code': 1, 'msg': 'unknown error, details = %s' % str(e)}), 400)
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, debug=True)
