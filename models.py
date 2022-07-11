from abc import abstractmethod
from pypmml import Model
from preprocess_utils import parse_tensor, parse_fields
import onnx
import onnxruntime as rt
import numpy as np

class AbstractModel():
    def __init__(self) -> None:
        pass

    @abstractmethod
    def predict(self, data):
        pass

    @abstractmethod
    def getInfo(self):
        pass

class PmmlModel(AbstractModel):
    def __init__(self, path, name) -> None:
        super().__init__()
        model = Model.fromFile(path)
        self.name = name
        self.total = {}
        self.total['engine'] = 'PyPMML'
        self.total['name'] = model.modelName
        self.total['type'] = model.modelElement
        self.total['function'] = model.functionName
        self.total['input'] = parse_fields(model.inputFields)
        self.total['output'] = parse_fields(model.outputFields)

    def getInfo(self):
        return self.total
    
    def predict(self, data):
        
        pass

class OnnxModel(AbstractModel):
    def __init__(self, path, name) -> None:
        super().__init__()
        
        model = onnx.load(path)
        self.name = name
        self.total = {}
        graph = model.graph
        self.total['type'] = 'ONNX'
        self.total['engine'] = 'ONNX Runtime'
        self.total['input'] = parse_tensor(graph.input[0])
        self.total['output'] = parse_tensor(graph.output[0])

    def getInfo(self):
        return self.total
    
    def predict(self, data):
        pass
