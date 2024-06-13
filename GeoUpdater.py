import requests,os,shutil

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

print('Geo文件更新开始，请勿中断程序……')
latest_ver = get_latest().split('/')[-1:][0]
base_url = 'https://github.com/lyc8503/sing-box-rules/releases/download/' + latest_ver + '/'
print('已获取最新版本：'+str(latest_ver))
os.mkdir('geo.old/')
shutil.move('geosite.db','geo.old/geosite.db')
shutil.move('geoip.db','geo.old/geoip.db')
try:
    geosite = savefile(getfile(base_url+'geosite.db'),'geosite.db')
    geoip = savefile(getfile(base_url+'geoip.db'),'geoip.db')
    shutil.rmtree('geo.old/')
    input('更新完毕！回车即可关闭本窗口。')
except:
    shutil.move('geo.old/geosite.db','geosite.db')
    shutil.move('geo.old/geoip.db','geoip.db')
    shutil.rmtree('geo.old/')
    input('更新失败，请检查报错信息！原Geo文件已恢复，回车以退出程序。')