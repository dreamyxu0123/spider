import m3u8

# playlist = m3u8.load('video/fc2ppv_1675277-a.mp4/m3u8.m3u8')
# print(playlist.dumps())
m3u8_obj = m3u8.load('video/161940.mp4/m3u8.m3u8')

for seg in m3u8_obj.segments:
    # uri = url_prefix + '/' + seg.uri
    # print(seg.uri, seg.byterange)
    pass

byte = ['1', '2']
byte = map(lambda x: int(x), byte)
print(list(byte))
