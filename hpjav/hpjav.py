import threading
import sys
import requests
import time
import os
from urllib.parse import urlparse
import math
import socket
import socks
# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
# socket.socket = socks.socksocket


headers = {
    # 'Host': "www714.o0-2.com",
    # 'Connection': 'keep-alive',
    # 'Connection': 'closer',
    # 'Pragma': 'no-cache',
    # 'Cache-Control': 'no-cache',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    # 'Accept': '*/*',
    # 'Sec-Fetch-Site': 'cross-site',
    # 'Sec-Fetch-Mode': 'no-cors',
    # 'Sec-Fetch-Dest': 'video',
    # 'Accept-Language': "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,zh-HK;q=0.6,ja;q=0.5,ko;q=0.4",
    # 'Referer': 'https://asianclub.tv/v/4-63qhzz88pxmed',
    # 'Range': 'bytes=0-',
    # 'accept': '*/*',
    # 'accept-encoding': 'identity;q=1, *;q=0',
    # 'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,zh-HK;q=0.6,ja;q=0.5,ko;q=0.4',
    # 'range': 'bytes=0-',
    'referer': 'https://vidoza.net/',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-fetch-dest': 'video',
    # 'sec-fetch-mode': 'no-cors',
    # 'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
}
proxies = {
    'https': 'https://127.0.0.1:1080',
    'http': 'http://127.0.0.1:1080'
}
progress = {}


class MulThreadDownload(threading.Thread):
    def __init__(self, url, startpos, endpos, f):
        super(MulThreadDownload, self).__init__()
        self.url = url
        self.startpos = startpos
        self.endpos = endpos
        self.fd = f

    def download(self):
        key = "start thread:%s at %s" % (self.getName(), time.time())
        value = key
        progress[key] = value
        print(key)
        # headers = {"Range": "bytes=%s-%s" % (self.startpos, self.endpos)}
        headers['Range'] = "bytes=%s-%s" % (self.startpos, self.endpos)
        response = requests.get(self.url, headers=headers)
        status_code = response.status_code
        print('status_code', status_code)
        if status_code != 206:
            self.download()
        # response.text 是将get获取的byte类型数据自动编码，是str类型， response.content是原始的byte类型数据
        # 所以下面是直接write(response.content)
        self.fd.seek(self.startpos)
        self.fd.write(response.content)
        self.fd.flush()
        print("stop thread:%s at %s" % (self.getName(), time.time()))
        progress.pop(key)
        print(len(progress.keys()))

    def run(self):
        self.download()


def log(*args, **kwargs):
    format = r'%Y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = '[' + time.strftime(format, value) + ']'
    log_file = os.path.join(os.path.dirname(__file__), r'log.txt')
    print(*args, **kwargs)
    with open(log_file, 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def hpjav_download_mp4(url, filename):
    # 获取文件的大小和文件名
    # url = "http://a238.static-file.com:8080/video/9fd38b603e9a14b9c8ea97634daed9c3/5fb3b3bf/cache/5503649e7b49a781e7ab9d00a2dd40cb.mp4?s=128"

    # filename = url.split('/')[-1]
    filesize = int(requests.head(
        url,).headers['Content-Length'])

    # 线程数
    thread_number = 2
    # 信号量，同时只允许3个线程运行
    threading.BoundedSemaphore(thread_number)
    # 默认3线程现在，也可以通过传参的方式设置线程数
    mtd_list = []
    start = 0
    end = 0
    path = 'video/' + filename
    # 请空并生成文件
    tempf = open(path, 'w')
    tempf.close()
    # rb+ ，二进制打开，可任意位置读写
    step = math.floor(filesize / thread_number)
    mb = filesize / 1024.0 / 1024.0

    with open(path, 'rb+') as f:
        fileno = f.fileno()
        # 如果文件大小为11字节，那就是获取文件0-10的位置的数据。如果end = 10，说明数据已经获取完了。
        while end < filesize:
            start = end
            end = end + step
            if end > filesize:
                end = filesize
            print('start', start, 'end', end)
            # print("start:%s, end:%s"%(start,end))
            # 复制文件句柄
            dup = os.dup(fileno)
            # print(dup)
            # 打开文件
            fd = os.fdopen(dup, 'rb+', -1)
            # print(fd)
            t = MulThreadDownload(url, start, end, fd)
            t.start()
            mtd_list.append(t)
        print(mb, 'MB')
        for i in mtd_list:
            i.join()
    return mb
def hpjav_download(url, filename):
    cmd = f'N_m3u8DL-CLI_v2.9.5.exe {url}'
    # print(cmd)
    os.system(cmd)

if __name__ == "__main__":
    url = 'https://lising-39.cdnamz.me/videos/ohdpsinm1t818e7biwrx3hrzfa.mp4'
    hpjav_download_mp4(url, 'filename.mp4')
