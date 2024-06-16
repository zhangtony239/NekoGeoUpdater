import requests,os
from tqdm import tqdm

def get_latest(base_url):
    response = requests.get(base_url+'latest/')
    return response.url

def getfile(url):
    response = requests.get(url)
    if response.status_code == 200:
        file_content = response.content
        return file_content
    else:
        print('HTTP ERROR:'+str(response.status_code))
        return None

def savefile(filename):
    with open(filename,'wb') as file:
        file.write(getfile(base_url+filename))
        file.close()
    qbar.update(1)

def core_check(lock):
    if lock == '1':
        print('核心锁定：sing-box')
        return '.db','https://github.com/lyc8503/sing-box-rules/releases/'
    elif lock == '0':
        print('核心锁定：Xray')
        return '.dat','https://github.com/Loyalsoldier/v2ray-rules-dat/releases/'
    else:
        with open('config/groups/coreType','r') as file:
            core_type = file.read()
            file.close()
        if core_type == '1':
            print('当前核心：sing-box')
            return '.db','https://github.com/lyc8503/sing-box-rules/releases/'
        elif core_type == '0':
            print('当前核心：Xray')
            return '.dat','https://github.com/Loyalsoldier/v2ray-rules-dat/releases/'
        
(suffix,base_url) = core_check(lock='1') #非官方版必须设置：锁sing-box，设为1；锁Xray，设为0。官方版留空自动同步Nekoray内的内核设置。
input('即将开始更新Geo文件，请确保网络连接正常，回车即可继续。')
print('Geo文件更新开始，请勿中断程序……')
if os.path.exists('geosite'+suffix):
    os.remove('geosite'+suffix)
if os.path.exists('geoip'+suffix):
    os.remove('geoip'+suffix)
latest_ver = get_latest(base_url).split('/')[-1:][0]
base_url = base_url + 'download/' + latest_ver + '/'
print('已获取最新版本：'+str(latest_ver))
qbar = tqdm(total=2)
geosite = savefile('geosite'+suffix)
geoip = savefile('geoip'+suffix)
input('更新完毕！回车即可关闭本窗口。')
exit()