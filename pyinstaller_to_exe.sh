Jaden-5Tg0WTB- ��������
#�������⻷��
pipenv install
#�������⻷������һ����ʡ��,��Ϊû�����⻷���Ļ����Զ�����һ����
pipenv shell
#��װģ��
pip install requests pyquery pysimplegui fake_useragent
#�����ģ��ҲҪ��װ
pip install pyinstaller
pyinstaller --icon=scr.ico -F -w pochanwang.py

pyinstaller --paths d:\software\anaconda\Library\bin\ --icon=scr.ico -F pochanwang.py

Pyinstaller ��Failed to execute script pyi_rth_pkgres�� and missing packages

pyinstaller --hidden-import=pkg_resources.py2_warn --icon=scr.ico -F pochanwang.py

pyinstaller --icon=scr.ico pochanwang.py 

1.ʹ��html.parser������lxml
2.setuptools == 44.0.0 �����������

