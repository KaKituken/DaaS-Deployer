import onnx
import onnxruntime as rt
import numpy as np
import pandas as pd
from pypmml import Model
import pypmml
import cv2
import json
from utils import parse_tensor, parse_fields


class Request:
    def __init__(self, name, type) -> None:
        self.name = name
        self.type = type

def store():
    pass

def getInfo(request: Request):
    name = request.name
    if request.type == 'pmml':
        try:
        #todo: 绝对路径
            model = Model.fromFile(name)
        except:
            return 'failure'
        
        total = {}
        shuru = []
        total['engine'] = 'PyPMML'
        total['name'] = model.modelName
        total['type'] = model.modelElement
        total['function'] = model.functionName
        total['input'] = parse_fields(model.inputFields)
        total['output'] = parse_fields(model.outputFields)
        
        return total
    elif request.type == 'onnx':
        try:
            model = onnx.load(name)
        except:
            return 'failure'
        total = {}
        graph = model.graph
        total['type'] = 'ONNX'
        total['engine'] = 'ONNX Runtime'
        total['input'] = parse_tensor(graph.input[0])
        total['output'] = parse_tensor(graph.output[0])

        return total

re = Request('./data/mnist-8.onnx', 'onnx')
info = getInfo(re)
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(info, f, ensure_ascii=False, indent=4)
