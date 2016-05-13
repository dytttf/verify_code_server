#coding:utf8
'''
验证码图片类型说明
    1:http://shixin.court.gov.cn/image.jsp
    2:http://zhixing.court.gov.cn/search/security/jcaptcha.jpg
    
'''
import os
import md5
import random
import time
from collections import defaultdict
from bottle import run, post, request
from PIL import Image

code_template_dic = {
    1:{},
    2:{}
    }

curpath = os.path.dirname(__file__)

def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1

def load_template(path):
    template_dic = defaultdict(list)
    for num in range(10):
        dir_path = os.path.join(path, '%s'%num)
        files = os.listdir(dir_path)
        images = [Image.open(os.path.join(dir_path, filename)) for filename in files]
        template_dic[num] = [buildvector(img) for img in images]
        for img in images:
            if hasattr(img, 'close'):
                img.close()
    return template_dic
    
def load_all():
    global code_template_dic
    for code_typ in code_template_dic.keys():
        path = os.path.join(curpath, 'main', 'template', '%s'%code_typ)
        template_dic = load_template(path)
        code_template_dic.update({
            code_typ:template_dic
            })
        #break
    return

#加载模版
load_all()

@post('/code')
def code_verify_out():
    try:
        code = code_verify(request)
    except:
        code = 'ERROR'
    return code

def code_verify(request):
    image_str = request.forms.get("code")
    typ = int(request.forms.get('type'))
    filename = os.path.join(
        curpath,
        'temp',
        '%s.png'%(
            md5.md5(
                str(time.time()) + str(random.random())
            ).hexdigest()
        )
    )
    with open(filename, 'wb') as f:
        f.write(image_str)
    img = Image.open(filename)
    exec '''from main import main_%s'''%(typ)
    exec '''code = main_%s.verify(img, code_template_dic[typ])'''%(typ)
    #exec '''code = main_%s.verify(img)'''%(typ)
    if hasattr(img, 'close'):
        img.close()
    try:
        os.remove(filename)
    except Exception as e:
        print u"删除图片失败 %s"%e
    return code

run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    #load_all()
    pass
        
