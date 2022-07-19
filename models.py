from abc import abstractmethod
from pypmml import Model
from preprocess_utils import parse_tensor, parse_fields
from redirection import MyStdout, MyStderr
import onnx
import onnxruntime as rt
import numpy as np
import json

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
        self.model = Model.fromFile(path)
        self.name = name
        self.total = {}
        self.total['engine'] = 'PyPMML'
        self.total['name'] = self.model.modelName
        self.total['type'] = self.model.modelElement
        self.total['function'] = self.model.functionName
        self.total['input'] = parse_fields(self.model.inputFields)
        self.total['output'] = parse_fields(self.model.outputFields)

    def getInfo(self):
        return self.total
    
    # TODO: 支持除了分类以外的其他任务
    def predict(self, data):
        if isinstance(data, list):
            # 仅测试用
            inputs = data
        else:
            # data 输入单条数据预计为json格式, 见`pmml_input_template.json`
            data = json.loads(data)
            inputs = data['inputs']
            inputs = [item['value'] for item in inputs]

        # 重定向
        myStderr = MyStderr()
        myStdout = MyStdout()

        # 判断是否输出了分类标签
        res = np.array(self.model.predict(inputs))
        flg = True
        if sum(res) == 1 and not (res == 0).any():
            # res只有概率分布
            flg = False
            label = np.argmax(res)
        output_keys = [output["name"] for output in self.total["output"]]
        outputs = dict(zip(output_keys, res))
        if not flg:
            outputs['predicted_label'] = label
        stderr = MyStderr.errinfo
        stdout = MyStdout.outinfo
        print("test output redirection")

        # 恢复标准输出
        myStderr.restoreStd()
        myStdout.restoreStd()

        # 输出为json
        output_json = {}
        output_json['result'] = outputs
        output_json['stdout'] = stdout
        output_json['stderr'] = stderr
        return json.dumps(output_json)

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
