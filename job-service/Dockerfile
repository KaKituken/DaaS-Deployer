FROM python:3.8
RUN mkdir /app
WORKDIR /app
# COPY sources.list sources.list
COPY requirements.txt requirements.txt
COPY . /app
# ADD sources.list /etc/apt/
# RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B4FE6ACC0B21F32
# RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse" >> /etc/apt/sources.list
# RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse" >>/etc/apt/sources.list
# RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse" >>/etc/apt/sources.list
# RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse" >>/etc/apt/sources.list

# RUN apt-get update
# RUN apt-get install -y libgl1-mesa-glx
# RUN sudo apt-get install default-jdk
RUN export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
RUN export PATH=$PATH:/usr/bin
# RUN java --version
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 80