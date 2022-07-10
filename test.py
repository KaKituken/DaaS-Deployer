from textwrap import indent
import onnx
import onnxruntime as rt
import numpy as np
import pandas as pd
from pypmml import Model
import pypmml
import cv2
import json

class Request:
    def __init__(self, name, type) -> None:
        self.name = name
        self.type = type

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
        total['input'] = shuru
        for input in model.inputFields:
            info = {}
            info['name'] = input.name
            info['optype'] = input.opType
            info['dataType'] = input.dataType
            info['valueRange'] = input.valuesAsString
            shuru.append(info)
        shuchu = []
        total['output'] = shuchu
        for output in model.targetFields:
            info = {}
            info['name'] = output.name
            info['optype'] = output.opType
            info['dataType'] = output.dataType
            info['valueRange'] = output.valuesAsString
            shuchu.append(info)
        
        return total
    elif request.type == 'onnx':
        try:
            model = onnx.load(name)
        except:
            return 'failure'
        

re = Request('model.pmml', 'pmml')
info = getInfo(re)
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(info, f, ensure_ascii=False, indent=4)
