let str = `import threading
import sys
import requests
import time
import os
from urllib.parse import urlparse
import math
from threading import Lock
lock = Lock()

headers = {
    # 'Host': "www714.o0-2.com",
    # 'Connection': 'keep-alive',
    # 'Connection': 'closer',
    # 'Pragma': 'no-cache',
    # 'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    # 'Accept': '*/*',
    # 'Sec-Fetch-Site': 'cross-site',
    # 'Sec-Fetch-Mode': 'no-cors',
    # 'Sec-Fetch-Dest': 'video',
    # 'Accept-Language': "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,zh-HK;q=0.6,ja;q=0.5,ko;q=0.4",
    # 'Referer': 'https://asianclub.tv/v/4-63qhzz88pxmed',
    # 'Range': 'bytes=0-',
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
        # self.saveFile(str(self.startpos), response.content)
        # with open(self.getName()+'.pdf', 'wb+') as f:
        #     f.write(response.content)
        # f.close()

    def saveFile(filename, data):
        with open(filename, 'rb+') as f:
            f.write(data)

    def run(self):
        self.download()


if __name__ == "__main__":
    # url = sys.argv[1]
    # 获取文件的大小和文件名
    url = {{}}
    result = urlparse(url)

    Host = result.netloc
    # headers['Host'] = Host
    # filename = url.split('/')[-1].split('?')[0]
    filename = url.split('/')[-1]

    # filename = 'video/test.mp4'
    filesize = int(requests.head(url).headers['Content-Length'])

    # 线程数
    thread_number = 8
    # 信号量，同时只允许3个线程运行
    threading.BoundedSemaphore(thread_number)
    # 默认3线程现在，也可以通过传参的方式设置线程数
    mtd_list = []
    start = 0
    end = 0

    # 请空并生成文件
    tempf = open(filename, 'w')
    tempf.close()
    # rb+ ，二进制打开，可任意位置读写
    step = math.floor(filesize / thread_number)

    with open(filename, 'rb+') as f:
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
        print(filesize / 1024 / 1024, 'MB')
        for i in mtd_list:
            i.join()

    print('filename', filename)
`
let s = str.replace('{{}}', 'filename')
console.log(s)