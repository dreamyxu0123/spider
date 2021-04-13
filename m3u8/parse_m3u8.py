from Crypto.Cipher import AES
from binascii import hexlify, unhexlify
import m3u8


def read_iv(m3u8_file):
    m3u8_obj = m3u8.load(m3u8_file)
    iv = ''
    for key in m3u8_obj.keys:
        if key:  # First one could be None
            iv = key.iv
    return iv


def read_m3u8():
    m3u8_obj = m3u8.load(r'm3u8.m3u8')
    uri_list = []
    for key in m3u8_obj.keys:
        if key:  # First one could be None
            print('key.uri', key.uri)
            print('key.method', key.method)
            print('key.iv', key.iv)

    # ki = read_key_and_iv(dirname)
    # if ki == None:
    #     with open(f'{dirname}/{filename}', "wb") as file:
    #         file.write(content)
    # else:
    #     [key, iv] = ki
    #     # key = unhexlify('c8a9ded8b41a7daa57e224968934f86f')
    #     # iv = unhexlify('962ec00083ed2a46d7c1c8a8271157c3')
    #     key = bytes.fromhex(key)
    #     iv = bytes.fromhex(iv)


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


def decode(filename, key, iv):
    with open(filename, 'rb') as content:
        decipher = AES.new(key, AES.MODE_CBC, iv)
        # pt = decipher.decrypt(content)
        # with open(f'decode_{filename}', "wb") as file:
        #     file.write(pt)


def get_key_content():
    pass


if __name__ == "__main__":
    key = read_hex_file('key.key')
    iv = read_iv('m3u8.m3u8')
    print('len(key)', len(key))
    # decode('1.ts', key, iv)
    # print(key, iv)
