import threading
import requests
import time
from pathlib import Path
import re
from bs4 import BeautifulSoup as bs
from lxml import etree

from utils import retry
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
}


@retry()
def request_get(url) -> str:
    response = requests.get(url, headers=headers)
    # https://regex101.com/r/HfrDzu/1
    redirMatch = re.findall(
        'window\.location\.href\s*=\s*\"([^\"]+)\"', response.text)
    # print(redirMatch)
    if len(redirMatch) > 0:
        u = 'https://www.ghdzck.com'+redirMatch[0]
        response = requests.get(u, headers=headers)
    return response.text


def downloads(urls, real_title):
    for i, url in enumerate(urls):
        img1 = f'imgs/{real_title}/img_{i+1}_{len(urls)}.jpg'
        img2 = f'imgs/all/{real_title}_img_{i+1}_{len(urls)}.jpg'

        if Path(img1).exists() == True:
            continue
        # print('download title:', img2, 'url',
        #       url, 'count', len(urls))

        thread = threading.Thread(target=download, args=(url, img1, img2))
        thread.start()


maxthreads = 5
sema = threading.Semaphore(value=maxthreads)
@retry()
def download(url, img1, img2):
    with sema:
        r0 = requests.get(url, headers=headers)
        Path(img1).parent.mkdir(parents=True, exist_ok=True)
        with open(img1, 'wb') as f:
            f.write(r0.content)
        Path(img2).parent.mkdir(parents=True, exist_ok=True)
        with open(img2, 'wb') as f:
            f.write(r0.content)


def imgs_page(url, real_title):
    text = request_get(url)
    tree = etree.HTML(text)
    img_urls = tree.xpath('/html/body/div[2]/div/div[1]/div/div/*/img/@src')
    title = tree.xpath('/html/body/div[2]/div/div[1]/div[1]/h1/text()')
    title = title[0]
    downloads(img_urls, real_title)


def page_urls(page_url):
    
    text = request_get(page_url)
    tree = etree.HTML(text)
    urls = tree.xpath(
        '/html/body/div[2]/div[2]/ul//a[contains(@class, "img-box")]/@href')
    titles = tree.xpath(
        '/html/body/div[2]/div[2]/ul//a[contains(@class, "img-box")]/@title')
    imgs_counts = tree.xpath(
        '/html/body/div[2]/div[2]/ul/*/div/a/em/text()')
    for index, title in enumerate(titles):
        # real_title = f"{str(count).zfill(5)}_{title}"
        imgs_count = imgs_counts[index].replace('P', '')
        # img = f'imgs/all/{title}_img_{imgs_count}.jpg'
        img = f'imgs/all/{title}_img_{imgs_count}_{imgs_count}.jpg'

        if Path(img).exists() == False:
            print('download title:', img, 'url',
                  urls[index], 'count', imgs_count)
            thread = threading.Thread(
                target=imgs_page, args=(urls[index], title))
            thread.start()
            time.sleep(20)


if __name__ == '__main__':
    # html test
    # url = 'https://www.ghdzck.com/post/26805.html?btwaf=96211918'
    # html(url)
    for i in range(1, 158):
        page_url = f'https://www.ghdzck.com/img.html?type=hot&page={i}'
        page_urls(page_url)
