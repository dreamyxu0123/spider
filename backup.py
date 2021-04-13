import copy
from hpjav.hpjav import hpjav_download1
import threading
import m3u8
import time
import random
import os
import requests

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


def m3u8_file_list1(path, url_prefix):
    m3u8_path = path + '/m3u8.m3u8'
    m3u8_obj = m3u8.load(m3u8_path)
    ts_list = []
    for i, seg in enumerate(m3u8_obj.segments):
        o = {}
        uri = url_prefix + '/' + seg.uri
        byte = seg.byterange.split('@')
        byte = list(map(lambda x: int(x), byte))
        # print('uri, byterange', uri, byterange)
        Range = f'bytes={min(byte)}-{max(byte)}'
        header = copy.deepcopy(headers)
        header['Range'] = Range
        o[uri] = header
        o['ts_file'] = str(i).zfill(5) + '.ts'
        ts_list.append(o)
    # print('ts_list', ts_list[0])
    # print('ts_list', ts_list[1])
    return ts_list


maxthreads = 20
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


# def download_ts(ts_file, path, url_prefix):
#     sema.acquire()
#     url = f'{url_prefix}/{ts_file}'
#     file_path = f'{path}/{ts_file}'
#     try:
#         if check_file(ts_file, path) == False:
#             print('url', url)
#             # hpjav_download1(url, file_path)
#             r = requests.get(
#                 url, headers=headers, stream=True)
#             print('r.status_code', r.status_code)
#             if r.status_code == 200:
#                 save(file_path, r.content)
#                 sema.release()
#             else:
#                 sema.release()
#                 raise Exception("not 200")

#     except Exception:
#         print('error')
#         download_ts(ts_file, path, url_prefix)


def download_ts(ts_file, path, url, header):
    file_path = f'{path}/{ts_file}'
    try:
        sema.acquire()

        if check_file(ts_file, path) == False:
            print('url', url)
            # hpjav_download1(url, file_path)
            r = requests.get(
                url, headers=header, stream=True)
            print('r.status_code', r.status_code)
            if r.status_code == 200:
                save(file_path, r.content)
            else:
                raise Exception("not 200")
        sema.release()

    except Exception:
        sema.release()
        time.sleep(1)
        print('error')
        download_ts(ts_file, path, url, header)


def download_all_ts(ts_list, path):
    for ts in ts_list:
        for key, value in ts.items():
            print(key, value)
            # download_ts(ts['ts_file'], path, key, value)
            t = threading.Thread(
                target=download_ts, args=(ts['ts_file'], path, key, value))
            t.start()


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

        ts_list = m3u8_file_list1(path, url_prefix)
        download_all_ts(ts_list, path)
        # print('len(ts_list)', len(ts_list))
        # for ts in ts_list:
        #     for key, value in ts.items():
        #         # print(key, value)
        #         download_ts(ts['ts_file'], path, key, value)
        # download_all_ts(ts_list, path, url_prefix)

    # 1. 获取所有ts url
    # 2. 多线程下载
if __name__ == '__main__':
    m3u8_url = 'https://kqcpz7z9wy8cwpxnqbhi.nincontent.com/K21nVnFLSWx1MjhJUVFwSmlUTHlkYTVrOTV2bDFSd3ZmcFhVc1p6Zk1KZ2U4ZVQwV1dwTHA3WmZQUmVWZko1UzMxMS9WMHF4bFg5anZOaStiVVIwRUZRWEhOTlk4RXVuYnNoaUk5TStDWUlFV0s0YmF5OTcrWVprNUhuWmtHRkx6MGQ4SFpxYmhGZ0pFOUNRUUlCUkdnPT0=/0Cb-bkJCstpygcntbRT3iw/2_720p.m3u8'
    dirname = '161940.mp4'
    # get_filename()
    Download_M3U8.start(m3u8_url, dirname)

# d=copy.deepcopy(alist)
