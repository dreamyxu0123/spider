import json
import sys
import threading

from utils import load, log

sys.path.extend(load('./env_path.json'))

from flask import Flask, jsonify, request

from hpjav.hpjav import hpjav_download, hpjav_download_mp4
from jable import jable_tv_download
from javhdporn import javhdporn
from ts_download import Download_M3U8

# print(sys.path)

app = Flask(__name__)  # 变量app是Flask的一个实例并且必须传入一个参数，__name__对应的值是__main，即当前的py文件的文件名作为Flask的程序名称，这个也可以自定义，比如，取，'MY_ZHH_APP'                          #__name__是固定写法，主要是方便flask框架去寻找资源 ，也方便flask插件出现错误时，去定位问题


@app.route('/hpjav_download', methods=['POST'])
def hpjav():  # 视图函数
    data = request.get_data()
    json_data = json.loads(data.decode('utf-8'))
    url = json_data.get('url')
    page_url = json_data.get('page_url')
    filename = json_data.get('filename') + '.mp4'
    video_type = json_data.get('video_type')
    host_type = json_data.get('host_type')

    if host_type == 'javhdporn':
        t = threading.Thread(target=javhdporn, args=(page_url, url))
        t.start()
        return "javhdporn"

    if video_type == 'mp4':
        mb = hpjav_download_mp4(url, filename)
    elif video_type == 'm3u8':
        # Download_M3U8.start(url, filename)
        t = threading.Thread(target=javhdporn, args=(page_url, url))
        t.start()
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
    return 'Hello World'


@app.route('/', methods=['POST'])
def hello_world():
    data = request.get_data()
    json_data = json.loads(data.decode('utf-8'))
    print('json_data', json_data)
    video_link = json_data['video_link']
    page_url = json_data['page_url']
    video_type = json_data['video_type']
    if video_type == 'mp4':
        mb = hpjav_download_mp4(video_link, page_url=page_url)
    # print(url, filename)
    elif video_type == 'm3u8':
        hpjav_download(video_link, 'filename')
    return 'Hello World'


@app.route('/javhdporn', methods=['POST'])
def javhdporn_api():
    data = request.get_data()
    json_data = json.loads(data.decode('utf-8'))
    page_url = json_data['href']
    videoLink = json_data['videoLink']

    t = threading.Thread(target=javhdporn, args=(page_url, videoLink))
    t.start()
    return "javhdporn"


@app.route('/')
def hello():
    return 'Hello World'


if __name__ == '__main__':
    app.run(
        debug=True
    )  # 启动这个应用服务器，并开启debug,才能定位问题
