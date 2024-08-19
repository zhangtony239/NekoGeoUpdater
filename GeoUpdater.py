import requests,shutil,os,json,time,asyncio
from tqdm import tqdm

async def download_file(filename):
    url = base_url+filename
    response = requests.get(url, proxies=proxies, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(filename+'.download', 'wb') as file:
        for data in response.iter_content(total_size//100):
            file.write(data)
            progress_bar.update(1)
    file.close()
    progress_bar.close()

async def downloader():
    await asyncio.gather(
        download_file('geosite'+suffix),
        download_file('geoip'+suffix)
    )

def init_proxies():
    with open('config/groups/nekobox.json') as file:
        port = str(json.load(file)["inbound_socks_port"])
        file.close()
    proxies = {'http': 'http://127.0.0.1:'+port, 'https': 'http://127.0.0.1:'+port}
    return proxies

def check_version():
    response = requests.get(base_url, proxies=proxies)
    return response.url.split('/')[-1]

suffix,base_url = '.db','https://github.com/lyc8503/sing-box-rules/releases/latest/download/'
proxies=init_proxies()
if os.path.exists('geosite'+suffix+'.download'):
    os.remove('geosite'+suffix+'.download')
if os.path.exists('geoip'+suffix+'.download'):
    os.remove('geoip'+suffix+'.download')
try:
    print('正在获取最新Geo文件：'+check_version())
    progress_bar = tqdm(total=101,bar_format='{percentage:3.0f}%|{bar}|')
    asyncio.run(downloader())
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