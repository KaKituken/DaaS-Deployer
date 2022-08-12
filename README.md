# DaaS-Deployer
2022小学期前后端大作业
## 选题
机器学习模型在线服务
## 分工表
- 前端：董文冲、潘首安、邢海潼
- 后端：罗华坤、李晨宇、何吉轩

## 待讨论的问题
（DAAS界面）
前后端衔接
一堆细节。。。

### 前端
框架：arco.design vue

### 后端
docker+k8s（也许可以参考一下B站上的教程）
Flask
1. 服务器（科协也许）
2. DaaS
3. 测试模型
4. 模型数据

可以先把上传模型的部分写了`db.model`（本地上传到云端+存储云端的地址，丢给前端）（周五之前）

## 功能/进度安排
- [ ]上传模型（pmml + onnx）（后端需要自己写model，用Flask）
    - [ ] 查看模型信息
- [ ]测试模型通过表单输入数据(表单项可能是文本也可能是文件，类似 postman)或者使用 JSON 命令直接输入 JSON 格式的数据，提交后预测结果会显示在界面中
- [ ]部署模型（纯后端，暴露一个给前端，测试时暴露给外部）
    - [ ]对外提供 restful api 接口进行调用
    - [ ]暂停，启动，删除
    - [ ]当前服务的状态
- [ ]前端测试部署的接口
- [ ]对外提供快速返回与等待返回两种API

## 文件/接口说明
- `test.py`中为Flask框架，“测试模型”功能需要从前端读取json格式的输入，见`./data/pmml_input_template.json`，之后返回给前端json格式的输出，见`./data/pmml_output_template.json`
- `manager.py`保存当前加载的模型信息（路径）
- `models.py`中实现模型的信息获取、预测等具体功能
- 使用`./data/pmml_generator.py`可以更换算法生成`.pmml`文件

*by助教：我们需要实现对分类、回归、聚类、降维任务的支持*
### 后端数据生成格式
- 分类: 返回概率分布、label
- 回归: 返回预测值（+置信度）
- 聚类: 等下
- 降维: 也等下



## Restful API文档

### 上传模型

- Post: `/model-upload`

- Param:

  ```json
  reqest{
  	"file": ,
  	"form": {	// 使用表单，会自动存进去
  		"name": ,
  		"type": ,
      "descript": ,
  	}
  }
  ```

- Response:

  ```json
  response{
      "data": {
      	"modelName": ,
      	"modelType": ,
      	"descript": ,
      	"updataTime": ,	// 上传上去的时间
      	"operation": ,
      	"status": ,		// 模型是否有效，无效搞一个报错
  	}
  }
  ```

### 获得模型概述

- POST: `/model-descript`

- Param:

  ```json
  let param = {
      "modelName": 
  }
  axios.GET('url', param)
  ```

- Response:

  ```json
  {
      "data": {
      	"modelName": ,
      	"modelType": ,
      	"modelEngine": ,
      	"descript": ,
      	"algorithm": ,
  	}
  }
  ```

### 获得模型变量

- POST: `/model-variable`

- Param: modelName

- Response:

  ```json
  {
      "data": {
      	"inputVariables":[
      
      	],
  		"targetVariables":[
              
          ]
  	}
  }
  ```

### 测试模型

- POST:`/model-test`

- Param: 按照模板文件`./data/pmml_input_template.json`

  ```json
  {
      "modelName": "",
      "data": {
          // 见./data/pmml_input_template.json
      }
  }
  ```

- Response: 前面的模板文件`./data/pmml_output_template.json`

### 部署实时预测Web服务

- POST:`/model-deploy-service`

- Param:

  ```json
  {
      "modelName": 
  }
  ```

- Response:（模型版本问一下）

  ```json
  {
      "data": {
      	"restfulUrl": ,
      	"serverVersion":[	// 可以规定一下
      
      	]
  	}
  }
  ```

提交时

- POST:`/model-deploy-service`

- Param:

  ```json
  {
      "modelName": ,
      "serverVersion": ,
      "cpuReserve": ,
      "memoryReserve": ,
      "replicas": ,
  }
  ```

- Response:

  ```json
  {
      "data": {
      	"restfulUrl": ,
  	}
  }
  ```

### 部署job

- POST: `/model-deploy-job`
- 待讨论

### 生成curl代码

前端来写吧，用上面的restfulUrl即可

### 提交Web服务

点击提交按钮，添加一个提交文件的按钮。（看看能不能根据后缀名改一下param中的type）

有两种返回：快速返回只接受json格式的输入（图片，视频也以json输入）同时不返回任务id；

等待返回发送一个文件包，先返回任务id。

如果格式是json，默认调用快速返回，如果是其他数据（如csv），传入文件名，文件统一放某一文件夹下（后端确定）

- POST: `restful url`

- Param:

  ```json
  {
      "type":	,// json or txt or csv...
      "args": ""
  }
  ```

- Response:

  快速返回：`{data{result}}`

  等待返回: `{data{id}}`

