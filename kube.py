from argparse import Namespace
from re import S
from venv import create
import requests
from kubernetes import config, client
from kubernetes.watch import Watch
# from netkiller.docker import *
config.kube_config.load_kube_config()


def create_image(image, commands, expose):
    python = Dockerfile()
    python.image(image)
    for c in commands:
        python.run(c)
    python.show()
    python.save('/tmp/Dockerfile')

# create_image('python:3.7', [['mkdir /app'], ['apt-get update'], ['apt-get install -y libgl1-mesa-glx'], ['pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple'], ['pip install -r requirements.txt']], ['5000'])

def url_create_svc(api_version, service_name, ):
    svc_yaml = '''
        kind: Service
        apiVersion: {}
        metadata:
        name: {}
        spec:
        ports:
            - name: http
            port: 80
            targetPort: 80
        selector:
            app: {}
        type: NodePort
    '''.format(api_version, service_name, service_name)
    print

    pass

PORT = 80

def getPort():
    global PORT
    PORT += 1
    return PORT

def create_svc(api_version, service_name, server_version, memory_reserve, cpu_reserve, replicas=1):
    v1 = client.CoreV1Api()
    port = getPort()
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
                            "ports": [{"containerPort": 80, "hostPort": port}],
                            "command": ["python", "rest.py"],
                            "imagePullPolicy": "IfNotPresent",
                            "resources": {
                                "limits": {
                                    "cpu": cpu_reserve,
                                    "memory": memory_reserve
                                },
                                "requests": {
                                    "cpu": "0",
                                    "memory": "0Mi"
                                }
                            }
                        }
                    ],
                },
            },
        },
    }

    print('deploy:')
    resp = client.AppsV1Api().create_namespaced_deployment(namespace="default", body=deployment_manifest)
    print(resp)
    body = {
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
                    "port": port,
                    "targetPort": 80
                }
            ],
            "type": "NodePort"
        }
    }
    # body = client.V1Service(
    #     api_version=api_version,
    #     kind="Service",
    #     metadata=client.V1ObjectMeta(name=service_name),
    #     spec=client.V1ServiceSpec(
    #         selector={"app": service_name},
    #         ports=[
    #             client.V1ServicePort(
    #                 port=80,
    #                 target_port=80
    #             )
    #         ],
    #         type="NodePort"
    #     )
    # )
    print('service:')
    resp = v1.create_namespaced_service(namespace="default", body=body)
    print(resp.spec.ports[0].node_port)

def patch_deployment_status():
    pass


def create_job(v1, job_name, server_version):

    # ports = client.V1ContainerPort(
    #     container_port=80,
    #     host_port=80
    # )

    # container = client.V1Container(
    #     name=containername,
    #     image=imagename,
    #     resources=client.V1ResourceRequirements(),
    #     image_pull_policy="IfNotPresent",
    #     ports=[ports],
    #     # command=["gunicorn", "rest:app", "-c", "./gunicorn.conf.py"]
    #     command=["python", "rest.py"]
    # )

    # secrets = client.V1LocalObjectReference(
    #     name="my-docker"
    # )

    # template = client.V1PodTemplateSpec(
    #     metadata=client.V1ObjectMeta(labels={"app": "python"}),
    #     spec=client.V1PodSpec(restart_policy="Never", containers=[container], image_pull_secrets=[secrets])
    # )


    # spec = client.V1JobSpec(
    #     template=template,
    #     backoff_limit=4,
    # )
    
    # # todo
    # job = client.V1Job(
    #     api_version="batch/v1",
    #     kind="Job",
    #     metadata=client.V1ObjectMeta(name=jobname),
    #     spec=spec
    # )

    # print(job)
    job_manifest = {
        "kind": "Job",
        "apiVersion": "batch/v1",
        "metadata": {
            "name": job_name
        },
        "spec": {
            "template": {
                "metadata":{
                    "labels": {
                        "app": job_name,
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": server_version,
                            "image": server_version,
                            "command": ["python", "rest.py"],
                            "imagePullPolicy": "IfNotPresent"
                        }
                    ],
                    "restartPolicy": "Never"
                }
            },
            
        }
    }
    batch_v1 = client.BatchV1Api()
    resp = batch_v1.create_namespaced_job(namespace="default", body=job_manifest)
    print(resp)
    # api_response = v1.create_namespaced_job(
    #     body=job,
    #     namespace="default",
    # )

    # watcher = Watch()

    # for event in watcher.stream(
    #     v1.list_namespaced_job,
    #     namespace='default',
    #     label_selector=f'job-name={jobname}'
    # ):
    #     print(event['object'])

# create_job(v1, "test1", "test", "first", ["python3", "test.py"])

def create_cron_job(v1, run_name, server_version):
    job_manifest = {
        "kind": "CronJob",
        "apiVersion": "batch/v1",
        "metadata": {
            "name": run_name
        },
        "spec": {
            "schedule": '* * * * *',
            "jobTemplate": {
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
                                    "command": ["python", "rest.py"],
                                    "imagePullPolicy": "IfNotPresent",
                                }
                            ],
                            "restartPolicy": "Never"
                        }
                    },
                }
            }
            
        }
    }
    resp = v1.create_namespaced_cron_job(namespace="default", body=job_manifest)
    print(resp)

# 创建镜像，生成job，直至结束返回结果
if __name__ == '__main__':
    # create_svc("v1", "my-dep2", "test", "100Mi", "1")
    v1 = client.BatchV1Api()
    # job_list = v1.list_namespaced_job(namespace="default", label_selector='job-name=my-job2').items
    # print(job_list)
    # create_job(v1, "my-job2", 'test')
    create_cron_job(v1, "my-cron-job", "test")
    # v1 = client.CoreV1Api()
    # service_name = "my-dep2"
    # resp = v1.read_namespaced_service(name=service_name, namespace="default")
    
    # pod_list = v1.list_namespaced_pod(namespace="default", label_selector="app=my-dep2", watch=False).items
    pass