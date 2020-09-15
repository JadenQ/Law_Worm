### 破产网信息爬虫整理 
http://pccz.court.gov.cn/pcajxxw/gkaj/gkaj
#### 1.selenium模拟网页点击操作
pochanwang_v3.py
仍然存在第5页之后无法锁定元素的bug
#### 2.request + beautifulsoup 利用request获得html，并用bs解析
pochanwang.py
可以正常运行已经交付
#### 3.sh文件用于使用pyinstaller生成exe可执行文件交付使用。
#### 4.cookeies.txt 内保存了可用的cookies，为了防止被禁用，可以定期更换，可以被pochanwang.py直接读取使用。
#### 5.运行情况
##### -支持输入收集信息的页码范围
##### -控制翻页间隔时间，防止IP被停用
##### -因网络问题中断时可保存进度并记录
##### -多种异常处理
