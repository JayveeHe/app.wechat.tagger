# coding: utf-8
import json
import datetime
from leancloud import Engine
import leancloud
import logentries
import time

from app import app

engine = Engine(app)

import logging

# logger = logging.getLogger('logentries')
# logger.setLevel(logging.INFO)
# # Note if you have set up the logentries handler in Django, the following line is not necessary
# lh = logentries.LogentriesHandler('c5351cb9-9d9c-4691-93db-8f11482d581f')
# fm = logging.Formatter('%(asctime)s : %(levelname)s, %(message)s',
#                        '%a %b %d %H:%M:%S %Y')
# lh.setFormatter(fm)
# logger.addHandler(lh)

# APPID = 'llir9y4gtqys053tivb4tildoan0hgj87kdd0j6ib5naye5e'
# APPKEY = 'h5roibgrbtux2luasq1o9xwr218jebbsyuthv9ho4lced9rv'
#
# APPID_TEST = '7g0ohycwpqq2fgynqyy71a48rfnae7d1wggo7kftr31cvymq'
# APPKEY_TEST = 'ftnxzrabkm8n3bpakiw24ye5okork58qpby9h1yxdhjn2pzb'
#
#
# @engine.define
# def hello(**params):
#     if 'name' in params:
#         return 'Hello, {}!'.format(params['name'])
#     else:
#         return 'Hello, LeanCloud!'
#
#
# # add hook log by jayvee
#
# @engine.before_save('Config')  # Config 为需要 hook 的 class 的名称
# def before_config_save(config):
#     """
#     log when add some config. @jayvee_he
#     :param config:
#     :return:
#     """
#     leancloud.init(APPID, APPKEY)
#     # leancloud.init(APPID_TEST, APPKEY_TEST)
#     logger.info('before_save')
#     Config_log = leancloud.Object.extend('Config_log')
#     diff_time = datetime.datetime.fromtimestamp(time.time())
#
#     name = config.get('name')
#     value = config.get('value')
#     if not name:
#         logger.error(str(leancloud.LeanEngineError(message='No Name!')))
#     else:
#         try:
#             config.set('name', name)
#             config.set('value', value)
#             config_log = Config_log()
#             config_log.set('name', name)
#             config_log.set('value', value)
#             config_log.save()
#             logger.info('[Add]diff_time=%s, name=%s, value=%s' % (diff_time, name, json.dumps(value)))
#         except leancloud.LeanCloudError, lce:
#             logger.error(lce)
#             logger.info('[Add]diff_time=%s, name=%s, value=%s' % (diff_time, name, json.dumps(value)))
#             config.set('name', name)
#             config.set('value', value)
#             config_log = Config_log()
#             config_log.set('name', name)
#             config_log.set('value', value)
#             config_log.save()
#
#
# @engine.after_update('Config')
# def after_article_update(config):
#     """
#     log change when update Config   @jayvee_he
#     [caution!!!]
#     should create a slave class (eg. Config_log) to store the last value of the changes,
#     cuz there is no before_update method
#     :param config:
#     :return:
#     """
#     leancloud.init(APPID, APPKEY)
#     # leancloud.init(APPID_TEST, APPKEY_TEST)
#     logger.info('after_update')
#     name = config.get('name')
#     value = config.get('value')
#     diff_time = datetime.datetime.fromtimestamp(time.time())
#     Config_log = leancloud.Object.extend('Config_log')
#     try:
#         clq = leancloud.Query(Config_log)
#         clq.equal_to('name', name)
#         find_result = clq.find()
#         if len(find_result) > 0:
#             last_result = find_result[0]
#             last_value = last_result.attributes['value']
#             diff_result = diff_utils.getDiff(json.dumps(last_value, sort_keys=True, ensure_ascii=False),
#                                              json.dumps(value, sort_keys=True, ensure_ascii=False))
#             logger.info('[Update]diff_time=%s, name=%s, diff_count=%s' % (diff_time, name, len(diff_result)))
#             for r in diff_result:
#                 logger.info('[Update]diff_time=%s, name=%s, diff=%s' % (diff_time, name, r))
#             last_result.set('value', value)
#             last_result.save()
#         else:
#             logger.info('[Add]diff_time=%s, name=%s, value=%s' % (diff_time, name, json.dumps(value)))
#             config.set('name', name)
#             config.set('value', value)
#             Config_log = leancloud.Object.extend('Config_log')
#             config_log = Config_log()
#             config_log.set('name', name)
#             config_log.set('value', value)
#             config_log.save()
#     except leancloud.LeanCloudError, lce:
#         logger.error(lce)
#         logger.info('[Add]diff_time=%s, name=%s, value=%s' % (diff_time, name, json.dumps(value)))
#         config.set('name', name)
#         config.set('value', value)
#         Config_log = leancloud.Object.extend('Config_log')
#         config_log = Config_log()
#         config_log.set('name', name)
#         config_log.set('value', value)
#         config_log.save()
#
#
# @engine.after_delete('Config')
# def after_album_delete(config):
#     leancloud.init(APPID, APPKEY)
#     # leancloud.init(APPID_TEST, APPKEY_TEST)
#     logger.info('after_update')
#     name = config.get('name')
#     value = config.get('value')
#     diff_time = datetime.datetime.fromtimestamp(time.time())
#     Config_log = leancloud.Object.extend('Config_log')
#     try:
#         clq = leancloud.Query(Config_log)
#         clq.equal_to('name', name)
#         find_result = clq.find()
#         if len(find_result) > 0:
#             find_result[0].destroy()
#             # logger.info('[Delete]diff_time=%s, name=%s, value=%s' % (diff_time, name, json.dumps(value)))
#     except leancloud.LeanCloudError, lce:
#         logger.error(lce)
#         logger.warn('[Delete]diff_time=%s, %s not in Config_log' % (diff_time, name))
#     finally:
#         logger.info('[Delete]diff_time=%s, name=%s, value=%s' % (diff_time, name, json.dumps(value)))
