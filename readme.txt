#verify_code_server  [https://github.com/duanyifei/verify_code_server.git]

verify_code_server  用于搭建一个验证码识别的服务

支持验证码类型
	1、http://shixin.court.gov.cn/image.jsp
	2、http://zhixing.court.gov.cn/search/security/jcaptcha.jpg

	

验证码识别采用python的PIL模块

服务使用python的bottle模块


用法:

启动服务:
	python code_server.py

请求服务:
```#coding:utf8
import urllib2
import urllib

def code(fd,ty=1):
    '''
    获得图片验证码
    '''
    url = "http://localhost:8080/code"
    cod = open(fd,"rb").read()
    dat = {
        "code":cod,
        "type":ty,
        }
    data = urllib.urlencode(dat)
    req = urllib2.Request(url,data)
    resp = urllib2.urlopen(req,timeout=20)
    ma = resp.read()
    return ma

if __name__=="__main__":
    print code("./temp/1.jpg")
```
