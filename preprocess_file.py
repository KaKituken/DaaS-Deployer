import pandas as pd
import zipfile
import os
import numpy as np
from PIL import Image
import models


IMG = ['jpg', 'png']
TXT = ['txt', 'json']


def preprocess_zip(zip, model): # 传入zip压缩包以及model
    res = []

    z = zipfile.ZipFile(zip, "r")
    # z = zipfile.ZipFile(os.path.join(os.getcwd(), 'img.zip'))
    for i in z.namelist():
        try:
            data = z.open(i)
            _, ext = i.split('.')
            if ext in IMG: # 图片集
                image_data = preprocess_img(data, model)
                res.append(image_data)
            elif ext in TXT: # 文本文件
                res.append(preprocess_txt(data, ext))
            else: # csv格式文件
                csv_data = preprocess_csv(data, model)
                res.append(csv_data)
        except:
            pass
    return res

def preprocess_csv(csv, model):
    csv_data = pd.read_csv(csv).to_dict(orient = 'records') # 读取csv文件并转化为字典
    print(csv_data)
    model_info = model.getInfo()['input']
    res = {}
    if model.total['engine'] == 'PyPMML': # 处理pmml格式的输入
        inputs_list = []
        for k,v in csv_data[0].items():
            item = {}
            item['name'] = k
            item['value'] = v
            inputs_list.append(item)
        res["inputs"] = inputs_list
    elif model.total['engine'] == 'ONNX Runtime': # 处理onnx格式的输入
        print('onnx csv')

def preprocess_img(image,model):
    img = Image.open(image) # 读取图片 
    img = img.convert('L') # 灰度化
    cols, rows = img.size # 图片大小
    Value = [[0] * cols for i in range(rows)]  # 创建一个大小与图片相同的二维数组
    img_array = np.array(img)
    for x in range(0, rows):
        for y in range(0, cols):
            Value[x][y] = img_array[x, y]  # 存入数组
    
    res = {}
    model_info = model.getInfo()['input']

    if model.total['engine'] == 'PyPMML': # 处理pmml格式的输入
        print('pmml img')
    elif model.total['engine'] == 'ONNX Runtime': # 处理onnx格式的输入
        print(model_info)
        res["X"] = [{model_info['name']:[[Value]]}]
        print(res)
    return res



def preprocess_txt(txt, ext):
    if ext == 'txt':
        return 'txt'
    elif ext == 'json':
        pass
    else:
        return ""


if __name__ == '__main__':
    model = models.OnnxModel('./data/mnist-8.onnx', 'test_model', "This is a test model")
    preprocess_zip("", model)
