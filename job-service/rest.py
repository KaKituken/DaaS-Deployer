import json
from preprocess_file import *
import argparse
import models

IMG = ['jpg', 'png']
TXT = ['txt', 'json']



def predict(data, model, model_type):
    if model_type == "pmml":
        return model.predict(data)
    elif model_type == "onnx":
        return model.predict(data)
    else:
        return {'status': 400}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', required=True, help="path to input dataset")
    parser.add_argument('-o', '--output', required=True, help="path to output dataset")
    parser.add_argument('-m', '--model', required=True, help="model to run")
    parser.add_argument('-t', '--type', required=True, help="model type")

    args = parser.parse_args()
    input = args.input
    output = args.output
    model_name = args.model
    model_type = args.type
    ext = input.split('.')[-1]

    # 读入模型
    if model_type == "pmml":
        model = models.PmmlModel(f'/model/{model_name}.pmml', model_name, None)
    elif model_type == "onnx":
        model = models.OnnxModel(f'/model/{model_name}.onnx', model_name, None)

    # 判断是单个文件还是压缩包
    if ext in TXT:
        with open('/dataset/'+input) as f:
            data = f.read()
        data = preprocess_txt(data, ext)
        print(type(data))
        res = predict(data, model, model_type)
    elif ext in IMG:
        data = preprocess_img("/dataset/"+input, model)
        res = predict(data, model, model_type)
    elif ext == 'zip' or ext == 'csv':
        data = preprocess_zip('/dataset/' + input, model)
        res = []
        for d in data:
            res.append(predict(d, model, model_type))

    res_info = {}
    res_info['outputs'] = res

    out_ext = output.split('.')[-1]
    if out_ext == "json":
        with open('/dataset/' + output, 'w') as f:
            json.dump(res_info, f)
    else:
        pass