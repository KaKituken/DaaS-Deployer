from email.mime import base
from http import server
import re
from time import time, ctime
import os
import requests
from manager import Manager
from models import AbstractModel, PmmlModel, OnnxModel
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api
from preprocess_file import preprocess_csv, preprocess_zip
from database.database import init_db, db_session
from database.database_models import Model, Job, Service

# DEBUG = True

# configurations & resoureces

app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)
CORS(app, resources={r'/*': {'origins': '*'}})
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
        node_port = Service.query.get(service_name).node_port
        resp = requests.post(url=f"127.0.0.1:{node_port}/predict", data=request.json) # 本地
        # resp = requests.post(url=f"82.156.5.94:{node_port}/predict", data=request.json) # 服务器
        return resp

class JobRestfulApi(Resource):
    def post(self, job_name):
        run_name = request.json['runName']
        env_var = request.json['variables']
        args = request.json['args']
        
        v1 = client.BatchV1Api()
        job = Job.query.get(job_name)
        body = job.job_json
        body['metadata']['name'] = run_name
        body['spec']['template']['metadata']['labels']['job-name'] = run_name
        response = {}
        if job.dispatch == 'demand':
            resp = v1.create_namespaced_job(namespace="default", body=body)
            response["scheduled"] = False
        else:
            resp = v1.create_namespaced_cron_job(namespace="default", body=body)
            response["scheduled"] = True
        response["args"] = args
        response["env"] = env_var
        response['jobName'] = job_name
        response["runName"] = run_name
        response["runID"] = resp.metadata.uid.split('-')[0]
        if resp.spec.suspend == False:
            response["status"] = "Running" 
        else:
            response["status"] = "Complete"
        return jsonify({"status": True})



api.add_resource(ServiceRestfulApi, '/app/v1/service/<string:service_name>/predict')
api.add_resource(JobRestfulApi, '/app/v1/job/<string:job_name>')


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


@app.route('/model-upload/test', methods=['POST'])
def upload_test():
    print(request.json)
    # test = json.loads(request.json)
    # print(test)
    path = request.json['file']
    name = request.json['name']
    type = request.json['type']
    descript = request.json['descript']
    print(path)

    # add into manager
    response_data = {}
    if add(name, path, type, descript):
        response_data['modelName'] = name
        response_data['modelType'] = type
        response_data['descript'] = descript
        response_data['updateTime'] = ctime()
        response_data['operation'] = ""
        response_data['status'] = True
        return jsonify(response_data)
    else:
        return jsonify({'status': False})


@app.route('/model-upload', methods=['POST'])
def upload():
    print(request.files)
    file = request.files['file']
    name = request.form.get('name')
    type = request.form.get('type')
    descript = request.form.get('descript')
    filename = name + '.' + type
    # save model -> ./models/model_name.pmml
    path = os.path.join(os.path.join(os.getcwd(), f'model/'), filename)
    file.save(path)
    print(file)

    # add into manager
    response_data = {}
    if add(name, path, type, descript):
        response_data['modelName'] = name
        response_data['modelType'] = type
        response_data['descript'] = descript
        response_data['updateTime'] = ctime()
        response_data['operation'] = ""
        response_data['status'] = True
        return jsonify(response_data)
    else:
        return jsonify({'status': False})


@app.route('/upload-file', methods=['POST'])
def upload_file():
    # 只是先存下来，不急着处理，等调用job的时候再处理
    file = request.files['file']
    # save data -> ./dataset/filename
    path = os.path.join(os.path.join(os.getcwd(), f'dataset/'), file.filename)
    file.save(path)
    return {'status': True}

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

@app.route('/dataset-info', methods=['GET'])
def dataset_info():
    base_dir = os.path.join(os.getcwd(), 'dataset/')
    files = os.listdir(base_dir)
    fl = []
    for f in files:
        filepath = os.path.join(base_dir, f)
        size = os.path.getsize(filepath)
        type = f.split('.')[-1]
        time = os.path.getmtime(filepath)
        data = {
            'fileName': f,
            'fileSize': size,
            'fileType': type,
            'fileSource': "local",
            'fileUpdateTime': time
        }
        fl.append(data)
    response_data = {}
    response_data['fileList'] = fl
    return jsonify(response_data)

@app.route('/model-descript', methods=['POST'])
def get_descript():
    print('prepare to get')
    total_info = getInfo(request)
    response_data = {}
    response_data['modelName'] = total_info['name']
    response_data['modelType'] = total_info['type']
    response_data['modelEngine'] = total_info['engine']
    response_data['descript'] = total_info['descript']
    response_data['algorithm'] = total_info['function']
    response_data['createTime'] = total_info['create_time']
    return jsonify(response_data)

    
@app.route('/model-variable', methods=['POST'])
def get_variable():
    total_info = getInfo(request)
    response_data = {}
    response_data['inputVariables'] = total_info['input']
    response_data['outputVariables'] = total_info['output']
    return jsonify(response_data)


@app.route('/model-test', methods=['POST'])
def predict():
    name = request.json['modelName']
    data = request.json['data']
    return jsonify(manager.getModel(name).predict(data))

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
        server_version = request.json['serverVersion']
        cpu_reserve = request.json['cpuReverse']
        memory_reserve = request.json['memoryReserve']
        replicas = request.json['replicas']
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
        
        resp = client.AppsV1Api().create_namespaced_deployment(namespace="default", body=deployment_manifest)
        resp = v1.create_namespaced_service(namespace="default", body=service_manifest)
        if resp.kind == 'Status':
            response_data['status'] = False
            return jsonify(response_data)
        else:
            response_data['status'] = True
        
        s = Service(service_name=service_name, model_name=model_name, cpu=cpu_reserve, memory=memory_reserve, service_version=server_version,\
            status=True, replicas=replicas, create_time=resp.metadata.creation_timestamp, node_port=resp.spec.ports[0].node_port, model_type=model_type)
        db_session.add(s)
        db_session.commit()
        return jsonify(response_data)
    else:
        # url = "http://82.156.5.94:5000/api/v1/service/"   # 如果在服务器上
        url = "http://127.0.0.1:5000/api/v1/service/"            # 如果在本地
        return jsonify({"restfulUrl": url})


@app.route('/service-info', methods=['POST'])
def get_service_info():
    service_name = request.json['serviceName']
    svc = Service.query.get(service_name)
    label_selector = "app=" + service_name
    v1 = client.CoreV1Api()
    pod_list = v1.list_namespaced_pod(namespace="default", label_selector=label_selector, watch=False).items
    response_data = {}
    # response_data['restfulUrl'] = "http://82.156.5.94:5000/api/v1/service/" # 服务器上
    response_data['restfulUrl'] = "http://127.0.0.1:5000/api/v1/service/"   # 本地
    response_data['createTime'] = svc.create_time
    # TODO: to json
    list = []
    for pod in pod_list:
        data = {
            "name": pod.metadata.name,
            "status": pod.status.phase
        }
        list.append(data)
    response_data['pod_list'] = list
    response_data['model_name'] = svc.model_name
    return jsonify(response_data)


@app.route('/operate-pod', methods=['POST'])
def restart_pod():
    podName = request.json['podName']
    v1 = client.CoreV1Api()
    resp = v1.delete_namespaced_pod(namespace="default", name=podName)
    response_data = {}
    if resp.kind == 'Status':
        response_data['status'] = False
    else:
        response_data['status'] = True
    return jsonify(response_data)


@app.route('/env-version', methods=['GET'])
def get_env_version():
    return jsonify({"version": [f'Python 3.{x} - Script as a Service' for x in range(6, 10)]})


@app.route('/operate-service', methods=["POST"])
def operate_service():
    service_name = request.json['serviceName']
    svc = Service.query.get(service_name)
    app_v1 = client.AppsV1Api()
    core_v1 = client.CoreV1Api()
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
        resp = app_v1.read_namespaced_deployment(name=service_name, namespace="default")
        resp.spec.replicas = svc.replicas
        app_v1.replace_namespaced_deployment(name=service_name, namespace='default', body=resp)
    return jsonify({"status": True})


# 部署job
@app.route('/model-deploy-job', methods=['POST'])
def deploy_job():
    job_name = request.json['jobName']
    job_description = request.json['jobDescription']
    server_version = request.json['serverVersion']
    input_dataset = request.json['inputDataset']
    output_dataset = request.json['outputDataset']
    env = request.json['variables']
    args = request.json['args'] # -i input -o output -t type
    dispatch = request.json['dispatch']
    run_name = request.json['runName']
    model_name = request.json['modelName']
    model_type = request.json['modelType']
    batch_v1 = client.BatchV1Api()
    if dispatch == 'demand':
        job_manifest = {
            "kind": "Job",
            "apiVersion": "batch/v1",
            "metadata": {
                "name": run_name
            },
            "spec": {
                "template": {
                    "metadata":{
                        "labels": {
                            "app": job_name,
                            "job-name": run_name
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": server_version,
                                "image": server_version,
                                "ports": [{"containerPort": 80}],
                                "command": ["python", "rest.py" , "-i", input_dataset, "-o", output_dataset, "-m", model_name, "-t", model_type],
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
                            }
                        ],
                        "restartPolicy": "Never"
                    }
                },
                
            }
        }
        resp = batch_v1.create_namespaced_job(namespace="default", body=job_manifest)
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
                                        # "command": ["python", "rest.py" , "-m", model_name, "-t", model_type],
                                        "command": ["python", "rest.py"],
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
                                    }
                                ],
                                "restartPolicy": "Never"
                            }
                        },
                    }
                }
                
            }
        }
        resp = batch_v1.create_namespaced_cron_job(namespace="default", body=job_manifest)
    
    response_data = {}
    if resp.kind == 'Status':
        response_data['status'] = False
    else:
        response_data['status'] = True
    job = Job(job_name=job_name, job_json=job_manifest, dispatch=dispatch, job_description=job_description, server_version=server_version, model_name=model_name, model_type=model_type)
    db_session.add(job)
    db_session.commit()
    return jsonify(response_data)


@app.route('/operate-job', methods=['POST'])
def operate_job():
    # 默认删除
    job_name = request.json['jobName']
    res = Job.query.get(job_name)
    label_selector = "app=" + res.job_name
    batch_v1 = client.BatchV1Api()
    if res.dispatch == 'demand':
        job_run_list = batch_v1.list_namespaced_job(namespace="default", label_selector=label_selector).items
        for run in job_run_list:
            patch = {"spec": {"suspend": True}}
            batch_v1.patch_namespaced_job(name=run.metadata.name, body=patch, namespace="default")
            batch_v1.delete_namespaced_job(name=run.metadata.name, namespace="default")
        
    else:
        job_run_list = batch_v1.list_namespaced_cron_job(namespace="default", label_selector=label_selector).items
        for run in job_run_list:
            # patch = {"spec": {"suspend": True}}
            # batch_v1.patch_namespaced_cron_job(name=run.metadata.name, body=patch, namespace="default")
            batch_v1.delete_namespaced_cron_job(name=run.metadata.name, namespace="default")
    db_session.delete(res)
    db_session.commit()
    return jsonify({"status": True})

@app.route('/operate-run', methods=['POST'])
def operate_run():
    run_name = request.json['runName']
    dispatch = request.json['dispatch']
    type = request.json['type']
    batch_v1 = client.BatchV1Api()
    if type == "delete":
        if dispatch == 'demand':
            patch = {"spec": {"suspend": True}}
            batch_v1.patch_namespaced_job(name=run_name, body=patch, namespace="default")
            batch_v1.delete_namespaced_job(name=run_name, namespace="default")
        else:
            batch_v1.delete_namespaced_cron_job(name=run_name, namespace="default")
    elif type == "pause":
        patch = {"spec": {"suspend": True}}
        if dispatch == 'demand':
            batch_v1.patch_namespaced_job(name=run_name, body=patch, namespace="default")
        else:
            batch_v1.patch_namespaced_cron_job(name=run_name, body=patch, namespace="default")
    else:   # restart
        patch = {"spec": {"suspend": False}}
        if dispatch == 'demand':
            batch_v1.patch_namespaced_job(name=run_name, body=patch, namespace="default")
        else:
            batch_v1.patch_namespaced_cron_job(name=run_name, body=patch, namespace="default")
    return jsonify({"status": True})


@app.route('/job-info', methods=['POST'])
def job_info():
    job_name = request.json['jobName']
    job = Job.query.get(job_name)
    # url = "http://82.156.5.94:5000/api/v1/job/"   # 服务器
    url = "http://127.0.0.1:5000/api/v1/job/"   # 本地
    batch_v1 = client.BatchV1Api()
    label_selector = 'app=' + job_name
    if job.dispatch == 'demand':
        job_list = batch_v1.list_namespaced_job(namespace="default", label_selector=label_selector).items
    else:
        job_list = batch_v1.list_namespaced_cron_job(namespace="default", label_selector=label_selector).items
    response_data = {}
    if len(job_list) == 0 or job_list[0].kind != 'Status':
        response_data['status'] = True
        response_data['dispatch'] = job.dispatch
        response_data['serverVersion'] = job.server_version
        response_data['url'] = url
        if job.dispatch == 'demand':
            list = []
            for job in job_list:
                if job.spec.suspend:
                    status = 'Running'
                    completion_time = None
                    delta = None
                else:
                    status = 'Complete'
                    completion_time = job.status.completion_time
                    delta = completion_time - job.metadata.creation_timestamp
                data = {
                    "id": job.metadata.uid.split('-')[0],
                    "name": job.metadata.name,
                    "status": status,
                    "createTime": job.metadata.creation_timestamp,
                    "duration": delta
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
                        delta = completion_time - second.metadata.creation_timestamp
                    else:
                        status = 'Running'
                        completion_time = None
                        delta = None
                    data = {
                        "id": second.metadata.uid.split('-')[0],
                        "name": second.metadata.name,
                        "status": status,
                        "createTime": second.metadata.creation_timestamp,
                        "duration": delta
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
    return jsonify(response_data)

@app.route('/model-run-job', methods=['POST'])
def run_job():
    job_name = request.json['jobName']
    run_name = request.json['runName']
    
    v1 = client.BatchV1Api()
    job = Job.query.get(job_name)
    body = job.job_json
    body['metadata']['name'] = run_name
    if job.dispatch == 'demand':
        body['spec']['template']['metadata']['labels']['job-name'] = run_name
    else:
        body['spec']['jobTemplate']['metadata']['labels']['job-name'] = run_name
        body['spec']['jobTemplate']['spec']['template']['metadata']['labels']['job-name'] = run_name
    if job.dispatch == 'demand':
        v1.create_namespaced_job(namespace="default", body=body)
    else:
        v1.create_namespaced_cron_job(namespace="default", body=body)
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
        s_info['status'] = service.status
        sl.append(s_info)
    response_data['serviceList'] = sl
    jl = []
    for job in job_list:
        j_info = {}
        j_info['name'] = job.job_name
        j_info['type'] =  "job"
        j_info['startTime'] = job.create_time
        j_info['status'] = True
        jl.append(j_info)
    response_data['serviceList'] = sl
    response_data['jobList'] = jl
    return jsonify(response_data)


@app.route('/generate-script', methods=['POST'])
def generate_script():
    input_dataset = request.json['inputDataset']
    output_dataset = request.json['outputDataset']


# # 测试一下
# @app.route('/model-deploy/run-job', methods=['POST'])
# def run_job():
#     pass

# 如果保留
def import_models():
    for model in Model.query.all():
        add_to_manager(model.model_name, model.model_path, model.type, model.descript)


if __name__ == '__main__':
    init_db()
    import_models()
    # app.run(host='0.0.0.0', port=5000)
    app.run()

    # # test
    # re = Request('test_model', './data/digis.pmml', 'pmml', 'this is a test model')
    # add(re.name, re.path, re.type, re.descript)
    # info = manager.getModel(re.name).getInfo()
    # with open("digis_data.json", "w", encoding="utf-8") as f:
    #     json.dump(info, f, ensure_ascii=False, indent=4)
