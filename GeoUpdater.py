import requests,shutil,os,json,time
from tqdm import tqdm

def download_file(filename):
    url = base_url+filename
    response = requests.get(url, proxies=proxies, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(filename+'.download', 'wb') as file:
        with tqdm(total=total_size, unit='iB', unit_scale=True, desc=filename) as progress_bar:
            for data in response.iter_content(1024):
                file.write(data)
                progress_bar.update(len(data))

def core_check():
    with open('config/groups/coreType','r') as file:
        core_type = file.read()
        file.close()
    if core_type == '1':
        print('当前核心：sing-box')
        return '.db','https://github.com/lyc8503/sing-box-rules/releases/latest/download/'
    elif core_type == '0':
        print('当前核心：Xray')
        return '.dat','https://github.com/Loyalsoldier/v2ray-rules-dat/releases/latest/download/'
    
def init_proxies():
    with open('config/groups/nekobox.json') as file:
        port = str(json.load(file)["inbound_socks_port"])
        file.close()
    proxies = {'http': 'http://127.0.0.1:'+port, 'https': 'http://127.0.0.1:'+port}
    return proxies

(suffix,base_url) = core_check()
proxies=init_proxies()
print('正在获取最新Geo文件...')
if os.path.exists('geosite'+suffix+'.download'):
    os.remove('geosite'+suffix+'.download')
if os.path.exists('geoip'+suffix+'.download'):
    os.remove('geoip'+suffix+'.download')
try:
    geosite = download_file('geosite'+suffix)
    geoip = download_file('geoip'+suffix)
except Exception as Error:
    print('更新失败，请检查报错信息。')
    print('报错信息：'+str(Error))
    input('回车即可关闭本窗口。')
    exit()
if os.path.exists('geosite'+suffix):
    os.remove('geosite'+suffix)
if os.path.exists('geoip'+suffix):
    os.remove('geoip'+suffix)
shutil.move('geosite'+suffix+'.download','geosite'+suffix)
shutil.move('geoip'+suffix+'.download','geoip'+suffix)
print('更新完毕，请重启Nekoray以应用更新。')
time.sleep(1)
exit()