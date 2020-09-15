Jaden-5Tg0WTB- （环境）
#建立虚拟环境
pipenv install
#进入虚拟环境（上一步可省略,因为没有虚拟环境的话会自动建立一个）
pipenv shell
#安装模块
pip install requests pyquery pysimplegui fake_useragent
#打包的模块也要安装
pip install pyinstaller
pyinstaller --icon=scr.ico -F -w pochanwang.py

pyinstaller --paths d:\software\anaconda\Library\bin\ --icon=scr.ico -F pochanwang.py

Pyinstaller “Failed to execute script pyi_rth_pkgres” and missing packages

pyinstaller --hidden-import=pkg_resources.py2_warn --icon=scr.ico -F pochanwang.py

pyinstaller --icon=scr.ico pochanwang.py 

1.使用html.parser而不是lxml
2.setuptools == 44.0.0 解决闪退问题

