import functools
import json
import os
import time


def log(*args, **kwargs):
    format = r'%Y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = '[' + time.strftime(format, value) + ']'
    log_file = os.path.join(os.path.dirname(__file__), r'log.txt')
    print(dt, *args, **kwargs)
    with open(log_file, 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def save(file_path, data):
    # print("save file", file_path)
    with open(file_path, 'wb') as f:
        f.write(data)


def save_json(data, path):
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    """
    本函数从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)


def retry(delay=0, times=2):
    def outer_wrapper(function):
        @functools.wraps(function)
        def inner_wrapper(*args, **kwargs):
            final_excep = None
            for counter in range(times):
                if counter > 0:
                    time.sleep(delay)
                final_excep = None
                try:
                    value = function(*args, **kwargs)
                    return value
                except Exception as e:
                    print('retry counter', counter+1)
                    final_excep = e
                    pass  # or log it
            if final_excep is not None:
                raise final_excep
        return inner_wrapper
    return outer_wrapper
