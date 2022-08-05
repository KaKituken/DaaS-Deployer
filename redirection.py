import sys

class MyStdout():

    def __init__(self):
        self.outinfo = []   # 保存重定向信息
        self.stdoutbak = sys.stdout
        sys.stdout = self
        
    def write(self, info):
        #info信息即标准输出sys.stdout接收到的输出信息
        str = info.strip()
        if len(str): 
            self.processInfo(str)  #对输出信息进行处理的方法
    
    def processInfo(self, info):
        self.stdoutbak.write("标准输出接收到消息："+info+"\n") #可以将信息再输出到原有标准输出，在定位问题时比较有用
        self.outinfo.append(info)
	
    def restoreStd(self):
        sys.stdout = self.stdoutbak 

    def __del__(self):
       self.restoreStd()
       

class MyStderr():

    # errinfo = []    # 保存重定向信息

    def __init__(self):
        self.errinfo = []
        self.stderrbak = sys.stderr
        sys.stderr = self

    def write(self, info):
        # info 为sys.stderr收到的报错信息
        str = info.strip()
        if len(str):
            self.processInfo(str)

    def processInfo(self, info):
        self.stderrbak.write("标准错误收到消息: " + info + "\n")
        self.errinfo.append(info)

    def restoreStd(self):
        sys.stderr = self.stderrbak

    def __del__(self):
        self.restoreStd()

# 重定向测试
if __name__ == "__main__":
    mystd = MyStdout()
    print("你好")
    mystd.restoreStd()
    print(MyStdout.outinfo)