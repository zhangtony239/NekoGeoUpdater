import requests,shutil,os,json,time
from tqdm import tqdm

def download_file(filename):
    url = base_url+filename
    response = requests.get(url, proxies=proxies)
    with open(filename+'.download', 'wb') as file:
        file.write(response.content)
    bar.update(1)

def init_proxies():
    with open('config/groups/nekobox.json') as file:
        port = str(json.load(file)["inbound_socks_port"])
        file.close()
    proxies = {'http': 'http://127.0.0.1:'+port, 'https': 'http://127.0.0.1:'+port}
    return proxies

suffix,base_url = '.db','https://github.com/lyc8503/sing-box-rules/releases/latest/download/'
proxies=init_proxies()
print('正在获取最新Geo文件...')
if os.path.exists('geosite'+suffix+'.download'):
    os.remove('geosite'+suffix+'.download')
if os.path.exists('geoip'+suffix+'.download'):
    os.remove('geoip'+suffix+'.download')
bar = tqdm(total=2)
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