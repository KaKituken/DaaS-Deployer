from time import time, ctime
import numpy as np
import pandas as pd
import os
import json
from manager import Manager
from models import AbstractModel, PmmlModel, OnnxModel
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api
from preprocess_file import preprocess_csv, preprocess_zip

DEBUG = True

# configurations & resoureces

app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)
CORS(app, resources={r'/*': {'origins': '*'}})

class Request:
    def __init__(self, name, path, type, descript, data=None):
        self.name = name
        self.path = path
        self.type = type
        self.data = data
        self.descript = descript


class ModelRestfulAPI(Resource):
    def get(self, model_name):
        model = manager.getModel(model_name)
        data = request.json['data']
        return jsonify(model.predict(data))


api.add_resource(ModelRestfulAPI, '/<string:model_name>')


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


# route to access

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
    file = request.files['file']
    name = request.form.get('name')
    type = request.form.get('type')
    descript = request.form.get('descript')
    # save model -> ./models/model_name/model_name.pmml
    path = os.path.join(os.path.join(os.getcwd(), f'models/{name}/'), file.filename)
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


@app.route('/upload-file', methods=['POST'])
def upload_file():
    # 只是先存下来，不急着处理，等调用job的时候再处理
    file = request.files['file']
    model_name = request.json['modelName']
    # save data -> ./models/model_name/data，也就是说，和对应的model存在一起
    path = os.path.join(os.path.join(os.getcwd(), f'models/{model_name}/'), file.filename)
    file.save(path)
    # ----------------放在job内-------------------
    _, ext = file.filename.split('.')
    ret = []
    if ext == 'zip':
        ret = preprocess_zip(file)
    elif ext == 'csv':
        ret = preprocess_csv(file)
    print(ret)
    # -------------------------------------------
        

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


# 部署服务
@app.route('/model-deploy/service', methods=['POST'])
def get_model_deploy_data():
    # 需要在这步生成docker service，并得到端口号（run flask in docker）
    model = manager.getModel(request.name)
    restful_url = ""
    server_version = [f"Python 3.{x} - Function as a Service" for x in range(7, 11)]
    response_data = {}
    response_data['restfulUrl'] = restful_url
    response_data['serverVersion'] = server_version
    return jsonify(response_data)


# 部署job
@app.route('./model-deploy/job', methods=['POST'])
def deploy_job():
    # 创建一个job，但是不运行，返回端口号（待测试）
    pass


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run()

    # # test
    # re = Request('test_model', './data/digis.pmml', 'pmml', 'this is a test model')
    # add(re.name, re.path, re.type, re.descript)
    # info = manager.getModel(re.name).getInfo()
    # with open("digis_data.json", "w", encoding="utf-8") as f:
    #     json.dump(info, f, ensure_ascii=False, indent=4)
