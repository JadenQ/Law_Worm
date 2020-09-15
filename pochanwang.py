import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
#import pkg_resources.py2_warn
import os

#将字符串仅保留汉字与数字
def format_Chinese_num(str):
    str = re.sub("[：A-Za-z\!\%\[\]\,\。""''></=_\n\"\r]", "", str)
    return str

def request_df(url,headers,payload):
    
    response = requests.request("POST", url, headers=headers, data = payload)

    #print(response.text.encode('utf8'))
    result = response.content.decode('utf-8')
    
    #寻找html中的元素
    soup = BeautifulSoup(result, features="html.parser")
    
    #案号
    ah = []
    for k in soup.find_all('a'):
        ah.append(format_Chinese_num(str(k['title'])))#查a标签的class属性
    
    #时间与案件类型
    time = []
    ajlx = []
    time_ajlx = []
    for k in soup.find_all('span'):
        time_ajlx.append(format_Chinese_num(str(k)))
    for i in range(len(time_ajlx)):
        if (i%2==1):
            time.append(time_ajlx[i])
        else:
            ajlx.append(time_ajlx[i])
    del time_ajlx
    
    #经办法院、申请人与被申请人
    fy_bsq_sq = []
    fy = []
    bsq = []
    sq = []
    
    for k in soup.find_all('p'):
        fy_bsq_sq.append(format_Chinese_num(str(k)).replace('  ',''))
    for i in range(len(fy_bsq_sq)):
        if (i%3==0):
            try:
                fy.append(fy_bsq_sq[i].replace('经办法院:',' ').strip())
            except IndexError:
                print('缺失法院数据')
                fy.append('-')
        elif(i%3==1):
            try:
                bsq.append(fy_bsq_sq[i].replace('被申请人:',',').replace('被上诉人:',',').split(',')[1])
            except IndexError:
                print('缺失被申请人数据')
                bsq.append('-')
        else:
            try:
                sq.append(fy_bsq_sq[i].replace('申请人:',',').replace('上诉人:',',').split(',')[1])
            except IndexError:
                print('缺失申请人数据')
                sq.append('-')
    del fy_bsq_sq
    
    #创建df保存数据
    df = pd.DataFrame({'案号':ah,'时间':time,'案件类型':ajlx,'经办法院':fy,'申请人':sq,'被申请人':bsq})    
    return df

#url
url = "http://pccz.court.gov.cn/pcajxxw/gkaj/gkajlb"
#开始和结束时间
print('===========欢迎使用爬虫软件==========')
print('—————————————Ver1.0———————————————')
# print('请输入最新cookies：')
# cookies_code = input()
print('输入开始时间xxxx-xx-xx:')
startT = input()
print('输入结束时间xxxx-xx-xx:')
endT = input()
#startP = 1
#endP = 50

print('输入起始页码数：(默认可输入1):')
startP = input()
startP = int(startP)
print('输入结束页码数：(默认可输入50):')
endP = input()
endP = int(endP)

with open('cookies.txt', 'r') as f:
        for line in f:
            cookies_name = line
print('cookies:',cookies_name)


#headers设置
headers = {
  'Connection': 'keep-alive',
  'Accept': 'text/html, */*; q=0.01',
  'X-Requested-With': 'XMLHttpRequest',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Origin': 'http://pccz.court.gov.cn',
  'Referer': 'http://pccz.court.gov.cn/pcajxxw/gkaj/gkaj',
  'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
  'Cookie': cookies_name
}


df = pd.DataFrame(columns = ['案号','时间','案件类型','经办法院','申请人','被申请人'])
try:
    for i in range(startP,endP+1):    
        payload = "start={}&end={}&cbt=&lx=999&pageNum={}".format(startT,endT,i)  
        df0 = request_df(url,headers,payload)
        if len(df0)==0:
            break
        else:
            df = pd.concat([df,df0],axis = 0)
        print('正在爬取第',i,'页...')
        #如果待加载数据过多，停留2秒翻页
        time.sleep(8)
        if df0['时间'][9].strip() != endT:
            break
except KeyError:
    print('爬取完成或者触动了反爬')
except ConnectionError:
    print('网络访问失败了哦，请从第{}页开始继续爬取'.format(i))
except ValueError:
    print('ValueError:网络出现问题，请从第{}页开始继续爬取'.format(i))
finally:
    df.to_csv('./results/{}至{} 第{}至{}页.csv'.format(startT,endT,startP,i),encoding='utf_8_sig')
print('完成爬取！')
os.system("pause")