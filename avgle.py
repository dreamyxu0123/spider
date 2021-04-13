import requests
import time
import threading
import os
from if_file import if_file, get_filepath

# {"url":"https:\/\/r3---sn-hk85l709.qooqlevideo.com\/videoplayback?sparams=clen,dur,ei,expire,gir,hcs,id,ip,ipbits,ipbypass,itag,lmt,mime,mm,mn,ms,mv,pl,ratebypass,requiressl,shardbypass,source,upn&ip=144.202.81.80&clen=976331746&id=HpzibXD6agYGKYFJuEHN1ym83SnBiFlYTSzze0tsG5Tuvy&source=youtube&sub=r3---sn-hk85l709&upn=mmyAwhkP0V1&ei=45edwWcUk4usO5CVfCzy_i&itag=18&ks=zHcg7wRqimkd_UmPOAKshw&pl=20&lmt=1504871426768256&expire=1577447426&ipbits=0&dur=9470.03&gir=yes&mime=video\/mp4&key=&requiressl=yes&beids=[7753970]&ratebypass=yes&signature=52C205BC2136F806A3E0F4168F0F9FCB3CB44DBD.4C8531AAC19EA2E322DEDECDE7CD0739C4887B63&redirect_counter=1&req_id=QoM1svOU2ACmvzyq&cms_redirect=yes&hcs=yes&s2=t\/1577447426\/QwxmmOPp3bAXAfZFNhtErw&s3=aHR0cHM6Ly9nb29xbGV2aWRlby54eXovcGxheWJhY2svZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6STFOaUo5LmV5SmxlSEJwY21WelFYUWlPakUxTnpRNU1qTTNOakVzSW5WelpYSkpVQ0k2SWpFME5DNHlNREl1T0RFdU9EQWlMQ0p3Y205NGVXbHVaMVZTVEVOeWVYQjBTbk52YmlJNkludGNJbU4wWENJNlhDSk9kSGxEYWsxNlExQlhUVWRYTmpJcmIzQnNRMjV0Y2pKVFJEaDVkMGxQTVcxRlRHcFlSRlF5V0ZCMldVczRjWGRPVWxCeGVuRkdPV1ZHT1RWMVRHUmtkRmxHWjIxWGFYSnVNSHBhVkdJek9FOWtaSGQ2Wm5GMVFXRlphMkZ3WEZ4Y0wwbE5WVGxUUjNOWWJWRkJRbE5sVFRjMVkweHNPRUZEVFZCRldIUXJjVmRPWlUwMGIydFBNRnBMZVVzeVJtVlBRMFpIVVZOVFpXdEtTV0YwWVVKclYyOXdNRWh2Y1VOemVGaGNYRnd2Vkd4ck1HWnpLM0E1YlRVNFZYQXJkWGhjWEZ3dmJtVkdRM1ZxY1VsMFRuUXpYRnhjTHpWUFpWQnVTRk5yVERkUU5HTm5QVDFjSWl4Y0ltbDJYQ0k2WENKaE9UWm1ZVEJtWlRBME5EVTBaV0ZsWWpFM09XWTBNV0kyWkRreE4yUmpPVndpTEZ3aWMxd2lPbHdpTkRJeE5qUXlORGhpWkRnME1USmlaVndpZlNKOS5CUXNreWhJUXJNYnhwcTQwcGtlOUJlMU1lc2RZQkhLQUxMNTRvWnY4ZWw4&ipbypass=yes&mm=31&mn=sn-i3co-i3b6&ms=au&mt=1504871426&mv=m&shardbypass=yes&aid=81892"}
headers = {
    # 'Host': 'cdn.qooqlevideo.com',
    # 'Connection': 'keep-alive',
    # 'Origin': 'https://avgle.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    # 'Accept': '*/*',
    # 'Sec-Fetch-Site': 'cross-site',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Referer': 'https://avgle.com/embed/f9f294b46c351b834a16',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,zh-HK;q=0.6,ja;q=0.5',
}

lock = threading.Lock()

# 限制线程的最大数量为 个
sem = threading.Semaphore(150)
file_dict = {}


def save(file_path, data):
    print("save file", file_path)
    with open(file_path, 'wb') as f:
        f.write(data)


def save_video(file_name, data):
    file = "video/" + file_name
    save(file, data)


def log(*args, **kwargs):
    format = r'%Y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = '[' + time.strftime(format, value) + ']'
    log_file = os.path.join(os.path.dirname(__file__), r'log.txt')
    print(*args, **kwargs)
    with open(log_file, 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def datetime():
    dt = time.time()
    return dt


def create_dir(url):
    url_list = url.split('/')
    dirname = url_list[-2]
    path = "video/" + dirname
    if not os.path.exists(path):
        os.makedirs(path)


def parse_url(number, url):

    s = url
    s = s[0:-14] + "seg-{}-v1-a1.ts"
    s = s.format(number)
    url = s
    create_dir(url)
    return url


def task(url):
    for i in range(1, 10):
        u = parse_url(i, url)
        filepath = get_filepath(u, i)
        if if_file(i, u):
            print('pass filepath', filepath)
        else:
            file_dict[filepath] = u


# def task(urls):
#     global file_dict
#     for i, url in enumerate(urls):
#         create_dir(url)
#         filepath = get_filepath(url, i+1)
#         if if_file(i+1, url):
#             print('pass filepath', filepath)
#         else:
#             file_dict[filepath] = url
#     # log(file_dict)


def taskpool(urls):
    '''
    urls dict 
    '''
    ts = []
    for filename, url in urls.items():
        # 创建线程01，不指定参数
        t = threading.Thread(target=request_get, args=(url, filename))
        # 启动线程01
        ts.append(t)
        t.start()

    for t in ts:
        t.join()


def request_get(url, filename):
    with sem:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            status_code = response.status_code
            print("response status_code", status_code,
                  'filename', filename, "url", url)
            if status_code == 200:
                save_video(filename, response.content)
            elif status_code == 404:
                # file_dict.pop(filename)
                print(404)
                pass
            else:
                pass
        except Exception:
            print('error')
            pass


if __name__ == "__main__":
    # url = "https://cdn.qooqlevideo.com/key=2SkAe0AjR-oc-k-TNbFUbw,end=1585567394,limit=2/referer=force,.avgle.com/data=1585567394/media=hlsA/383469.mp4/seg-1-v1-a1.ts"
    # task(url)
    # taskpool()
    # https://sk222p.cdnlab.live/hls/CSBeidG1AurbDSTGDYZQTw/1603890455/1000/1577/15770.ts
    # https://sk222p.cdnlab.live/hls/CSBeidG1AurbDSTGDYZQTw/1603890455/1000/1577/15772595.ts
    urls = {}
    for i in range(15772, 15775):
        filename = str(i) + '.ts'
        url = 'https://sk222p.cdnlab.live/hls/CSBeidG1AurbDSTGDYZQTw/1603890455/1000/1577/' + filename
        urls[filename] = url
    taskpool(urls)

# https://ip219408796.cdn.qooqlevideo.com/key=lckPJkPjswf7WyYFJAhnoQ,s=,end=1604186580,limit=2/data=1604186580/state=X53dmhEY/referer=force,.avgle.com/reftag=56109644/media=hlsA/2/177/6/226530216.mp4/seg-1-v1-a1.ts
# https://cdn.qooqlevideo.com/key=NaY+qEKptjCc8e-zF7KfzA,end=1604186174,limit=2/ip=154.17.24.19/referer=force,.avgle.com/data=1604186174/media=hlsA/444653.mp4/seg-1-v1-a1.ts

# https://cdn.qooqlevideo.com/key=H9zXGGX2HI7kwdaX31hlZg,end=1604187429,limit=2/ip=154.17.24.19/referer=force,.avgle.com/data=1604187429/media=hlsA/442803.mp4/seg-1-v1-a1.ts
# https://cdn.qooqlevideo.com/key=vj7Gfa3N+aQISP5vZZdwqw,end=1604185660,limit=2/ip=154.17.24.19/referer=force,.avgle.com/data=1604185660/media=hlsA/442803.mp4/seg-1-v1-a1.ts
# b7b411ab-6286-4c82-bc55-31a9a0828c03
