import os


def get_filename(number):
    filename = str(number) + ".ts"
    filename = filename.zfill(7)
    return filename


def get_filepath(url, number):
    filename = get_filename(number)

    url_list = url.split('/')
    dirname = url_list[-2]
    path = "video/" + dirname
    if not os.path.exists(path):
        os.makedirs(path)
    return dirname + "/" + filename


def file_list(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        return files


# 判断文件是否已存在
def if_file(number, url):
    filename = get_filename(number)
    # print('filename', filename)
    url_list = url.split('/')
    dirname = url_list[-2]
    file_dir = "./video" + '/' + dirname
    # print('file_dir', file_dir)
    files = file_list(file_dir)
    # print('files', files)
    return filename in files


if __name__ == "__main__":
    l = []
    # number = 1
    for number in range(1, 1451 + 1):
        url = "https://ip174215975.cdn.qooqlevideo.com/key=iU1UmQbcZN7fEe47bb17lA,s=,end=1581452582,limit=2/data=1581452582/state=Wfip/referer=force,.avgle.com/reftag=56109644/media=hlsA/ssd6/177/9/87667459.mp4/seg-{}-v1-a1.ts".format(
            number)
        if if_file(number, url) == False:
            l.append(number)
    print('l', l)
