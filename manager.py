from models import AbstractModel
class Manager():
    def __init__(self) -> None:
        self.map = {}
    
    # 重名
    def addModel(self, model: AbstractModel):
        self.map[model.name] = model
        return True
    
    def getModel(self, name):
        return self.map[name]