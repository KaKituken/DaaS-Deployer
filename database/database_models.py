from xmlrpc.client import boolean
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Float
from database.database import Base
from datetime import datetime

class Service(Base):
    __tablename__ = 'services'
    service_name = Column(String(50), primary_key=True)
    model_type = Column(String(10))
    model_name = Column(String(50))
    cpu = Column(String(10))
    memory = Column(String(10))
    service_version = Column(Integer)
    status = Column(Boolean)    # True表示运行中，False表示暂停中
    replicas = Column(Integer)
    create_time = Column(DateTime)
    node_port = Column(String(10))
    # performance related
    access_times = Column(Integer)
    average_response_time = Column(Float)
    max_response_time = Column(Float)
    min_response_time = Column(Float)
    first_access = Column(Boolean)
    first_access_time = Column(DateTime)
    last_access_time = Column(DateTime)

    def __init__(self, service_name=None, model_name=None, cpu=None, memory=None, service_version=None, 
    status=None, replicas=None, create_time=datetime.now(), node_port=None, model_type=None):
        self.service_name = service_name
        self.model_name = model_name
        self.model_type = model_type
        self.cpu = cpu
        self.memory = memory
        self.service_version = service_version
        self.status = status
        self.replicas = replicas
        self.create_time = create_time
        self.node_port = node_port
        self.access_times = 0
        self.average_response_time = 0.0
        self.max_response_time = 0.0
        self.min_response_time = 99999.9
        self.first_access = True
        self.first_access_time = None
        self.last_access_time = None

    def __repr__(self):
        return '<Service %r>' % (self.service_name)


# Job模板，并非运行中的job
class Job(Base):
    __tablename__ = 'job'
    job_name = Column(String(50), primary_key=True)
    create_time = Column(DateTime)
    job_json = Column(JSON)
    dispatch = Column(String(20))
    job_description = Column(String(100))
    server_version = Column(String(20))
    model_type = Column(String(10))
    model_name = Column(String(50))
    input_dataset = Column(String(50))
    output_dataset = Column(String(50))

    def __init__(self, job_name=None, create_time=datetime.now(), job_json=None, 
    dispatch="demand", job_description=None, server_version=None, model_name=None, model_type=None, 
    input_dataset=None, output_dataset=None) -> None:
        self.job_name = job_name
        self.create_time = create_time
        self.job_json = job_json
        self.dispatch = dispatch
        self.job_description = job_description
        self.server_version = server_version
        self.model_name = model_name
        self.model_type = model_type
        self.input_dataset = input_dataset
        self.output_dataset = output_dataset

    def __repr__(self) -> str:
        return '<Job %r>' % (self.job_name)


class Model(Base):
    __tablename__ = 'model'
    model_name = Column(String(50), primary_key=True)
    model_path = Column(String(80))
    create_time = Column(DateTime)  # 这里需要改？
    descript = Column(String(100))
    type = Column(String(50))
    #--------------------------------
    engine = Column(String(20))
    function = Column(String(20))
    input = Column(JSON)    # 没有办法存list，也许转为json存
    output = Column(JSON)

    def __init__(self, model_name=None, model_path=None, create_time=datetime.now(), descript=None,
        engine=None, type=None, function=None, input=None, output=None) -> None:
        self.model_name = model_name
        self.model_path = model_path
        self.create_time = create_time
        self.descript = descript
        #--------------------------
        self.engine = engine
        self.type = type
        self.function = function
        self.input = input
        self.output = output

    def __repr__(self) -> str:
        return '<Model %r>' % (self.model_name)


class Setting(Base):
    __tablename__ = 'setting'
    model_name = Column(String(50), primary_key=True)
    filename = Column(String(50))
    ext = Column(String(10))
    job_name = Column(String(50))
    job_description = Column(String(144))
    server_version = Column(String(20))
    variables = Column(String(100))
    args = Column(String(100))
    dispatch = Column(String(10))
    run_name = Column(String(50))

    def __init__(self, model_name=None, filename=None, ext=None, job_name=None, job_description=None, server_version=None,
        variables=None, args=None, dispatch=None, run_name=None):
        self.model_name = model_name
        self.filename = filename
        self.ext = ext
        self.job_name = job_name
        self.job_description = job_description
        self.server_version = server_version
        self.variables = variables
        self.args = args
        self.dispatch = dispatch
        self.run_name = run_name

    def __repr__(self) -> str:
        return '<Setting %r>' % (self.model_name)

class Dataset(Base):
    __tablename__ = 'dataset'
    dataset_name = Column(String(50))
    job_id = Column(String(10), primary_key=True)   # 实际上是run_id

    def __repr__(self) -> str:
        return '<Dataset %r>' % (self.dataset_name)