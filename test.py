#coding:utf8
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
