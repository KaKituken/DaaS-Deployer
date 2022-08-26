import json
from preprocess_file import *
import argparse
import models
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS
from pypmml import Model
import onnx
import argparse

app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)
CORS(app, resources={r'/*': {'origins': '*'}})



# 持久卷./model

@app.route('/predict', methods=["POST"])
def predict():
    global model_name
    global model_type
    if model_type == "pmml":
        model = models.PmmlModel(f'/model/{model_name}.pmml', model_name, None)
    elif model_type == "onnx":
        model = models.OnnxModel(f'/model/{model_name}.onnx', model_name, None)
    # if request.json:
    try:
        data = request.json['data']
    except: 
    # elif request.files['file']:
        data_file = request.files['file']
        print(data_file)
        filename = data_file.filename
        ext = filename.split('.')[-1]
        # return filename
        print("ext:", ext)
        if ext in TXT:
            data_file = data_file.read()
            data = preprocess_txt(data_file, ext)
            print(type(data))
        elif ext in IMG:
            # TODO: 把图片先存到'temp/'下, 再读进来
            data_file.save('temp/' + filename)
            data = preprocess_img("temp/"+filename, model)
    if model_type == "pmml":
        return jsonify(model.predict(data))
    elif model_type == "onnx":
        return jsonify(model.predict(data))
    else:
        return jsonify({'status': 400})


@app.route("/file")
def file_test():
    file = request.files['file']
    return "hello file"


@app.route("/test")
def hello_world():
    return "hello world"

if __name__ == "__main__":
    # global model_name
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model', required=True, help="model to run")
    parser.add_argument('-t', '--type', required=True, help="model type")

    args = parser.parse_args()
    model_name = args.model
    model_type = args.type
    app.run(host='0.0.0.0', port=80)
    # app.run()