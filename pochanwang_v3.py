# -*- coding: utf-8 -*-
"""
Created on Sun May 17 10:40:50 2020

@author: Jaden
"""

# -*- coding: utf-8 -*-
"""
Created on Sat May 16 15:46:18 2020

@author: Jaden
"""

# -*- coding: utf-8 -*-
# 使用Selenium, 北京安居客->小区->二手房信息
import json
import requests
from lxml import etree
import time
from selenium import webdriver
import pandas as pd 
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.chrome.options import Options

chromedriver = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"


# 需要将chromedriver放到Chrome\Application目录下
#driver = webdriver.Chrome()
driver = webdriver.Chrome(chromedriver)
# 去空格，去换行\n
print('只查询一天的话填同样的日期(格式xxxx-xx-xx)')
startDate = input("输入起始日期哦：")
endDate = input("输入结束日期:")

def InputDate(startDate,endDate):
    driver.find_element_by_id('rel').send_keys(startDate)
    driver.find_element_by_id('zhi').send_keys(endDate)
    driver.find_element_by_class_name('btn.searchBtn').click()
    return 0

def format_str(str):
    return str.replace('\n', '').replace(' ', '')

def ToPage():
    return 0
# 对页面进行抓取分析
def work(request_url):
    driver.get(base_url)
    time.sleep(1)
    InputDate(startDate,endDate)
    html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
    html = etree.HTML(html)
    # 设置需要抓取字段的xpath,每页显示10条信息
    title = []
    caseType = []
    court = []
    WasApp = []
    App = []
    date = []
    caseList = html.xpath("/html/body/div[@class='container clearfix']/div[@class='content_right container']/div[@id='gkajlb']/div[@class='caseList']/text()")
    print(caseList)
    for i in range(1,11):
        title.append(html.xpath("/html/body/div[@class='container clearfix']/div[@class='content_right container']/div[@id='gkajlb']/ul[{}]/li[@class='clearfix']/div[1]/h4[@class='cbt']/a/text()".format(i)))
        caseType.append(html.xpath("/html/body/div[@class='container clearfix']/div[@class='content_right container']/div[@id='gkajlb']/ul[{}]/li[@class='clearfix']/div[1]/span[@class='ajlx']/text()".format(i)))
        court.append(html.xpath("/html/body/div[@class='container clearfix']/div[@class='content_right container']/div[@id='gkajlb']/ul[{}]/li[@class='clearfix']/div[@class='center']/p[1]/text()".format(i)))
        WasApp.append(html.xpath("/html/body/div[@class='container clearfix']/div[@class='content_right container']/div[@id='gkajlb']/ul[{}]/li[@class='clearfix']/div[@class='center']/p[2]/text()".format(i)))
        App.append(html.xpath("/html/body/div[@class='container clearfix']/div[@class='content_right container']/div[@id='gkajlb']/ul[{}]/li[@class='clearfix']/div[@class='center']/p[3]/text()".format(i)))
        date.append(html.xpath("/html/body/div[@class='container clearfix']/div[@class='content_right container']/div[@id='gkajlb']/ul[{}]/li[@class='clearfix']/div[1]/span[@class='date']/text()".format(i)))
#date 为空值？
    cases = pd.DataFrame(columns = ['title', 'caseType', 'court', 'WasApp', 'App','date'])
    for i in range(len(title)):
        # 设置抓取的案件
        temp = {}
        temp['title'] = format_str(title[i][0])
        temp['caseType'] = format_str(caseType[i][0])
        temp['court'] = format_str(court[i][0])
        temp['WasApp'] = format_str(WasApp[i][0])
        temp['App'] = format_str(App[i][0])
        temp['date'] = format_str(date[i][0])

        # 添加案件
        cases = cases.append(temp,ignore_index=True)
    return cases

# 抓取10页案件数据
page_num = 5
base_url = 'http://pccz.court.gov.cn/pcajxxw/gkaj/gkaj'
cases = pd.DataFrame(columns = ['title', 'caseType', 'court', 'WasApp', 'App','date'])
for i in range(0, page_num):
    # 抓取该页的信息
    temp = work(base_url)
    cases = cases.append(temp)
    print(temp)
    time.sleep(1)
    # nextpagebutton 找不到可点击的翻页对象？
    if(i+1 == page_num):
        break
    else:
        # 将网页模拟滚轮滑倒底端，避免翻页按钮被遮挡
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(driver).send_keys(Keys.END).perform()
        if(i < 4):
            nextpagebutton = driver.find_element_by_xpath('//*[@id="kkpager"]/div[1]//a[{}]'.format(i+1))
        
        nextpagebutton.click()  # 模拟点击下一页
    wait = WebDriverWait(driver, 4)  # 浏览器等待4s
cases.to_csv('cases.csv',encoding = 'utf-8')


