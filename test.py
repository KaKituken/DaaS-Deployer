
from distutils.debug import DEBUG
import numpy as np
import pandas as pd
import os
import cv2
import json
from manager import Manager
from models import AbstractModel, PmmlModel, OnnxModel
from flask import Flask, render_template, request
from flask_cors import CORS

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

class Request:
    def __init__(self, name, path, type, data=None) -> None:
        self.name = name
        self.path = path
        self.type = type
        self.data = data

def predict(request: Request):
    data = request.data
    name = request.name
    return manager.getModel(name).predict(data)


manager = Manager()

def add(name, path, type):
    if type == 'pmml':
        manager.addModel(PmmlModel(path, name))
    elif type == 'onnx':
        manager.addModel(OnnxModel(path, name))
    else:
        pass

def getInfo(request: Request):
    name = request.name
    model = manager.getModel(name)
    return model.getInfo()

@app.route('/', methods=['GET'])
def index():
    return render_template('./index.html')

@app.route('/', methods=['POST'])
def upload():
    file = request.files['file']
    name = request.form.get('name')
    type = request.form.get('type')
    # 保存模型
    path = os.path.join(os.path.join(os.getcwd(), 'data'), file.filename)
    file.save(path)
    print(file)

    # 加入manager
    add(path, name, type)

    return {'status': 'success'}

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run()

    # # 测试
    # re = Request('model.pmml', './data/mnist-8.onnx', 'onnx')
    # add(re.name, re.path, re.type)
    # info = getInfo(re)
    # with open("data1.json", "w", encoding="utf-8") as f:
    #     json.dump(info, f, ensure_ascii=False, indent=4)
