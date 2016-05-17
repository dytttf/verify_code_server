# coding:utf8
import math
import numpy as np

class VectorCompare(object):
    #计算矢量大小
    def magnitude(self,concordance):
        total = concordance.dot(concordance)
        return math.sqrt(total)

    #计算矢量之间的 cos 值
    def relation(self,concordance1, concordance2):
        if len(concordance1) < len(concordance2):
            concordance1 = np.array(concordance1.tolist() + [0] * (len(concordance2) - len(concordance1)))
        else:
            concordance2 = np.array(concordance2.tolist() + [0] * (len(concordance1) - len(concordance2)))
        topvalue = concordance1.dot(concordance2)
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

def buildvector(im):
    d1 = np.array(im.getdata())
    return d1
