import threading
import m3u8
import time
import random
import os
import requests
from hpjav.hpjav import hpjav_download1

from hpjav import hpjav_download1
headers = {
    # 'Host': 'f94dakfbkg.nincontent.com',
    # 'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    # 'Accept': '*/*',
    # 'Origin': 'https://ninjastream.to',
    # 'Sec-Fetch-Site': 'cross-site',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Referer': 'https://ninjastream.to/watch/Ng9Qnz8GqQVKb',
    # 'Accept-Encoding': 'identity',
    # 'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,zh-HK;q=0.6,ja;q=0.5,ko;q=0.4',

}


def get_filename():
    print(time.strftime('%Y%m%d', time.localtime()))  # 时间格式化


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save(file_path, data):
    # print("save file", file_path)
    with open(file_path, 'wb') as f:
        f.write(data)


def download_m3u8_file(path, m3u8_url):
    # 请空并生成文件
    temp = open(path, 'w')
    temp.close()
    r = requests.get(
        m3u8_url, headers=headers, timeout=10)
    if r.status_code == 200:
        save(path, r.content)
    else:
        raise Exception("not 200")


def m3u8_file_list(m3u8_path):
    m3u8_obj = m3u8.load(m3u8_path)
    temp_list = []
    ts_list = []
    for seg in m3u8_obj.segments:
        # uri = url_prefix + '/' + seg.uri
        temp_list.append(seg.uri)
    ts_list.append(temp_list[0])
    t = temp_list[0]
    for uri in temp_list:
        if t != uri:
            ts_list.append(uri)
            t = uri
    return ts_list


maxthreads = 2
sema = threading.Semaphore(value=maxthreads)


def file_list(dirname):
    for root, dirs, files in os.walk(dirname):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        return files


def check_file(filename, dir):
    files = file_list(dir)
    # log('filename', filename, filename in files)
    return filename in files


def download_ts(ts_file, path, url_prefix):
    sema.acquire()
    url = f'{url_prefix}/{ts_file}'
    file_path = f'{path}/{ts_file}'
    if check_file(ts_file, path) == False:
        hpjav_download1(url, file_path)
        # r = requests.get(
        #     url, headers=headers, stream=True)
        # print('r.status_code', r.status_code)
        # if r.status_code == 200:
        #     save(file_path, r.content)
        #     sema.release()
        # else:
        #     sema.release()
        #     raise Exception("not 200")


def download_all_ts(ts_list, path, url_prefix):
    print(len(ts_list))
    for ts_file in ts_list:
        # print('ts_file', ts_file)
        download_ts(ts_file, path, url_prefix)
        # t = threading.Thread(
        #     target=download_ts, args=(ts_file, path, url_prefix))
        # t.start()


class Download_M3U8():
    @staticmethod
    def start(m3u8_url, dirname=''):
        if dirname == '':
            dirname = random.randint(1000, 9999)
        path = "video/" + dirname
        create_dir(path)
        download_m3u8_file(path + '/m3u8.m3u8', m3u8_url)
        t = m3u8_url.split('/')[:-1]
        url_prefix = '/'.join(t)

        ts_list = m3u8_file_list(path + '/m3u8.m3u8')
        download_all_ts(ts_list, path, url_prefix)


    # 1. 获取所有ts url
    # 2. 多线程下载
if __name__ == '__main__':
    get_filename()
