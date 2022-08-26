import json
from random import randint
import re
from time import time, ctime
import os
import requests
from datetime import datetime
from manager import Manager
from models import AbstractModel, PmmlModel, OnnxModel
from flask import Flask, render_template, request, jsonify, Response, send_file
from flask_session import Session
from flask_cors import CORS
from flask_restful import Resource, Api
from database.database import init_db, db_session
from database.database_models import Model, Job, Service, Setting, Dataset

# DEBUG = True

# configurations & resoureces

app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
manager = Manager()

class Request:
    def __init__(self, name, path, type, descript, data=None):
        self.name = name
        self.path = path
        self.type = type
        self.data = data
        self.descript = descript


class ModelRestfulAPI(Resource):
    def get(self, model_name):
        model = manager.getModel(model_name)
        data = request.json['data']
        return jsonify(model.predict(data))


api.add_resource(ModelRestfulAPI, '/predict/<string:model_name>')


class ServiceRestfulApi(Resource):
    def post(self, service_name):
        svc = Service.query.get(service_name)
        node_port = svc.node_port
        # 判断是否上传的是文件
        try:
            print(request.files)
            file = request.files['file']
            print("here")
            files = {'file': (file.filename, file.read(), file.content_type)}
            start = time() * 1000
            resp = Response(requests.post(url=f"http://82.156.5.94:{node_port}/predict", files=files)) # 服务器
            print("there")
            end = time() * 1000
        except:
            data = request.json
            print(data)
            print(type(data))
            start = time() * 1000
            resp = Response(requests.post(url=f"http://82.156.5.94:{node_port}/predict", json=data)) # 服务器
            print(resp)
            end = time() * 1000
        # resp = requests.get(url=f"http://82.156.5.94:{node_port}/test") # 服务器
        print(resp)
        # 更新performance
        if svc.first_access:
            svc.first_access = False
            svc.first_access_time = datetime.now()
        svc.last_access_time = datetime.now()
        delta = end - start
        access_times = svc.access_times
        average_response_time = svc.average_response_time
        svc.access_times += 1
        svc.average_response_time = (average_response_time * access_times + delta) / (access_times + 1)
        if delta > svc.max_response_time:
            svc.max_response_time = delta
        if delta < svc.min_response_time:
            svc.min_response_time = delta
        db_session.commit()
        return resp

class JobRestfulApi(Resource):
    def post(self, job_name):
        run_name = request.json['runName']
        env_var = request.json['variables']
        env_var = env_var.split(";")
        env = []
        if env_var[0] != '':
            for item in env_var:
                li = item.split("=")
                env.append({"name":li[0], "value":li[1]})
        args = request.json['args']
        
        v1 = client.BatchV1Api()
        job = Job.query.get(job_name)
        output_dataset = job.output_dataset
        ext = output_dataset.split('.')[-1]
        run_output_dataset = ''.join(output_dataset.split('.')[:-1]) + str(randint(0, 99999)) + '.' + ext
        body = job.job_json
        body['metadata']['name'] = run_name
        if job.dispatch == 'demand':
            body['spec']['template']['metadata']['labels']['job-name'] = run_name
            body['spec']['template']['spec']['containers'][0]['command'][5] = run_output_dataset
        else:
            body['spec']['jobTemplate']['metadata']['labels']['job-name'] = run_name
            body['spec']['jobTemplate']['spec']['template']['metadata']['labels']['job-name'] = run_name
            body['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['command'][5] = run_output_dataset
        response = {}
        if job.dispatch == 'demand':
            resp = v1.create_namespaced_job(namespace="default", body=body)
            response["scheduled"] = False
        else:
            resp = v1.create_namespaced_cron_job(namespace="default", body=body)
            response["scheduled"] = True
        response["args"] = args
        response["env"] = env
        response['jobName'] = job_name
        response["runName"] = run_name
        response["runID"] = resp.metadata.uid.split('-')[0]
        if resp.spec.suspend == False:
            response["status"] = "Running" 
        else:
            response["status"] = "Complete"
        dataset = Dataset(dataset_name=run_output_dataset, job_id=resp.metadata.uid.split('-')[0])
        db_session.add(dataset)
        db_session.commit()
        return jsonify(response)



api.add_resource(ServiceRestfulApi, '/api/v1/service/<string:service_name>/predict')
api.add_resource(JobRestfulApi, '/api/v1/job/<string:job_name>')


####### 以上是restapi #######


def add(name, path, type, descript) -> bool:
    if add_to_manager(name, path, type, descript):
        model = Model(model_name=name, model_path=path, type=type, descript=descript)
        db_session.add(model)
        db_session.commit()
        return True
    else: return False


def add_to_manager(name, path, type, descript) -> bool:
    if type == 'pmml':
        return manager.addModel(PmmlModel(path, name, descript))
    elif type == 'onnx':
        return manager.addModel(OnnxModel(path, name, descript))
    else:
        return False


def getInfo(request) -> dict:
    print('after get')
    print(request.json)
    print('after json')
    name = request.json.get('modelName')
    print(name)
    model = manager.getModel(name)
    return model.getInfo()


# route to access

@app.route('/', methods=['GET'])
def index():
    return render_template('./index.html')


# luohk
@app.route('/model-upload', methods=['POST'])
def upload():
    print(request.files)
    file = request.files['file']
    name = request.form.get('name')
    type = request.form.get('type')
    descript = request.form.get('descript')
    # save model -> ./models/model_name.pmml
    print("name:", name)
    print("type:", type)
    filename = name + '.' + type
    print("filename:", filename)
    path = os.path.join(os.path.join(os.getcwd(), f'model/'), filename)
    try:
        file.save(path)
    except:
        return jsonify({'status': False, "detailed": "duplicate"})
    print(file)

    # add into manager
    response_data = {}
    try:
        if add(name, path, type, descript):
            response_data['modelName'] = name
            response_data['modelType'] = type
            response_data['descript'] = descript
            response_data['updateTime'] = datetime.now()
            response_data['operation'] = ""
            response_data['status'] = True
            return jsonify(response_data)
        else: return jsonify({'status': False, "detailed": "duplicate"})
    except:
        return jsonify({'status': False, "detailed": "invalid model"})


# luohk
@app.route('/operate-model', methods=['POST'])
def operate_model():
    model_name = request.json["modelName"]
    operation = request.json["operation"]
    if operation == "delete":
        if manager.deleteModel(model_name):
            # requests.post(url="http://82.156.5.94:5000/operate-service", )
            res = Model.query.get(model_name)
            setting = Setting.query.get(model_name)
            file_path = res.model_path
            db_session.delete(res)
            if setting is not None:
                db_session.delete(setting)
            db_session.commit()
            svc_list = Service.query.filter(Service.model_name==res.model_name)
            for svc in svc_list:
                requests.post(url="http://127.0.0.1:5000/operate-service", json={
                    "serviceName": svc.service_name,
                    "type": "delete"
                })
            job_list = Job.query.filter(Job.model_name==res.model_name)
            for job in job_list:
                requests.post(url="http://127.0.0.1:5000/operate-job", json={
                    "jobName": job.job_name
                })
            print(file_path)
            os.remove(file_path)
            return jsonify({"status": True})
        else:
            return jsonify({"status": False, "detailed": ""})
    else:
        return jsonify({"status": False, "detailed": "operation not defined"})


# lichenyu ----------------------------------------------------------------
@app.route('/add-dataset', methods=['POST'])
def upload_file():
    # 只是先存下来，不急着处理，等调用job的时候再处理
    # try:
        print(request.files.get('file'))
        file = request.files['file']
        file_name = request.form['fileName'] + '.' + file.filename.split('.')[-1]
        print(file_name)
        # save data -> ./dataset/filename
        path = os.path.join(os.path.join(os.getcwd(), f'dataset/'), file_name)
        print(path)
        try:
            file.save(path)
        except:
            return jsonify({'status': False, "detailed": "duplicate"})
        return {'status': True}
    # except:
    #     return {'status': False, "detailed": "illegal filename"}
# lichenyu ----------------------------------------------------------------


@app.route('/operate-dataset', methods=['POST'])
def operate_dataset():
    dataset_name = request.json["dataset"]
    operation = request.json["operation"]
    path = "dataset/" + dataset_name
    if not os.path.exists(path):
        return jsonify({"status": False, "detailed": "file {} not exists".format(dataset_name)})
    if operation == "delete":
        try:
            os.remove(path)
        except:
            return jsonify({"status": False, "detailed": "can't delete {}".format(dataset_name)})
        res = Dataset.query.get(dataset_name)
        # 有一部分是存在数据库中的
        if res is not None:
            db_session.delete(res)
            db_session.commit()
        return jsonify({"status": True})
    elif operation == "download":   # TODO: 下载数据集
        return send_file(path, as_attachment=True)
    else:
        return "not implemented yet"


@app.route('/model-info', methods=['GET'])
def model_info():
    model_list = Model.query.all()
    ml = []
    for model in model_list:
        data = {
            "modelName": model.model_name,
            "modelType": model.type,
            "createTime": model.create_time
        }
        ml.append(data)
    response_data = {}
    response_data['modelList'] = ml
    return jsonify(response_data)

@app.route('/dataset-info', methods=['GET', 'POST'])
def dataset_info():
    if request.method == 'POST':
        model_name = request.json['modelName']
        print(model_name)
        setting = Setting.query.get(model_name)
        print(setting)
        if setting is not None and Job.query.get(setting.job_name) is not None:
            # 避免不点击高级设置，直接点击“立即执行”时默认job名冲突
            try:
                print("modelName not None")
                job_name = model_name.lower().replace("_", "-") + str(randint(0, 999999999))
                while Job.query.get(job_name) is not None:
                    job_name = model_name.lower().replace("_", "-") + str(randint(0, 999999999))
                setting.job_name = job_name
                setting.run_name = job_name + 'run1'
                print(job_name)
                db_session.commit()
            except:
                return jsonify({"status": False, "detailed": "setting load error"})
        if setting is None:
            try:
                job_name = model_name.lower().replace("_", "-") + str(randint(0, 999999999))
                new_setting = Setting(model_name=model_name, filename='test', ext='.py', job_name=job_name, job_description="default", 
                server_version="Python 3.7 - Script as a Service", dispatch="demand", run_name=job_name+'run1')
                db_session.add(new_setting)
                db_session.commit()
            except:
                return jsonify({"status": False, "detailed": "setting create error"})
    base_dir = os.path.join(os.getcwd(), 'dataset/')
    files = os.listdir(base_dir)
    fl = []
    for f in files:
        filepath = os.path.join(base_dir, f)
        size = os.path.getsize(filepath)
        type = f.split('.')[-1]
        time = ctime(os.path.getmtime(filepath))
        data = {
            'name': f,
            'size': size,
            'type': type,
            'source': "local",
            'createTime': time
        }
        fl.append(data)
    response_data = {}
    response_data['datasetList'] = fl
    return jsonify(response_data)


@app.route('/save-settings', methods=["POST"])
def save_settings():
    if not request.json.get('fileName'):
        try:
            setting = Setting.query.get(request.json['modelName'])
            if setting is None:
                return jsonify({'status': False, "detailed": "model not exists"})
            res = {}
            res["fileName"] = setting.filename
            res["ext"] = setting.ext
            res["jobName"] = setting.job_name
            res["jobDescription"] = setting.job_description
            res["serverVersion"] = setting.server_version
            res["variables"] = setting.variables
            res["args"] = setting.args
            res["dispatch"] = setting.dispatch
            res["runName"] = setting.run_name.lower().replace("_", "-")
        except:
            return jsonify({"status": False, "detailed": "setting update failure"})
        return jsonify(res)
    else:
        setting = Setting.query.get(request.json['modelName'])
        if setting is not None:
            setting.filename = request.json['fileName']
            setting.ext = request.json['ext']
            setting.job_name = request.json['jobName']
            setting.job_description = request.json['jobDescription']
            print(request.json['jobDescription'])
            setting.server_version = request.json['serverVersion']
            # setting.server_version = "test"
            setting.variables = request.json['variables']
            setting.args = request.json['args']
            setting.dispatch = request.json['dispatch']
            setting.run_name = request.json['runName'].lower().replace("_", "-")
            print("job name:", setting.job_name)
            db_session.commit()
        else:
            return jsonify({'status': False, "detailed": "model not exists"})
        return jsonify({"status": True})


@app.route('/model-descript', methods=['POST'])
def get_descript():
    print('prepare to get')
    total_info = getInfo(request)
    response_data = {}
    try:
        response_data['modelName'] = total_info['name']
        response_data['modelType'] = total_info['type']
        response_data['modelEngine'] = total_info['engine']
        response_data['descript'] = total_info['descript']
        response_data['algorithm'] = total_info['function']
        response_data['createTime'] = total_info['create_time']
    except:
        response_data['status'] = False
        response_data['detailed'] = total_info['type'] + 'not exist'
    return jsonify(response_data)


@app.route('/model-variable', methods=['POST'])
def get_variable():
    total_info = getInfo(request)
    response_data = {}
    try:
        response_data['inputVariables'] = total_info['input']
        response_data['outputVariables'] = total_info['output']
        print("input:", total_info['input'])
        print('output:', total_info['output'])
    except:
        response_data['status'] = False   
        response_data['detailed'] = "input/output variables error"
    return jsonify(response_data)


@app.route('/model-test', methods=['POST'])
def predict():
    name = request.json['modelName']
    data = request.json['data']
    print(data)
    try:
        model = manager.getModel(name)
        print(name)
        print(model)
        print(type(data))
        if type(data) == type('x'):
            data = json.loads(data)
        print(type(data))
        print("here")
        dict = manager.getModel(name).predict(data)
    except:
        return jsonify({'status': False, "detailed": "model or data invalid"})
    return jsonify(dict)

PORT = 80
def getPort():
    global PORT
    PORT += 1
    return PORT

from kubernetes import config, client
config.kube_config.load_kube_config()
# 部署服务
@app.route('/model-deploy-service', methods=['GET', 'POST'])
def get_model_deploy_data():
    if request.method == "POST":
        # 需要在这步生成docker service，并得到端口号（run flask in docker）
        model_name = request.json['modelName']
        model_type = request.json['modelType']
        service_name = request.json['serviceName']
        # server_version = request.json['serverVersion']
        server_version = "test" # TODO: 之后要把镜像替换进来
        print("top")
        cpu_reserve = str(request.json['cpuReserve'])
        memory_reserve = str(request.json['memoryReserve']) + "Mi"
        replicas = request.json['replicas']
        print("here")
        port = getPort()
        v1 = client.CoreV1Api()
        deployment_manifest = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"labels": {"app": service_name}, "name": service_name},
            "spec": {
                "replicas": replicas,
                "selector": {"matchLabels": {"app": service_name}},
                "template": {
                    "metadata": {"labels": {"app": service_name}},
                    "spec": {
                        "containers": [
                            {
                                "name": server_version,
                                "image": server_version,
                                "ports": [{"containerPort": 80}],
                                "command": ["python", "app.py" , "-m", model_name, "-t", model_type],
                                # "command": ["python", "rest.py"],
                                "imagePullPolicy": "IfNotPresent",
                                "resources": {
                                    "cpu": cpu_reserve,
                                    "storage": memory_reserve
                                },
                                "volumeMounts": [{
                                    "name": "model",
                                    "mountPath": "/model",
                                },
                                {
                                    "name": "dataset",
                                    "mountPath": "/dataset",
                                },
                                {
                                    "name": "jdk",
                                    "mountPath": "/usr/lib/jvm/java-11-openjdk-amd64",
                                },
                                {
                                    "name": "app",
                                    "mountPath": "/app",
                                }
                                ]
                            },
                        ],
                        "volumes":[
                            {
                                "name": "model",
                                "hostPath": {
                                    "path": "/home/backendTeam/DaaS-Deployer/model",
                                    "type": "Directory"
                                }
                            },
                            {
                                "name": "dataset",
                                "hostPath":{
                                    "path": "/home/backendTeam/DaaS-Deployer/dataset",
                                    "type": "Directory"
                                }
                            },
                            {
                                "name":"jdk",
                                "hostPath":
                                {
                                    "path":"/usr/lib/jvm/java-8-openjdk-amd64",
                                    "type": "Directory"
                                }
                            },
                            {
                                "name":"app",
                                "hostPath":
                                {
                                    "path":"/home/backendTeam/job-service",
                                    "type": "Directory"
                                }
                            }
                        ],
                    },
                },
            },
        }
        service_manifest = {
            "kind": "Service",
            "apiVersion": "v1",
            "metadata": {
                "name": service_name
            },
            "spec": {
                "selector": {
                    "app": service_name
                },
                "ports": [
                    {
                        "protocol": "TCP",
                        "port": port,   # 外面的
                        "targetPort": 80    # 里面的
                    }
                ],
                "type": "NodePort"
            }
        }
        response_data = {}
        try:
            resp = client.AppsV1Api().create_namespaced_deployment(namespace="default", body=deployment_manifest)
        except:
            return jsonify({"status": False, "detailed": "deployment create failure!"})
        if resp.kind == 'Status':
            return jsonify({"status": False, "detailed": "deployment create failure!"})
        else:
            response_data['status'] = True
        
        try:
            resp = v1.create_namespaced_service(namespace="default", body=service_manifest)
        except:
            return jsonify({"status": False, "detailed": "service create failure!"})
        if resp.kind == 'Status':
            return jsonify({"status": False, "detailed": "service create failure!"})
        else:
            response_data['status'] = True
        
        try:
            s = Service(service_name=service_name, model_name=model_name, cpu=cpu_reserve, memory=memory_reserve, service_version=request.json['serverVersion'],\
                status=True, replicas=replicas, create_time=resp.metadata.creation_timestamp, node_port=resp.spec.ports[0].node_port, model_type=model_type)
            db_session.add(s)
            db_session.commit()
        except:
            return jsonify({"status": False, "detailed": "database add failure"})

        return jsonify(response_data)
    else:
        url = "http://82.156.5.94:5000/api/v1/service/"   # 如果在服务器上
        # url = "http://127.0.0.1:5000/api/v1/service/"            # 如果在本地
        return jsonify({"restfulUrl": url})


@app.route('/service-info', methods=['POST'])
def get_service_info():
    service_name = request.json['serviceName']
    svc = Service.query.get(service_name)
    if svc is None:
        return jsonify({'status': False, "detailed": "service not exists"})
    label_selector = "app=" + service_name
    v1 = client.CoreV1Api()
    pod_list = v1.list_namespaced_pod(namespace="default", label_selector=label_selector, watch=False).items
    response_data = {}
    response_data['restfulUrl'] = "http://82.156.5.94:5000/api/v1/service/" # 服务器上
    # response_data['restfulUrl'] = "http://127.0.0.1:5000/api/v1/service/"   # 本地
    response_data['createTime'] = svc.create_time
    list = []
    for pod in pod_list:
        data = {
            "name": pod.metadata.name,
            "status": pod.status.phase
        }
        list.append(data)
    response_data['podList'] = list
    response_data['modelName'] = svc.model_name
    response_data['cpuReserve'] = svc.cpu
    response_data['memoryReserve'] = svc.memory
    response_data['function'] = "predict"
    response_data['acessTimes'] = svc.access_times
    if svc.min_response_time == 99999.9:
        response_data['maxResponseTime'] = "-"
        response_data['minResponseTime'] = "-"
        response_data['averageResponseTime'] = "-"
    else:
        response_data['averageResponseTime'] = svc.average_response_time
        response_data['maxResponseTime'] = svc.max_response_time
        response_data['minResponseTime'] = svc.min_response_time
    response_data['firstAccessTime'] = svc.first_access_time
    response_data['lastAccessTime'] = svc.last_access_time
    return jsonify(response_data)


@app.route('/operate-pod', methods=['POST'])
def restart_pod():
    podName = request.json['podName']
    v1 = client.CoreV1Api()
    try:
        resp = v1.delete_namespaced_pod(namespace="default", name=podName)
    except:
        return jsonify({"status": False, "detailed": "delete pod error"})
    response_data = {}
    if resp.kind == 'Status':
        response_data['status'] = False
    else:
        response_data['status'] = True
    return jsonify(response_data)


@app.route('/env-version', methods=['GET'])
def get_env_version():
    return jsonify({"version": [f'Python 3.{x} - Script as a Service' for x in range(7, 11)]})


@app.route('/operate-service', methods=["POST"])
def operate_service():
    service_name = request.json['serviceName']
    svc = Service.query.get(service_name)
    if svc is None:
        return jsonify({'status': False, "detailed": "service not exists"})
    app_v1 = client.AppsV1Api()
    core_v1 = client.CoreV1Api()
    try:
        # todo: 判断k8s操作后的返回值
        if request.json['type'] == 'delete':
            app_v1.delete_namespaced_deployment(name=service_name, namespace="default")
            core_v1.delete_namespaced_service(name=service_name, namespace="default")
            db_session.delete(svc)
            db_session.commit()
        elif request.json['type'] == 'modify':
            replicas = request.json['replicas'] # 传的string, 要不统一成int?
            resp = app_v1.read_namespaced_deployment(name=service_name, namespace="default")
            resp.spec.replicas = replicas
            app_v1.replace_namespaced_deployment(name=service_name, namespace="default", body=resp)
            svc.replicas = replicas
            db_session.commit()
        elif request.json['type'] == 'pause':
            svc.status = False
            db_session.commit()
            resp = app_v1.read_namespaced_deployment(name=service_name, namespace="default")
            resp.spec.replicas = 0
            app_v1.replace_namespaced_deployment(name=service_name, namespace='default', body=resp)
        else: 
            svc.status = True
            db_session.commit()
            resp = app_v1.read_namespaced_deployment(name=service_name, namespace="default")
            resp.spec.replicas = svc.replicas
            app_v1.replace_namespaced_deployment(name=service_name, namespace='default', body=resp)
    except:
        return jsonify({'status': False, "detailed": "database or k8s error"})
    return jsonify({"status": True})


# 部署job
@app.route('/model-deploy-job', methods=['POST'])
def deploy_job():
    if request.json.get('jobName'): # 方便测试用
        job_name = request.json['jobName']
        job_description = request.json['jobDescription']
        server_version = request.json['serverVersion']
        input_dataset = request.json['inputDataset']
        output_dataset = request.json['outputDataset']
        ext = output_dataset.split('.')[-1]
        run_output_dataset = ''.join(output_dataset.split('.')[:-1]) + str(randint(0, 99999)) + '.' + ext
        env = request.json['variables']
        args = request.json['args'] # -i input -o output -t type
        dispatch = request.json['dispatch']
        run_name = request.json['runName']
        model_name = request.json['modelName']
        model_type = request.json['modelType']
        server_version = "test"
    else:
        model_name = request.json['modelName']
        setting = Setting.query.get(model_name)
        if setting is None:
            return jsonify({'status': False, "detailed": "setting not exists"})
        job_name = setting.job_name
        print(job_name)
        job_description = setting.job_description
        # server_version = setting.server_version
        server_version = "test" # TODO: 要换
        input_dataset = request.json['inputDataset']
        # print(input_dataset)
        output_dataset = request.json['outputDataset']
        ext = output_dataset.split('.')[-1]
        run_output_dataset = ''.join(output_dataset.split('.')[:-1]) + str(randint(0, 99999)) + '.' + ext
        if setting.variables is None:
            env = []
        else:
            env_li = setting.variables.split(';')
            print(env_li)
            env = []
            if env_li[0] != '':
                for item in env_li:
                    dic = {}
                    l = item.split("=")
                    dic["name"] = l[0]
                    dic["value"] = l[1]
                    env.append(dic)
        dispatch = setting.dispatch
        run_name = setting.run_name
        args = setting.args
        if args == '' or args is None:
            args = []
        else:
            args = args.split(' ')
        dispatch = setting.dispatch
        model_type = request.json['modelType']
        print("model_type:", model_type)
    batch_v1 = client.BatchV1Api()

    if dispatch == 'demand':
        job_manifest = {
            "kind": "Job",
            "apiVersion": "batch/v1",
            "metadata": {
                "name": run_name,
                "labels": {
                    "app": job_name,
                }
            },
            "spec": {
                "template": {
                    "metadata":{
                        "labels": {
                            "app": run_name,
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": server_version,
                                "image": server_version,
                                "ports": [{"containerPort": 80}],
                                "command": ["python", "rest.py" , "-i", input_dataset, "-o", run_output_dataset, "-m", model_name, "-t", model_type] + args,
                                # "command": ["python", "rest.py"],
                                "imagePullPolicy": "IfNotPresent",
                                "env": env,
                                "volumeMounts": [{
                                    "name": "model",
                                    "mountPath": "/model",
                                },
                                {
                                    "name": "dataset",
                                    "mountPath": "/dataset",
                                },
                                {
                                    "name": "jdk",
                                    "mountPath": "/usr/lib/jvm/java-11-openjdk-amd64",
                                },
                                {
                                    "name": "app",
                                    "mountPath": "/app",
                                }
                                ]
                            },
                        ],
                        "volumes":[
                            {
                                "name": "model",
                                "hostPath": {
                                    "path": "/home/backendTeam/DaaS-Deployer/model",
                                    "type": "Directory"
                                }
                            },
                            {
                                "name": "dataset",
                                "hostPath":{
                                    "path": "/home/backendTeam/DaaS-Deployer/dataset",
                                    "type": "Directory"
                                }
                            },
                            {
                                "name":"jdk",
                                "hostPath":
                                {
                                    "path":"/usr/lib/jvm/java-8-openjdk-amd64",
                                    "type": "Directory"
                                }
                            },
                            {
                                "name":"app",
                                "hostPath":
                                {
                                    "path":"/home/backendTeam/job-service",
                                    "type": "Directory"
                                }
                            }
                        ],
                        "restartPolicy": "Never"
                    }
                },
                
            }
        }
        print(job_manifest)
        try:
            resp = batch_v1.create_namespaced_job(namespace="default", body=job_manifest)
        except:
            return jsonify({"status": False, "detailed": "job create failure!"})
    else:
        if request.json.get('option') is None:
            option = 0
        else:
            option = int(request.json['option'])
        schedule = ['0' for i in range(0, option)] + ['*' for i in range(0, 5-option)]
        schedule = ' '.join(schedule)
        job_manifest = {
            "kind": "CronJob",
            "apiVersion": "batch/v1",
            "metadata": {
                "name": run_name,
                "labels":{
                    "app": job_name
                }
            },
            "spec": {
                "schedule": schedule,
                "metadata":{
                    "labels":{
                        "app": job_name
                    }
                },
                "jobTemplate": {
                    "metadata":{
                        "labels":{
                            "app": run_name
                        }
                    },
                    "spec":{
                        "template": {
                            "metadata":{
                                "labels": {
                                    "app": run_name,
                                }
                            },
                            "spec": {
                                "containers": [
                                    {
                                        "name": server_version,
                                        "image": server_version,
                                        "ports": [{"containerPort": 80}],
                                        "command": ["python", "rest.py" , "-i", input_dataset, "-o", run_output_dataset, "-m", model_name, "-t", model_type] + args,
                                        # "command": ["python", "rest.py"],
                                        "imagePullPolicy": "IfNotPresent",
                                        "env": env,
                                        "volumeMounts": [{
                                            "name": "model",
                                            "mountPath": "/model",
                                        },
                                        {
                                            "name": "dataset",
                                            "mountPath": "/dataset",
                                        },
                                        {
                                            "name": "jdk",
                                            "mountPath": "/usr/lib/jvm/java-11-openjdk-amd64",
                                        },
                                        {
                                            "name": "app",
                                            "mountPath": "/app",
                                        }
                                        ]
                                    },
                                ],
                                "volumes":[
                                    {
                                        "name": "model",
                                        "hostPath": {
                                            "path": "/home/backendTeam/DaaS-Deployer/model",
                                            "type": "Directory"
                                        }
                                    },
                                    {
                                        "name": "dataset",
                                        "hostPath":{
                                            "path": "/home/backendTeam/DaaS-Deployer/dataset",
                                            "type": "Directory"
                                        }
                                    },
                                    {
                                        "name":"jdk",
                                        "hostPath":
                                        {
                                            "path":"/usr/lib/jvm/java-8-openjdk-amd64",
                                            "type": "Directory"
                                        }
                                    },
                                    {
                                        "name":"app",
                                        "hostPath":
                                        {
                                            "path":"/home/backendTeam/job-service",
                                            "type": "Directory"
                                        }
                                    }
                                ],
                                "restartPolicy": "Never"
                            }
                        },
                    }
                }
                
            }
        }
        try:
            resp = batch_v1.create_namespaced_cron_job(namespace="default", body=job_manifest)
        except:
            return jsonify({"status": False, "detailed": "cronjob create failure!"})
    
    if resp.kind == 'Status':
        response_data = {}
        response_data['status'] = False
    else:
        response_data = {}
        response_data['status'] = True
        response_data['jobName'] = job_name
    try:
        dataset = Dataset(dataset_name=run_output_dataset, job_id=resp.metadata.uid.split('-')[0])
        db_session.add(dataset)
        db_session.commit()
    except:
        return jsonify({"status": False, "detailed": "dataset create failure!"})
    try:
        job = Job(job_name=job_name, job_json=job_manifest, dispatch=dispatch, job_description=job_description, server_version=setting.server_version, 
        model_name=model_name, model_type=model_type, input_dataset=input_dataset, output_dataset=output_dataset)
        db_session.add(job)
        db_session.commit()
    except:
        return jsonify({"status": False, "detailed": "job database update failure!"})
    return jsonify(response_data)


@app.route('/operate-job', methods=['POST'])
def operate_job():
    # 默认删除
    job_name = request.json['jobName']
    res = Job.query.get(job_name)
    if res is None:
        return jsonify({"status": False, "detailed": "job not exist"})
    label_selector = "app=" + res.job_name
    print(label_selector)
    batch_v1 = client.BatchV1Api()
    # TODO: 好像有bug
    try:
        if res.dispatch == 'demand':
            print("here")
            job_run_list = batch_v1.list_namespaced_job(namespace="default", label_selector=label_selector).items
            for run in job_run_list:
                print("in the run")
                batch_v1.delete_namespaced_job(name=run.metadata.name, namespace="default")
                core_v1 = client.CoreV1Api()
                label_selector = "app=" + run.metadata.name
                print(label_selector)
                pod_list = core_v1.list_namespaced_pod(namespace="default", label_selector=label_selector).items
                print(pod_list)
                for pod in pod_list:
                    core_v1.delete_namespaced_pod(name=pod.metadata.name, namespace="default")
        else:
            job_run_list = batch_v1.list_namespaced_cron_job(namespace="default", label_selector=label_selector).items
            for run in job_run_list:
                # patch = {"spec": {"suspend": True}}
                # batch_v1.patch_namespaced_cron_job(name=run.metadata.name, body=patch, namespace="default")
                batch_v1.delete_namespaced_cron_job(name=run.metadata.name, namespace="default")
    except:
        return jsonify({"status": False, "detailed": "job delete failure!"})
    # res = Dataset.query
    db_session.delete(res)
    db_session.commit()
    return jsonify({"status": True})

@app.route('/operate-run', methods=['POST'])
def operate_run():
    run_name = request.json['runName']
    job_name = request.json['jobName']
    job = Job.query.get(job_name)
    if job is None:
        return jsonify({"status": False, "detailed": "job not exist"})
    type = request.json['type']
    batch_v1 = client.BatchV1Api()
    try:
        if type == "delete":
            if job.dispatch == 'demand':
                batch_v1.delete_namespaced_job(name=run_name, namespace="default")
                core_v1 = client.CoreV1Api()
                label_selector = "app=" + run_name
                pod_list = core_v1.list_namespaced_pod(namespace="default", label_selector=label_selector).items
                for pod in pod_list:
                    core_v1.delete_namespaced_pod(name=pod.metadata.name, namespace="default")
            else:
                batch_v1.delete_namespaced_cron_job(name=run_name, namespace="default")
        elif type == "pause":
            patch = {"spec": {"suspend": True}}
            if job.dispatch == 'demand':
                batch_v1.patch_namespaced_job(name=run_name, body=patch, namespace="default")
            else:
                batch_v1.patch_namespaced_cron_job(name=run_name, body=patch, namespace="default")
        elif type == "result":
            run_id = request.json['runId']
            dataset = Dataset.query.get(run_id)
            if dataset is None:
                return {"status": False, "detail": "this dataset has been removed"}
            with open('dataset/'+dataset.dataset_name, "r") as f:
                res = f.read()
            return jsonify({"status": True, "res": res})
        else:   # restart
            patch = {"spec": {"suspend": False}}
            if job.dispatch == 'demand':
                batch_v1.patch_namespaced_job(name=run_name, body=patch, namespace="default")
            else:
                batch_v1.patch_namespaced_cron_job(name=run_name, body=patch, namespace="default")
    except:
        return jsonify({"status": False, "detailed": "operation failure!"})
    return jsonify({"status": True})


@app.route('/job-variable', methods=['POST'])
def get_job_variable():
    job_name = request.json['jobName']
    job = Job.query.get(job_name)
    if job is None:
        return jsonify({"status": False, "detailed": "job not exist"})
    response_data = {}
    if job.dispatch == "demand":
        response_data['env'] = job.job_json['spec']['template']['spec']['containers'][0]['env']
        response_data['args'] = job.job_json['spec']['template']['spec']['containers'][0]['command'][10:]
    else:
        response_data['env'] = job.job_json['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['env']
        response_data['args'] = job.job_json['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['command'][10:]
    return jsonify(response_data)


@app.route('/job-info', methods=['POST'])
def job_info():
    job_name = request.json['jobName']
    job = Job.query.get(job_name)
    if job is None:
        return jsonify({"status": False, "detailed": "job not exist"})
    url = "http://82.156.5.94:5000/api/v1/job/"   # 服务器
    # url = "http://127.0.0.1:5000/api/v1/job/"   # 本地
    batch_v1 = client.BatchV1Api()
    label_selector = 'app=' + job_name
    try:
        if job.dispatch == 'demand':
            job_list = batch_v1.list_namespaced_job(namespace="default", label_selector=label_selector).items
        else:
            job_list = batch_v1.list_namespaced_cron_job(namespace="default", label_selector=label_selector).items
    except:
        return jsonify({"status": False, "detailed": "job search failure!"})
    response_data = {}
    if len(job_list) == 0 or job_list[0].kind != 'Status':
        response_data['status'] = True
        response_data['dispatch'] = job.dispatch
        response_data['serverVersion'] = job.server_version
        response_data['createTime'] = job.create_time
        response_data['modelName'] = job.model_name
        response_data['url'] = url
        if job.dispatch == 'demand':
            list = []
            for job in job_list:
                if job.spec.suspend:
                    status = 'Suspend'
                    completion_time = None
                    delta = None
                elif job.status.completion_time is None:
                    status = 'Running'
                    completion_time = None
                    delta = None
                else:
                    status = 'Complete'
                    completion_time = job.status.completion_time
                    delta = (completion_time - job.metadata.creation_timestamp).seconds
                
                data = {
                    "id": job.metadata.uid.split('-')[0],
                    "name": job.metadata.name,
                    "status": status,
                    "createTime": job.metadata.creation_timestamp,
                    "duration": delta,
                    # "env": job.spec.template.spec.containers[0].env,
                    # "args": job.spec.template.spec.containers[0].command[10:]
                }
                list.append(data)
            response_data['runList'] = list
        else:
            res = []
            for job in job_list:
                label_selector = 'app=' + job.metadata.name
                second_list = batch_v1.list_namespaced_job(namespace="default", label_selector=label_selector).items
                list = []
                for second in second_list:
                    if second.spec.suspend:
                        status = 'Suspend'
                        completion_time = None
                        delta = None
                    elif second.status.completion_time is not None: 
                        status = 'Complete'
                        completion_time = second.status.completion_time
                        delta = (completion_time - second.metadata.creation_timestamp).seconds  # 会有bug
                    else:
                        status = 'Running'
                        completion_time = None
                        delta = None
                    data = {
                        "id": second.metadata.uid.split('-')[0],
                        "name": second.metadata.name,
                        "status": status,
                        "createTime": second.metadata.creation_timestamp,
                        "duration": delta,
                        # "env": second.spec.template.spec.containers[0].env,
                        # "args": second.spec.template.spec.containers[0].command[10:]
                    }
                    list.append(data)
                cron_job = {
                    "id": job.metadata.uid.split('-')[0],
                    "name": job.metadata.name,
                    "createTime": job.metadata.creation_timestamp,
                    "job_list": list
                }
                res.append(cron_job)
            response_data['runList'] = res    
    else:
        response_data['status'] = False
    print(response_data)
    return jsonify(response_data)

@app.route('/model-run-job', methods=['POST'])
def run_job():
    job_name = request.json['jobName']
    run_name = request.json['runName']
    
    v1 = client.BatchV1Api()
    job = Job.query.get(job_name)
    if job is None:
        return jsonify({"status": False, "detailed": "job not exist"})
    output_dataset = job.output_dataset
    ext = output_dataset.split('.')[-1]
    run_output_dataset = ''.join(output_dataset.split('.')[:-1]) + str(randint(0, 99999)) + '.' + ext
    body = job.job_json
    body['metadata']['name'] = run_name
    if job.dispatch == 'demand':
        body['spec']['template']['metadata']['labels']['job-name'] = run_name
        body['spec']['template']['spec']['containers'][0]['command'][5] = run_output_dataset
    else:
        body['spec']['jobTemplate']['metadata']['labels']['job-name'] = run_name
        body['spec']['jobTemplate']['spec']['template']['metadata']['labels']['job-name'] = run_name
        body['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['command'][5] = run_output_dataset
    try:
        if job.dispatch == 'demand':
            resp = v1.create_namespaced_job(namespace="default", body=body)
        else:
            resp = v1.create_namespaced_cron_job(namespace="default", body=body)
    except:
        return jsonify({"status": False, "detailed": "job create failure!"})
    try:
        dataset = Dataset(dataset_name=run_output_dataset, job_id=resp.metadata.uid.split('-')[0])
        db_session.add(dataset)
        db_session.commit()
    except:
        return jsonify({"status": False, "detailed": "dataset create failure!"})
    return jsonify({"status": True})


@app.route('/get-deploy-info', methods=['POST'])
def get_deploy_info():
    model_name = request.json['modelName']
    model_type = request.json['modelType']
    service_list = Service.query.filter(Service.model_name==model_name, Service.model_type==model_type).all()
    job_list = Job.query.filter(Job.model_name==model_name, Job.model_type==model_type).all()
    response_data = {}
    # name, type , start_time, status
    sl = []
    for service in service_list:
        s_info = {}
        s_info['name'] = service.service_name
        s_info['type'] = "Service"
        s_info['startTime'] = service.create_time
        if service.status:
            s_info['status'] = "Running"
        else:
            s_info['status'] = "Pending"
        sl.append(s_info)
    response_data['serviceList'] = sl
    jl = []
    for job in job_list:
        j_info = {}
        j_info['name'] = job.job_name
        j_info['type'] =  "Job"
        j_info['startTime'] = job.create_time
        j_info['status'] = "Running"
        jl.append(j_info)
    response_data['serviceList'] = sl
    response_data['jobList'] = jl
    return jsonify(response_data)


# TODO: 代码返回啥
@app.route('/generate-script', methods=['POST'])
def generate_script():
    input_dataset = request.json['inputDataset']
    output_dataset = request.json['outputDataset']
    if os.path.exists(f"dataset/{output_dataset}"):
        return jsonify({"status": False, "detailed": "Name conflict"})
    return jsonify({"code": r'''import json
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
    elif ext == 'zip':
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
        pass"'''})


@app.route('/download/<string:filename>')
def download(filename):
    path = "dataset/" + filename
    return send_file(path,as_attachment=True)



def import_models():
    for model in Model.query.all():
        add_to_manager(model.model_name, model.model_path, model.type, model.descript)


if __name__ == '__main__':
    init_db()
    import_models()
    app.run(host='0.0.0.0', port=5000)
