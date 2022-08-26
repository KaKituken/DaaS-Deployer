from models import AbstractModel
class Manager():
    def __init__(self) -> None:
        self.map = {}
    
    # 重名
    def addModel(self, model: AbstractModel) -> bool:
        if model.name in self.map.keys():
            return False
        self.map[model.name] = model
        return True
    
    def getModel(self, name) -> AbstractModel:
        return self.map[name]

    # TODO: 放到本地
    def deleteModel(self, name) -> bool:
        if name not in self.map.keys():
            return False
        del self.map[name]
        return True