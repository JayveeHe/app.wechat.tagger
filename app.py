# coding=utf-8
import json
import os
import re

from flask import Flask, request, make_response, render_template
from flask.ext.cors import cross_origin
import requests
import sys
import jieba.analyse
import numpy as np
from sklearn.externals import joblib
from passage_classifier.vector_builder import VectorBuilder
from passage_classifier.web_content_extractor import get_content

reload(sys)
sys.setdefaultencoding('utf-8')

project_path = os.path.dirname(__file__)
sys.path.append(project_path)
app = Flask(__name__)
vb = VectorBuilder()
nbclf = joblib.load('%s/data/models/nbclf.model' % project_path)


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
    resp = make_response(
        json.dumps({'code': 0, 'class': class_dict[classify_result], 'keyword': keyword_result}, ensure_ascii=False),
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
    resp = make_response(
        json.dumps({'code': 0, 'class': class_dict[classify_result], 'keyword': keyword_result}, ensure_ascii=False),
        200)
    return resp


if __name__ == '__main__':
    app.run(port=3333, debug=True)
