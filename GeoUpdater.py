import requests,shutil,os,json,time
from multiprocessing.pool import ThreadPool
from tqdm import tqdm

def download_file(filename):
    url = base_url+filename
    response = requests.get(url, proxies=proxies, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(filename+'.download', 'wb') as file:
        for data in response.iter_content(total_size//100):
            file.write(data)
            progress_bar.update(1)
    file.close()

def init_proxies():
    with open('config/groups/nekobox.json') as file:
        port = str(json.load(file)["inbound_socks_port"])
        file.close()
    proxies = {'http': 'http://127.0.0.1:'+port, 'https': 'http://127.0.0.1:'+port}
    return proxies

def check_version():
    response = requests.get(base_url, proxies=proxies)
    return response.url.split('/')[-1]

base_url = 'https://github.com/lyc8503/sing-box-rules/releases/latest/download/'
proxies=init_proxies()
if os.path.exists('geosite.db.download'):
    os.remove('geosite.db.download')
if os.path.exists('geoip.db.download'):
    os.remove('geoip.db.download')
try:
    print('正在获取最新Geo文件：'+check_version())
    progress_bar = tqdm(total=202,bar_format='{percentage:3.0f}%|{bar}|')
    with ThreadPool(2) as pool:
        pool.map(download_file, ['geosite.db', 'geoip.db'])
    progress_bar.close()
except Exception as Error:
    print('更新失败，请检查报错信息。')
    print('报错信息：'+str(Error))
    input('回车即可关闭本窗口。')
    exit()
if os.path.exists('geosite.db'):
    os.remove('geosite.db')
if os.path.exists('geoip.db'):
    os.remove('geoip.db')
shutil.move('geosite.db.download','geosite.db')
shutil.move('geoip.db.download','geoip.db')
print('更新完毕，请重启Nekoray以应用更新。')
time.sleep(1)
exit()