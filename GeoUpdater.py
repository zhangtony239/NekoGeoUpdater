import requests

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
    
latest_ver = get_latest().split('/')[-1:][0]
base_url = 'https://github.com/lyc8503/sing-box-rules/releases/download/' + latest_ver + '/'
geosite = savefile(getfile(base_url+'geosite.db'),'geosite.db')
geoip = savefile(getfile(base_url+'geoip.db'),'geoip.db')