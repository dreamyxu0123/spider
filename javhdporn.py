'''
Author: yanxl
Date: 2021-04-13 15:45:12
LastEditors: yanxl
LastEditTime: 2021-12-28 19:24:02
Description: 
'''
import shutil
import threading
import urllib.parse
import uuid
from hashlib import md5
from pathlib import Path
from turtle import st

import requests
from sklearn.manifold import MDS

import m3u8
from utils import log, retry, save, save_json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,zh-HK;q=0.6,ja;q=0.5,ko;q=0.4',
}

thread_max_num = threading.Semaphore(30)


def download(path, url):
    with thread_max_num:
        try:
            log('start', path)
            response = requests.get(url, headers=headers, timeout=10)
            status_code = response.status_code
            print('status_code', status_code)
            # log('download_m3u8_file status_code', status_code)
            if status_code == 200:
                # log('download_m3u8_file content', response.content)
                save(path, response.content)
            log('end', path)

        except Exception as e:
            log('fail url', url)


def create_metadata(base_path, url_list):
    raw = []
    json_path = Path(base_path, 'raw.json')
    Path(base_path, "Part").mkdir(parents=True, exist_ok=True)
    for url in url_list:
        urlparse = urllib.parse.urlparse(url)
        filename = urlparse.path.split('/').pop()
        # path = base_path + filename
        path = Path(base_path, "Part", filename)
        o = {
            "path": str(path),
            "url": url,
        }
        raw.append(o)
    save_json(raw, json_path)
    return raw


def start_downloads(metadatas):
    threads = []

    for metadata in metadatas:
        path = metadata['path']
        url = metadata['url']
        if Path(path).is_file() == False:
            t = threading.Thread(target=download, args=(path, url))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()


def check_files(metadatas):
    for metadata in metadatas:
        path = metadata['path']
        url = metadata['url']
        file = Path(path)
        if file.is_file() == False:
            return False
            # t = threading.Thread(target=download, args=(path, url))
            # t.start()


def download_m3u8(base_path, m3u8_url):
    # master m3u8
    m3u8_path = Path(base_path, 'master.m3u8')
    response = requests.get(m3u8_url, headers=headers, timeout=10)
    status_code = response.status_code
    log('download m3u8 status code', status_code, m3u8_path)
    if status_code == 200:
        save(m3u8_path, response.content)

    # ts file list m3u8
    master_m3u8 = m3u8.load(str(m3u8_path))
    raw_m3u8_path = Path(base_path, 'raw.m3u8')
    index_m3u8_url = master_m3u8.data["playlists"].pop()['uri']
    # index_m3u8_url = master_m3u8.data["playlists"]
    response = requests.get(index_m3u8_url, headers=headers, timeout=10)
    if status_code == 200:
        save(raw_m3u8_path, response.content)

    return raw_m3u8_path


def get_base_path(dir, url):
    hash = md5(url.encode('utf-8')).hexdigest()
    path = Path(dir, str(hash))
    path.mkdir(parents=True, exist_ok=True)
    return {"path": str(path), "hash": hash}


def merge_m3u8(video_path, metadatas):
    log('merge m3u8 sava path', video_path)
    with open(video_path, 'wb') as merged:
        for metadata in metadatas:
            path = metadata['path']

            with open(path, 'rb') as mergefile:
                shutil.copyfileobj(mergefile, merged)


def javhdporn(url, m3u8_url):
    base_dir = 'G:/code/spider/video'
    p = get_base_path(base_dir, url)
    base_path = p['path']
    hash = p['hash']

    raw_m3u8_path = download_m3u8(base_path, m3u8_url)
    log('base_path', base_path)

    l = m3u8.load(str(raw_m3u8_path))
    url_list = []
    for seg in l.segments:
        uri = seg.uri
        url_list.append(uri)

    metadatas = create_metadata(str(base_path), url_list)
    start_downloads(metadatas)

    while check_files(metadatas) == False:
        log("retrying...")
        start_downloads(metadatas)

    video = hash + ".mp4"
    video_path = Path(base_dir, video)
    merge_m3u8(str(video_path), metadatas)
    log("ending...")


if __name__ == '__main__':
    url = 'https://www2.javhdporn.net/video/fc2-ppv-1585077/'
    m3u8_url = 'https://delivery439.akamai-cdn-content.com/hls2/01/00529/xf3pxtyusa2m_,n,h,.urlset/master.m3u8?t=18Pf_BSfU5eRTJa3Bp4qbZ0C7cFGPgCLwNgodYspKEU&s=1653652681&e=21600&f=2645728&srv=sto093&client=218.102.244.227'
    javhdporn(url, m3u8_url)
