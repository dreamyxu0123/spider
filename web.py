import json
import sys
from utils import load
sys.path.extend(load('./env_path.json'))
from jable import jable_tv_download
from hpjav.hpjav import hpjav_download_mp4
from flask import request, Flask, jsonify
from ts_download import Download_M3U8


# print(sys.path)

app = Flask(__name__)  # 变量app是Flask的一个实例并且必须传入一个参数，__name__对应的值是__main，即当前的py文件的文件名作为Flask的程序名称，这个也可以自定义，比如，取，'MY_ZHH_APP'                          #__name__是固定写法，主要是方便flask框架去寻找资源 ，也方便flask插件出现错误时，去定位问题


@app.route('/hpjav_download', methods=['POST'])
def hpjav():  # 视图函数
    data = request.get_data()
    json_data = json.loads(data.decode('utf-8'))
    url = json_data.get('url')
    filename = json_data.get('filename') + '.mp4'
    video_type = json_data.get('video_type')
    if video_type == 'mp4':
        mb = hpjav_download_mp4(url, filename)
    # print(url, filename)
    elif video_type == 'm3u8':
        Download_M3U8.start(url, filename)
    # print('mb', mb, type(mb))
    # Download_M3U8.start(url, filename)
    else:
        return 'None Video Type'
    return filename + '''start download  url: ''' + url


@app.route('/jable_tv_download', methods=['POST'])
def jable_tv():  # 视图函数
    data = request.get_data()
    json_data = json.loads(data.decode('utf-8'))
    url = json_data.get('url')
    print('url', url)
    jable_tv_download(url)
    return 'Hello World'  # response，最终给浏览器返回的内容


@app.route('/', methods=['POST'])
def hello_world():  # 视图函数
    return 'Hello World'  # response，最终给浏览器返回的内容


if __name__ == '__main__':
    app.run(
        debug=True
    )  # 启动这个应用服务器，并开启debug,才能定位问题
