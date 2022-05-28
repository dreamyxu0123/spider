import _thread
from hex import read_hex_file
from binascii import hexlify, unhexlify

from Crypto.Cipher import AES
import requests
from config import get_headers
from utils import log, save
import m3u8
import os
from threading import Lock
import threading
import shutil
import socket
# import socks
# ss
# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
# socket.socket = socks.socksocket

total = 0
lo = Lock()
maxthreads = 20
sema = threading.Semaphore(value=maxthreads)
completion_number = 0


def file_list(dirname):
    for root, dirs, files in os.walk(dirname):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        return files


def print_percent():
    global lo
    with lo:
        global completion_number
        global total
        # log('completion_number, total', completion_number, total)
        completion_number += 1
        percent = 'percent: {:.0%}'.format(completion_number / total)
        # Progress: 366 of 1538
        print(
            f'\r Progress: {str(completion_number)} of {str(total)} ',
            percent,
            end='',
            flush=True)


class M3u8():
    def __init__(self, page_url, m3u8_link):
        self.m3u8_link = m3u8_link
        self.page_url = page_url
        self.dir = self.create_dir(page_url)
        m3u8_file_name = 'm3u8.m3u8'
        self.m3u8_file_path = self.dir + '/' + m3u8_file_name
        url_list = self.m3u8_link.split('/')
        url_list.pop(-1)
        print('url_list', url_list)
        self.url_prefix = '/'.join(url_list)
        print('self.url_prefix', self.url_prefix)

    def create_dir(self, page_url):
        url_list = page_url.split('/')
        dirname = url_list[-2]
        path = 'videos/' + dirname
        if not os.path.exists(path):
            os.makedirs(path)
        print('path', path)
        return path

    def download_all_ts(self):
        self.download_m3u8_file()
        self.download_m3u8_key()
        urls = self.m3u8_url_list()
        global total
        total += len(urls)
        ThreadDownload.thread_download(urls, self.dir)
        fs = file_list(self.dir)
        if len(fs) == len(urls) + 2:
            # log(f' {self.dir} file count ', len(fs))
            url_list = self.page_url.split('/')
            filename = url_list[-2]
            merge_m3u8(self.dir, f'{filename}.ts', 'videos')
        else:
            self.download_all_ts()

    def download_m3u8_file(self):
        # 请空并生成文件
        temp = open(self.m3u8_file_path, 'w')
        temp.close()
        response = requests.get(
            self.m3u8_link, headers=get_headers(), timeout=10)
        status_code = response.status_code
        log('self.m3u8_link', self.m3u8_link)
        # log('download_m3u8_file status_code', status_code)
        if response.status_code == 200:
            # log('download_m3u8_file content', response.content)
            save(self.m3u8_file_path, response.content)
        else:
            raise Exception("not 200")

    # def set_url_prefix(self, link):
    #     url_list = link.split('/')
    #     url_list.pop(-1)
    #     self.url_prefix = '/'.join(url_list)
    #     log(url_list)
    #     log(link)
    #     log(self.url_prefix)

    # def m3u8_link(self):
    #     response = requests.get(self.page_url, headers=get_headers(), timeout=10)
    #     log('response', response)
    #     soup = bs(response.text, 'lxml')
    #     r = soup.find_all('link', href=True)
    #     link = r[-1]['href']
    #     self.set_url_prefix(link)
    #     self.link = link

    def download_m3u8_key(self):
        m3u8_obj = m3u8.load(self.m3u8_file_path)
        for key in m3u8_obj.keys:
            if key:  # First one could be None
                link = self.url_prefix + '/' + key.uri
                key_filename = key.uri[0:-3] + '.key'
                response = requests.get(
                    link, headers=get_headers(), timeout=10)
                path = self.dir + '/' + key_filename
                log('download_m3u8_key path', path)
                save(path, response.content)

    def m3u8_url_list(self):
        m3u8_obj = m3u8.load(self.m3u8_file_path)
        uri_list = []
        for seg in m3u8_obj.segments:
            uri = self.url_prefix + '/' + seg.uri
            uri_list.append(uri)
        return uri_list


class ThreadDownload():
    @staticmethod
    def thread_download(urls, dirname):
        threads = []
        l = len(urls)
        for i, url in enumerate(urls):
            # 创建线程01，不指定参数
            # urls.remove(url)

            if ThreadDownload.check_file(url, dirname) == False:
                t = threading.Thread(
                    target=ThreadDownload.download, args=(url, dirname))
                # 启动线程
                threads.append(t)
                t.start()
            else:
                print_percent()
        for t in threads:
            t.join()
        log('threads done join')

    @staticmethod
    def check_file(url, dirname):
        filename = url.split('/')[-1]
        files = file_list(dirname)
        # log('filename', filename, filename in files)
        return filename in files

    @staticmethod
    def download(url, dirname):
        try:
            sema.acquire()
            response = requests.get(url, headers=get_headers(), timeout=10)
            status_code = response.status_code
            log('status_code', status_code)
            if status_code == 200:
                filename = url.split('/')[-1]
                path = f'{dirname}/{filename}'
                # print('save', path)
                decrypt_save(dirname, filename, response.content)
                # m3u8_decode(dirname, filename)
                print_percent()
            else:
                raise Exception(f"not 200 status_code {status_code}")
            sema.release()
        except Exception as e:
            log(' fail_url', e, url)
            sema.release()


def decrypt_save(dirname, filename, content):
    ki = read_key_and_iv(dirname)
    path = f'{dirname}/{filename}'
    if ki == None:
        with open(path, "wb") as file:
            file.write(content)
    else:
        [key, iv] = ki
        # key = unhexlify('c8a9ded8b41a7daa57e224968934f86f')
        # iv = unhexlify('962ec00083ed2a46d7c1c8a8271157c3')


        # AES-128 加密后的 key文件应该是16字节
        key = bytes.fromhex(key)
        iv = bytes.fromhex(iv)

        # log('len key', key, len(key))
        # log('len iv', iv, len(iv))

        decipher = AES.new(key, AES.MODE_CBC, iv)
        pt = decipher.decrypt(content)
        # print('save', path)
        with open(path, "wb") as file:
            file.write(pt)


def read_hex_file(file):
    with open(file, 'rb') as f:
        data = f.read()
        return hexlify(data).decode("utf-8")


def read_key_and_iv(dirname):
    m3u8_path = dirname + '/' + 'm3u8.m3u8'
    m3u8_obj = m3u8.load(m3u8_path)

    uri = ''
    iv = ''
    for key in m3u8_obj.keys:
        if key:  # First one could be None
            # print(key.uri)
            # print(key.method)
            # print(key.iv)
            uri = key.uri
            iv = key.iv
        else:
            return None
    key_file = uri[0:-3] + '.key'
    key_file = dirname + '/' + key_file

    key_bytes = read_hex_file(key_file)
    # [key, iv]
    # log('str(key_bytes), iv[2:]', str(key_bytes), iv[2:])
    return [key_bytes, iv[2:]]


# F1B91AC5D0A96BD009D40368EA9CAEED1256D8AEE432820C29972DAFEF3F16C5
# f1b91ac5d0a96bd009d40368ea9caeed1256d8aee432820c29972dafef3f16c5

def merge_m3u8(dirname, filename, sava_path):

    ts_filenames = []
    # Parse playlist for filenames with ending .ts and put them into the list ts_filenames
    m3u8 = f'{dirname}/m3u8.m3u8'
    with open(m3u8, 'r') as playlist:
        # ts_filenames = [line.rstrip() for line in playlist
        #                 if line.rstrip().endswith('.ts')]
        for line in playlist:
            if line.rstrip().endswith('.ts'):
                f = f'{dirname}/{line}'.rstrip()
                ts_filenames.append(f)

    # print('ts_filenames', len(ts_filenames), ts_filenames[0])
    # open one ts_file from the list after another and append them to merged.ts
    sava_path = f'{sava_path}/{filename}'
    print('merge m3u8 sava path', sava_path)
    with open(sava_path, 'wb') as merged:
        for ts_file in ts_filenames:
            with open(ts_file, 'rb') as mergefile:
                shutil.copyfileobj(mergefile, merged)
