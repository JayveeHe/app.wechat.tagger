# coding: utf-8


from wsgiref import simple_server
import leancloud

from app import app
from cloud import engine

# APP_ID = os.environ.get('LC_APP_ID', 'pelj09whtpy6ipcob33o4zw4jl6850et2be2f1g331lcn7vr')  # your app id
# MASTER_KEY = os.environ.get('LC_APP_MASTER_KEY', '')  # your app master key
APPID = 'Yfl74NQtHo3tASR8XKEx2WnQ'
APPKEY = 'WRJrx7LH7d8xnPbWcuwNRAK9'
# APPID_TEST = '7g0ohycwpqq2fgynqyy71a48rfnae7d1wggo7kftr31cvymq'
# APPKEY_TEST = 'ftnxzrabkm8n3bpakiw24ye5okork58qpby9h1yxdhjn2pzb'
# leancloud.init('7g0ohycwpqq2fgynqyy71a48rfnae7d1wggo7kftr31cvymq',
#                'ftnxzrabkm8n3bpakiw24ye5okork58qpby9h1yxdhjn2pzb')
leancloud.init(APPID, APPKEY)
# leancloud.init(APPID_TEST, APPKEY_TEST)

application = engine

if __name__ == '__main__':
    # 只在本地开发环境执行的代码
    app.debug = True
    server = simple_server.make_server('localhost', 3000, application)
    server.serve_forever()
