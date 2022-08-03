from time import time, ctime
import numpy as np
import pandas as pd
import os
import cv2
from manager import Manager
from models import AbstractModel, PmmlModel, OnnxModel
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

class Request:
    def __init__(self, name, path, type, data=None):
        self.name = name
        self.path = path
        self.type = type
        self.data = data


manager = Manager()

def add(name, path, type, descript) -> bool:
    if type == 'pmml':
        return manager.addModel(PmmlModel(path, name, descript))
    elif type == 'onnx':
        return manager.addModel(OnnxModel(path, name, descript))
    else:
        return False

def getInfo(request) -> dict:
    name = request.json['modelName']
    model = manager.getModel(name)
    return model.getInfo()

@app.route('/', methods=['GET'])
def index():
    return render_template('./index.html')


@app.route('/model-upload/test', methods=['POST'])
def upload_test():
    print(request.json)
    # test = json.loads(request.json)
    # print(test)
    path = request.json['file']
    name = request.json['name']
    type = request.json['type']
    descript = request.json['descript']
    print(path)

    # add into manager
    response_data = {}
    if add(name, path, type, descript):
        response_data['modelName'] = name
        response_data['modelType'] = type
        response_data['descript'] = descript
        response_data['updateTime'] = ctime()
        response_data['operation'] = ""
        response_data['status'] = True
        return jsonify(response_data)
    else:
        return jsonify({'status': False})


@app.route('/model-upload', methods=['POST'])
def upload():
    print(request.form)
    print("??????")
    file = request.files['file']
    name = request.form.get('name')
    type = request.form.get('type')
    descript = request.form.get('descript')
    # save model
    path = os.path.join(os.path.join(os.getcwd(), 'data'), file.filename)
    file.save(path)
    print(file)

    # add into manager
    response_data = {}
    if add(name, path, type, descript):
        response_data['modelName'] = name
        response_data['modelType'] = type
        response_data['descript'] = descript
        response_data['updateTime'] = ctime()
        response_data['operation'] = ""
        response_data['status'] = True
        return jsonify(response_data)
    else:
        return jsonify({'status': False})

@app.route('/model-descript', methods=['GET'])
def get_descript():
    total_info = getInfo(request)
    response_data = {}
    response_data['modelName'] = total_info['name']
    response_data['modelType'] = total_info['type']
    response_data['modelEngine'] = total_info['engine']
    response_data['descript'] = total_info['descript']
    response_data['algorithm'] = total_info['function']
    return jsonify(response_data)

    
@app.route('/model-variable', methods=['GET'])
def get_variable():
    total_info = getInfo(request)
    response_data = {}
    response_data['inputVariables'] = total_info['input']
    response_data['outputVariables'] = total_info['output']
    return jsonify(response_data)


@app.route('/model-test', methods=['POST'])
def predict():
    name = request.json['modelName']
    data = request.json['data']
    return jsonify(manager.getModel(name).predict(data))


@app.route('/model-deploy', methods=['GET'])
def get_model_deploy_data():
    model = manager.getModel(request.name)
    restful_url = ""
    server_version = [f"Python 3.{x} - Function as a Service" for x in range(7, 11)]
    response_data = {}
    response_data['restfulUrl'] = restful_url
    response_data['serverVersion'] = server_version
    return jsonify(response_data)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run()

    # # test
    # re = Request('model.pmml', './data/mnist-8.onnx', 'onnx')
    # add(re.name, re.path, re.type)
    # info = getInfo(re)
    # with open("data1.json", "w", encoding="utf-8") as f:
    #     json.dump(info, f, ensure_ascii=False, indent=4)
