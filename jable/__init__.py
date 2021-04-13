from bs4 import BeautifulSoup as bs
import requests
from download_ts import M3u8
# import download_ts
# from binascii import hexlify, unhexlify
from utils import log, save
from config import get_headers
from multiprocessing import Process
import threading

# def m3u8_decode(dirname, filename):
#     [key, iv] = read_key_and_iv(dirname)
#     log('len(key), len(iv)', len(key), len(iv))
#     new_filename = '0' + filename
#     cmd = f'openssl aes-128-cbc -d -in {filename} -out {new_filename} -nosalt -iv {iv[2:]} -K {key}'
#     cmd = f'cd {dirname} && {cmd} '
#     # log(cmd)
#     os.system(cmd)
#     os.remove(f'{dirname}/{filename}')


# 1. 下载m3u8文件
# 2. 传递m3u8文件 下载所有ts文件, 合并所有ts文件
class JableTv():
    def __init__(self, page_url):
        self.page_url = page_url
        # self.dirname = create_dir(page_url)
        # self.filename = self.dirname

    def get_m3u8_file_link(self):
        response = requests.get(
            self.page_url, headers=get_headers(), timeout=2)
        print('response', response)
        soup = bs(response.text, 'lxml')
        r = soup.find_all('link', href=True)
        link = r[-1]['href']
        return link

    def download_all_ts(self, m3u8_link):
        m = M3u8(self.page_url, m3u8_link)
        m.download_all_ts()


def jable_tv_download(page_url):
    jable = JableTv(page_url)
    m3u8_link = jable.get_m3u8_file_link()
    print('m3u8_link', m3u8_link)
    jable.download_all_ts(m3u8_link)


# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
# socket.socket = socks.socksocket
if __name__ == "__main__":
    page_url = "https://jable.tv/videos/pred-277/"
    # https://qvv21d.cdnlab.live/hls/6pdPcy_q-RtSzqUODKjUZQ/1604199843/11000/11142/11142.m3u8
    # p = Process(target=jable_tv_download, args=(page_url,))
    # p.start()
    t = threading.Thread(
        target=jable_tv_download, args=(page_url,))
    # 启动线程
    t.start()

