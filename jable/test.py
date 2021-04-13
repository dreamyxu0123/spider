fail_urls = [
    'https://ddgo12.cdnlab.live/hls/WCluG568z6iYrlg57oeGVA/1608364016/10000/10314/103140.ts']

url = 'https://ddgo12.cdnlab.live/hls/WCluG568z6iYrlg57oeGVA/1608364016/10000/10314/103140.ts'
if url in fail_urls:
    fail_urls.remove(url)

print(fail_urls)
