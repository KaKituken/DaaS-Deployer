import pandas as pd
import zipfile
import os
import numpy as np
from PIL import Image
import json
from models import PmmlModel, OnnxModel


IMG = ['jpg', 'png']
TXT = ['txt', 'json']


def preprocess_zip(zip, model): # 传入zip压缩包以及model
    res = []
    file_type = zip.split('.')[-1]
    if file_type == 'csv':
        return preprocess_csv(zip, model)
    else:
        z = zipfile.ZipFile(zip)
        for i in z.namelist():
            try:
                data = z.open(i)
                _, ext = i.split('.')
                if ext in IMG: # 图片集
                    image_data = preprocess_img(data, model)
                    print(image_data)
                    res.append(image_data)
                elif ext in TXT: # 文本文件
                    # return str(type(data))
                    res.append(preprocess_txt(data, ext))
            except:
                # return "failed"
                pass
        return res


def preprocess_csv(csv, model):
    csv_data = pd.read_csv(csv).to_dict(orient = 'records') # 读取csv文件并转化为字典
    res = []
    if model.total['engine'] == 'PyPMML': # 处理pmml格式的输入
        for single_input in csv_data:
            single_res = {}
            inputs_list = []
            for k, v in single_input.items():
                item = {}
                item['name'] = k
                item['value'] = v
                inputs_list.append(item)
            single_res["inputs"] = inputs_list
            res.append(single_res)
    elif model.total['engine'] == 'ONNX Runtime': # 处理onnx格式的输入
        # print('onnx csv')
        print(csv_data)
    return res
        

def preprocess_img(image,model):
    # print(image)
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
        np_value_reshape = np.reshape(np.array(Value), model_info['shape'])
        # print(np_value_reshape.tolist())
        res["X"] = [{model_info['name']:np_value_reshape.tolist()}]
        print(res)
    return res


def preprocess_txt(txt, ext):
    if ext == 'txt':
        return json.loads(txt.read())
    else:
        return txt.read()


