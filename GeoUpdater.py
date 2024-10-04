print(f'正在获取最新版本信息...\r',end='')

import os
import json
import time
from concurrent.futures import ThreadPoolExecutor
try:
    import requests
except ImportError:
    os.system('pip install requests')
try:
    from tqdm import tqdm
except ImportError:
    os.system('pip install tqdm')

def init_proxies():
    """初始化代理设置，从配置文件中读取代理端口。"""
    with open('config/groups/nekobox.json') as file:
        port = str(json.load(file)["inbound_socks_port"])
    proxies = {'http': f'http://127.0.0.1:{port}', 'https': f'http://127.0.0.1:{port}'}
    return proxies

def check_version(session):
    """获取最新版本号。"""
    response = session.get(base_url)
    return response.url.split('/')[-1]

def download_file(args):
    """下载指定的文件，并显示下载进度。"""
    filename, position = args
    url = base_url + filename
    response = session.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))+1
    chunk_size = 1024 * 1024

    with open(f'{filename}.download', 'wb') as file, \
         tqdm(total=total_size, unit='B', unit_scale=True, desc=filename, dynamic_ncols=True, position=position, leave=True) as pbar:
        for data in response.iter_content(chunk_size):
            file.write(data)
            pbar.update(len(data))

# 初始化基本参数和会话
base_url = 'https://github.com/lyc8503/sing-box-rules/releases/latest/download/'
proxies = init_proxies()
session = requests.Session()
session.proxies = proxies

try:
    latest_version = check_version(session)
    print(f'正在获取最新Geo文件：{latest_version}')
    
    files_with_positions = [('geosite.db', 0), ('geoip.db', 1)]

    # 删除已有的下载文件
    for filename, _ in files_with_positions:
        if os.path.exists(f'{filename}.download'):
            os.remove(f'{filename}.download')

    # 使用线程池并行下载文件
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(download_file, files_with_positions)

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

# 替换旧的文件
for filename, _ in files_with_positions:
    if os.path.exists(filename):
        os.remove(filename)
    os.replace(f'{filename}.download', filename)

print('更新完毕，请重启Nekoray以应用更新。')
time.sleep(1)
exit()