import requests,shutil,os
from tqdm import tqdm

def download_file(filename):
    url = base_url+filename
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(filename+'.download', 'wb') as file:
        with tqdm(total=total_size, unit='iB', unit_scale=True, desc=filename) as progress_bar:
            for data in response.iter_content(1024):
                file.write(data)
                progress_bar.update(len(data))

def core_check(lock):
    if lock == '1':
        print('核心锁定：sing-box')
        return '.db','https://github.com/lyc8503/sing-box-rules/releases/latest/download/'
    elif lock == '0':
        print('核心锁定：Xray')
        return '.dat','https://github.com/Loyalsoldier/v2ray-rules-dat/releases/latest/download/'
    else:
        with open('config/groups/coreType','r') as file:
            core_type = file.read()
            file.close()
        if core_type == '1':
            print('当前核心：sing-box')
            return '.db','https://github.com/lyc8503/sing-box-rules/releases/latest/download/'
        elif core_type == '0':
            print('当前核心：Xray')
            return '.dat','https://github.com/Loyalsoldier/v2ray-rules-dat/releases/latest/download/'

(suffix,base_url) = core_check(lock='') #非官方版必须设置：锁sing-box，设为1；锁Xray，设为0。官方版留空自动同步Nekoray内的内核设置。
print('正在获取最新Geo文件...')
try:
    geosite = download_file('geosite'+suffix)
    geoip = download_file('geoip'+suffix)
except:
    input('更新失败，请检查网络连接或稍后再试。')
    exit()
if os.path.exists('geosite'+suffix):
    os.remove('geosite'+suffix)
if os.path.exists('geoip'+suffix):
    os.remove('geoip'+suffix)
shutil.move('geosite'+suffix+'.download','geosite'+suffix)
shutil.move('geoip'+suffix+'.download','geoip'+suffix)
input('更新完毕！回车即可关闭本窗口。')
exit()