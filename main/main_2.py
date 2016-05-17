#coding:utf8
'''
2:http://zhixing.court.gov.cn/search/security/jcaptcha.jpg
'''
import re
import os
import random
import math
import hashlib
import shutil
from PIL import Image
from collections import Counter, defaultdict
from util import VectorCompare, buildvector

#模版
global_template_dic = defaultdict(list)

def clear_image(img):
    u'''去噪'''
    img = img.convert('L')
    #img.show()
    new_img = Image.new('P', img.size, 255)
    his = img.histogram()
    values = {}
    pix_list = []
    #去噪声
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pix = img.getpixel((x, y))
            pix_list.append(pix)
            if pix < 175:
                new_img.putpixel((x,y), 0)
            else:
                new_img.putpixel((x,y), 255)
    return new_img

def split_image_with_width(img):
    u'''纵向切分'''
    foundletter = False
    inletter = False
    start, end = 0, 0
    letters = []
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pix = img.getpixel((x,y))
            if pix == 0:
                inletter = True
        if not foundletter and inletter:
            foundletter = True
            start = x

        if foundletter and not inletter:
            foundletter = False
            end = x
            letters.append((start, end))
        inletter = False
    image_temp_list = []
    for letter in letters:
        image_temp = img.crop((letter[0], 0, letter[1], img.size[1]))
        image_temp_list.append(image_temp)
    return image_temp_list

def split_image_with_height(img):
    u'''横向切分'''
    foundletter = False
    inletter = False
    start, end = 0, 0
    letters = []
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            pix = img.getpixel((x,y))
            if pix == 0:
                inletter = True
        if not foundletter and inletter:
            foundletter = True
            start = y

        if foundletter and not inletter:
            foundletter = False
            end = y
            letters.append((start, end))
        inletter = False
    image_temp_list = []
    for letter in letters:
        image_temp = img.crop((0, letter[0], img.size[0], letter[1]))
        image_temp_list.append(image_temp)
    return image_temp_list

def compare_image(vec_1, vec_2):
    u'''相似度比较'''
    similary = VectorCompare().relation(vec_1, vec_2)
    return similary

def cluster():
    u'''聚合图片'''
    path = './images/split_images'
    path = r'C:\Users\Administrator\Desktop\model'
    temp_dic = defaultdict(list)
    template_image_list = []
    for image_name in os.listdir(path):
        img = Image.open(os.path.join(path, image_name))
        if not template_image_list:
            template_image_list.append(img)
            temp_dic[img].append(img)
        else:
            similary_list = []
            for template_img in template_image_list:
                similary = compare_image(template_img, img)
                if similary > 0.9:
                    similary_list.append((similary, template_img))
            if similary_list:
                similary_list.sort(key=lambda x:x[0])
                temp_dic[similary_list[-1][1]].append(img)
            else:
                temp_dic[img].append(img)
                template_image_list.append(img)
   #print len(template_image_list)
    #return
    idx = 0
    for k, image_list in temp_dic.iteritems():
        dir_path = "./images/template_images/%s"%idx
        os.mkdir(dir_path)
        count = 0
        for img in image_list:
            img.save(os.path.join(dir_path, "%s_%s.png"%(idx, count)))
            count += 1
        idx += 1
    return

def to_top():
    u'''把子目录里的文件提取到上层'''
    def dd(path, dest):
        for root, dirs, files in os.walk(path):
            for dir_c in dirs:
                dd(os.path.join(root, dir_c), dest)
            for filename in files:
                shutil.copyfile(os.path.join(root, filename), os.path.join(dest, filename))
        shutil.rmtree(path)
    path = r'E:\FPAN\somepy\mypyfile\test_PIL\zhixing_court_gov_cn\images\template_images'
    for root, dirs, files in os.walk(path):
        for dir_c in dirs:
            path_1 = os.path.join(path, dir_c)
            for root_1, dirs_1, files_1 in os.walk(path_1):
                for dir_1_c in dirs_1:
                    dd(os.path.join(root_1, dir_1_c), path_1)
    return

def load_template():
    curpath = os.path.dirname(__file__)
    template_dic = defaultdict(list)
    path = os.path.join(curpath, 'template', '2')
    for num in range(10):
        dir_path = os.path.join(path, '%s'%num)
        files = os.listdir(dir_path)
        images = [Image.open(os.path.join(dir_path, filename)) for filename in files]
        template_dic[num] = [buildvector(img) for img in images]
        for img in images:
            if hasattr(img, 'close'):
                img.close()
    return template_dic

def verify(image, template_dic=load_template()):
    image = clear_image(image)    
    image_split_list = split_image_with_width(image)
    code = []
    for image in image_split_list:
        image = split_image_with_height(image)[0]
        num_similary = []
        for num, template_image_list in template_dic.iteritems():
            temp_similary = []
            for template_image_vec in template_image_list:
                iamge_vec = buildvector(image)
                similary = compare_image(template_image_vec, iamge_vec)
                temp_similary.append(similary)
            temp_similary.sort()
            num_similary.append((temp_similary[-1], num))
        num_similary.sort(key=lambda x:x[0])
        code.append(str(num_similary[-1][1]))
    return ''.join(code)

def verifyall():
    global global_template_dic
    global_template_dic = load_template()
    
    path = r'E:\FPAN\somepy\mypyfile\test_PIL\zhixing_court_gov_cn\images\original_images'
    for image_name in os.listdir(path):
        #if '6804' not in image_name:
        #    continue
        abs_image_name = os.path.join(path, image_name)
        image = Image.open(abs_image_name)
        image = clear_image(image)
        
        image_split_list = split_image_with_width(image)
        code = []
        for image in image_split_list:
            image = split_image_with_height(image)[0]
            #image.show()
            #image.save('%s.png'%random.randint(0, 10))
            num_similary = []
            for num, template_image_list in global_template_dic.iteritems():
                temp_similary = []
                for template_image_vec in template_image_list:
                    iamge_vec = buildvector(image)
                    similary = compare_image(template_image_vec, iamge_vec)
                    temp_similary.append(similary)
                temp_similary.sort()
                #if num == 0:
                #    print temp_similary
                num_similary.append((temp_similary[-1], num))
            num_similary.sort(key=lambda x:x[0])
            #print num_similary
            #print num_similary[-1]
            code.append(str(num_similary[-1][1]))
            
        os.rename(abs_image_name, re.sub("\d+\.jpg", "%s.jpg"%''.join(code), abs_image_name))
        #break
    return 
                

def main():
    images = os.listdir('./images/original_images')
    for image_name in images:
        img = Image.open(os.path.join('./images/original_images', image_name))
        new_img = clear_image(img)
        new_img.save(os.path.join('./images/clear_images', image_name.replace('jpg', 'png')))
        image_temp_list_width = split_image_with_width(new_img)
        for idx_width, image_temp_width in enumerate(image_temp_list_width):
            image_temp_list_height = split_image_with_height(image_temp_width)
            if hasattr(image_temp_width, 'close'):
                image_temp_width.close()
            for idx_height, image_temp_height in enumerate(image_temp_list_height):
                image_temp_height.save("./images/split_images/%s_%s_%s"%(idx_width, idx_height, image_name.replace('jpg', 'png')))
                if hasattr(image_temp_height, 'close'):
                    image_temp_height.close()
        if hasattr(img, 'close'):
            img.close()
        if hasattr(new_img, 'close'):
            new_img.close()

    return

if __name__ == "__main__":
    #image_path = r'E:\FPAN\somepy\mypyfile\test_PIL\zhixing_court_gov_cn\images\split_images\0_0_1462755420.png'
    #img = Image.open(image_path)
    #main()
    #clear_image(img)
    #cluster()
    #to_top()
    #verifyall()
    #测试单个图片
    img = Image.open('./test_iamge/2.jpg')
    print verify(img, load_template())
