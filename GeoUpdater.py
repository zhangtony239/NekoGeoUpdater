import requests,os
from tqdm import tqdm

def get_latest():
    response = requests.get('https://github.com/lyc8503/sing-box-rules/releases/latest/')
    return response.url

def getfile(url):
    response = requests.get(url)
    if response.status_code == 200:
        file_content = response.content
        return file_content
    else:
        print('HTTP ERROR:'+str(response.status_code))
        return None

def savefile(file_content,filename):
    with open(filename,'wb') as file:
        file.write(file_content)
        file.close()
    qbar.update(1)

input('即将开始更新Geo文件，请确保网络连接正常，回车即可继续。')
print('Geo文件更新开始，请勿中断程序……')
if os.path.exists('geosite.db'):
    os.remove('geosite.db')
if os.path.exists('geoip.db'):
    os.remove('geoip.db')
latest_ver = get_latest().split('/')[-1:][0]
base_url = 'https://github.com/lyc8503/sing-box-rules/releases/download/' + latest_ver + '/'
print('已获取最新版本：'+str(latest_ver))
qbar = tqdm(total=2)
geosite = savefile(getfile(base_url+'geosite.db'),'geosite.db')
geoip = savefile(getfile(base_url+'geoip.db'),'geoip.db')
input('更新完毕！回车即可关闭本窗口。')
exit()