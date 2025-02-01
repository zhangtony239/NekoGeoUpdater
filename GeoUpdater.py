print(f'正在获取最新版本信息...\r',end='')

import os,json,time
from concurrent.futures import ThreadPoolExecutor as ThreadPool
try:
    import requests
except ImportError:
    os.system('pip install requests')
try:
    from tqdm import tqdm
except ImportError:
    os.system('pip install tqdm')

def GetProxyCfg():
    with open('config/groups/nekobox.json') as file:
        port = str(json.load(file)["inbound_socks_port"])
    proxies = {'http': f'http://127.0.0.1:{port}', 'https': f'http://127.0.0.1:{port}'}
    return proxies

def GetGeoVer(session):
    response = session.get(base_url)
    return response.url.split('/')[-1]

def StartDownload(filename):
    response = session.get(base_url+filename, stream=True)
    with open(filename+'.download', 'wb') as file:
        for chunk in tqdm(response.iter_content(chunk_size=1024),total=int(response.headers['content-length'])//1024,unit='KB',desc=filename,leave=False):
            file.write(chunk)
        file.flush()
        file.close()
        tqdm.write(filename+': Done.')

base_url = 'https://github.com/lyc8503/sing-box-rules/releases/latest/download/'
proxies = GetProxyCfg()
session = requests.Session()
session.proxies = proxies

try:
    print('正在获取最新Geo文件：'+str(GetGeoVer(session)))
    if os.path.exists('geosite.db.download'):
        os.remove('geosite.db.download')
    if os.path.exists('geoip.db.download'):
        os.remove('geoip.db.download')
    with ThreadPool(max_workers=2) as executor:
        executor.map(StartDownload, ['geosite.db', 'geoip.db'])
        time.sleep(0.1)

except requests.exceptions.RequestException as e:
    print('更新失败，请检查网络连接和代理设置。')
    print(f'网络请求出现错误：{e}')
    input('按回车键退出程序。')
    exit()
except Exception as e:
    print('更新失败，请检查报错信息。')
    print(f'发生其它错误：{e}')
    input('按回车键退出程序。')
    exit()

if os.path.exists('geosite.db'):
    os.remove('geosite.db')
os.replace('geosite.db.download', 'geosite.db')
if os.path.exists('geoip.db'):
    os.remove('geoip.db')
os.replace('geoip.db.download', 'geoip.db')

print('更新完毕，请重启Nekobox以应用更新。')
time.sleep(1)
exit()