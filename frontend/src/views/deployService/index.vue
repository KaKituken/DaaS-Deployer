<template>
  <div class="layout-demo">
    <a-layout style="min-height: 950px">
      <a-layout-header style="height: 180px">
        <div>
          <a-breadcrumb style="margin-left: 15px">
            <a-breadcrumb-item>主页</a-breadcrumb-item>
            <a-breadcrumb-item><a href="\list">模型</a></a-breadcrumb-item>
            <a-breadcrumb-item
              ><a :href="modelUrl">{{ modelName }}</a></a-breadcrumb-item
            >
            <a-breadcrumb-item>{{ serviceName }}</a-breadcrumb-item>
            <template #separator>
              <icon-right />
            </template>
          </a-breadcrumb>
          <div style="height: 200px; margin-left: 10px">
            <p style="font-weight: bold; font-size: 22px">{{ serviceName }}</p>
            <p style="width: 600px"
              ><span style="color: gray">端点: </span
              ><span style="colro: black; font-weight: bold">POST </span
              ><span style="color: purple">{{ postmsg }}</span></p
            >
          </div>
        </div>
        <div id="detailInfo">
          <a-space direction="vertical" size="medium" fill>
            <a-descriptions
              :data="basicData"
              size="small"
              :align="{ label: 'right', value: 'right' }"
              :column="6"
              layout="inline-vertical"
            />
          </a-space>
        </div>
      </a-layout-header>
      <a-layout-content>
        <a-tabs default-active-key="1" style="width: 100%; height: 100%">
          <a-tab-pane key="1" title="概述">
            <div id="deploy">
              <div class="deployheader">
                <p class="tag" style="margin-top: 0; padding-top: 15px">指标</p>
              </div>
              <a-divider style="margin-top: 0" />
              <div class="table">
                <a-table :columns="indexColumns" :data="indexData" />
              </div>
              <a-divider />
              <!-- 灰色分隔块 -->
              <div style="height: 40px; background-color: #f5f5f5"></div>

              <div class="deployheader">
                <p class="tag" style="margin-top: 0; padding-top: 15px">副本</p>
              </div>
              <a-divider style="margin-top: 0" />
              <div class="table">
                <a-table :columns="copyColumns" :data="copyData">
                  <template #operation="{ record }">
                    <a-button @click="onclickColumn(record)">删除</a-button>
                  </template>
                </a-table>
              </div>
              <a-divider />
            </div>
          </a-tab-pane>
          <a-tab-pane id="overview" key="2" title="测试">
            <div id="var">
              <div id="inputVar">
                <p class="tag" style="margin-left: 2%"
                  >请求
                  <a
                    style="
                      text-align: right;
                      color: #165dff;
                      text-decoration: none;
                      font-weight: normal;
                      margin-left: 5%;
                    "
                    href="#"
                    @click="genCode"
                    >生成代码</a
                  >
                </p>
                <!-- 显示curl代码的悬浮窗 -->
                <a-modal v-model:visible="visible" hide-cancel @ok="handleOk">
                  <template #title> 生成的curl代码 </template>
                  <div style="white-space: pre-line">{{ showCode }}</div>
                </a-modal>
                <a-divider />
                <p style="margin-left: 2%">* 函数名</p>
                <a-input
                  v-model="testFuncName"
                  :style="{
                    'width': '94%',
                    'margin': '2%',
                    'background-color': 'white',
                    'border-style': 'solid',
                    'border-color': 'gray',
                    'border-radius': '5px',
                  }"
                  placeholder=""
                  allow-clear
                  disabled
                />
                <p style="margin-left: 10px">* 请求正文</p>
                <a-textarea
                  v-model="testRequire"
                  placeholder="Please enter something"
                  allow-clear
                  style="
                    background-color: white;
                    position: relative;
                    top: -20px;
                    width: 94%;
                    border-style: solid;
                    border-color: gray;
                    height: 50%;
                    margin-left: 2%;
                    margin-top: 20px;
                  "
                />
                <input style="margin-left:5%;" type="file" placeholder="请选择模型文件" id="fileUpload"/>
                <div style="position: relative; left:50%">
                  <a-button type="outline" style="margin: 10px" @click="clear"
                    >清除</a-button
                  >
                  <a-button
                    type="primary"
                    style="margin: 10px"
                    @click="dataSubmit"
                    >提交</a-button
                  >
                  <a-button type="primary" style="margin:10px" @click="submitFile">提交文件</a-button>
                </div>
              </div>
              <div id="targetVar">
                <p class="tag">响应</p>
                <a-divider />
                <a-textarea
                  v-model="testResponse"
                  placeholder="Please enter something"
                  allow-clear
                  style="
                    background-color: white;
                    position: relative;
                    top: -20px;
                    width: 94%;
                    border-style: solid;
                    border-color: gray;
                    height: 71%;
                    margin-left: 2%;
                    margin-top: 20px;
                  "
                  disabled
                />
              </div>
            </div>
          </a-tab-pane>
        </a-tabs>
      </a-layout-content>
      <a-layout-footer> </a-layout-footer>
    </a-layout>
  </div>
</template>

<script lang="ts" setup>
  import { Message } from '@arco-design/web-vue';
  import { ref, onMounted, reactive } from 'vue';
  import axios from 'axios';
  import { useRoute, useRouter } from 'vue-router';
  import { Sleep } from '../../api/deployService';
  import type {
    requireDataResponse,
    copyResponseData,
  } from '../../api/deployService';
  import { status } from '../../api/addService';

  const route = useRoute();
  const router = useRouter();
  const serviceName = ref('serviceName');
  const modelName = ref('modelName');
  const fileData = ref('');  // 测试文件
  serviceName.value = route.params.serviceName as string; // 工作名称
  modelName.value = route.params.modelName as string; // 模型名称

  const modelUrl = ref(`/detail/${modelName.value}`);

  const postmsg = ref('');
  const basicData = reactive([
    {
      label: '类别',
      value: '网络服务',
    },
    {
      label: '类型',
      value: '默认实时预测',
    },
    {
      label: '对象',
      value: modelName.value,
    },
    {
      label: '创建时间',
      value: '-',
    },
    {
      label: '预留CPU核数',
      value: '-',
    },
    {
      label: '预留内存(MB)',
      value: '-',
    },
  ]);

  // 测试页面的变量
  const testFuncName = ref('predict');
  const testRequire = ref();
  const testResponse = ref();
  const visible = ref(false);
  const showCode = ref();

  // 概述界面表格相关：
  const indexColumns = [
    {
      title: '函数名',
      dataIndex: 'funcName',
    },
    {
      title: '访问次数',
      dataIndex: 'accessTimes',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: '平均响应时间(ms)',
      dataIndex: 'avgResponseTime',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: '最小响应时间(ms)',
      dataIndex: 'minResponseTime',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: '最大响应时间(ms)',
      dataIndex: 'maxResponseTime',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: '首次访问时间',
      dataIndex: 'firstAccessTime',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: '最新访问时间',
      dataIndex: 'latestAccessTime',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
  ];
  const indexData = reactive([
    {
      funcName: 'predict',
      accessTimes: 2,
      avgResponseTime: 205.0,
      minResponseTime: 12.0,
      maxResponseTime: 398.0,
      firstAccessTime: '2019-09-28 17:30:59',
      latestAccessTime: '2019-09-28 17:31:40',
    },
  ]);

  const copyColumns = [
    {
      title: '名称',
      dataIndex: 'name',
    },
    {
      title: '状态',
      dataIndex: 'status',
    },
    {
      title: '操作',
      slotName: 'operation',
    },
  ];

  const copyData = ref();

  const clear = () => {
    testFuncName.value = '';
    testRequire.value = '';
  };

  const onclickColumn = async (record: any) => {
    const params = reactive({
      podName: record.name,
      operationType: 'delete',
    });
    const res = await axios.post<status>(
      'http://82.156.5.94:5000/operate-pod',
      params
    );
    // console.log('======delete pod======');
    // console.log(res.data);
    if (res.data.status === false) {
      alert('delete pod failed, please try again...');
    } else {
      const isPending = ref(true);
      if (isPending.value) {
        const param = {
          serviceName: serviceName.value,
        };
        const res1 = await axios.post<copyResponseData>(
          'http://82.156.5.94:5000/service-info',
          param
        );
        copyData.value = res1.data.podList;
        isPending.value = false;
        for (let i = 0; i < copyData.value.length; i += 1) {
          if (copyData.value[i].status === 'Pending') {
            isPending.value = true;
          }
        }
        await Sleep(3000);
      }
    }
  };

  onMounted(async () => {
    axios
      .get('http://82.156.5.94:5000/model-deploy-service')
      .then((response) => {
        // 把链接拼接出来
        // postmsg.value = response.data.restfulUrl.concat(serviceName.value);
        postmsg.value = response.data.restfulUrl.concat(
          serviceName.value,
          '/predict'
        );
      });

    // 获取副本
    const param = {
      serviceName: serviceName.value,
    };
    const res1 = await axios.post<copyResponseData>(
      'http://82.156.5.94:5000/service-info',
      param
    );
    basicData[3].value = res1.data.createTime;
    basicData[4].value = res1.data.cpuReserve;
    basicData[5].value = res1.data.memoryReserve;
    indexData[0].funcName = res1.data.function;
    indexData[0].accessTimes = res1.data.acessTimes;
    indexData[0].avgResponseTime = res1.data.averageResponseTime;
    indexData[0].minResponseTime = res1.data.minResponseTime;
    indexData[0].maxResponseTime = res1.data.maxResponseTime;
    indexData[0].firstAccessTime = res1.data.firstAccessTime;
    indexData[0].latestAccessTime = res1.data.lastAccessTime;
    copyData.value = res1.data.podList;
  });

  const dataSubmit = async () => {
    const userRequestData = JSON.parse(testRequire.value);

    const submitParam = {
      modelName: modelName.value,
      data: userRequestData
    }

    const res1 = await axios.post<requireDataResponse>(
      postmsg.value,
      submitParam
    );
    let returnData = JSON.stringify(res1.data);
    returnData = returnData.replace(/{([^{}]*)}/g, '{\n$1\n    }'); // 在{}对前面加缩进，后面加换行
    returnData = returnData.replace(/(\[)([a-zA-Z0-9'"])/g, '$1\n$2'); // 在[后面加换行
    returnData = returnData.replace(/([a-zA-Z0-9'"])(\])/g, '$1\n$2'); // 在]后面加换行
    returnData = returnData.replace(/,/g, ',\n'); // 在,后面加换行
    testResponse.value = returnData;
    const param = {
      serviceName: serviceName.value,
    };
    const res2 = await axios.post<copyResponseData>(
      'http://82.156.5.94:5000/service-info',
      param
    );
    basicData[3].value = res2.data.createTime;
    basicData[4].value = res2.data.cpuReserve;
    basicData[5].value = res2.data.memoryReserve;
    indexData[0].funcName = res2.data.function;
    indexData[0].accessTimes = res2.data.acessTimes;
    indexData[0].avgResponseTime = res2.data.averageResponseTime;
    indexData[0].minResponseTime = res2.data.minResponseTime;
    indexData[0].maxResponseTime = res2.data.maxResponseTime;
    indexData[0].firstAccessTime = res2.data.firstAccessTime;
    indexData[0].latestAccessTime = res2.data.lastAccessTime;
  };

  const genCode = () => {
    const urlCode = postmsg.value;
    // showCode.value = 'curl --location --request POST'.concat('\\\n' ,"'",urlCode , "'",'\\\n');
    showCode.value = 'curl --location --request POST '.concat(
      "'",
      urlCode,
      "'"
    );
    showCode.value = showCode.value.concat(
      " --header 'Content-Type: application/json' --data-raw '",
      testRequire.value,
      "'"
    );
    visible.value = true;
  };
  const handleOk = () => {
    visible.value = false;
  };

  const submitFile = async () => {
    console.log('get file');
    
    const formData = new FormData();
    formData.append('modelName', modelName.value);
    const file = document.querySelector('#fileUpload') as HTMLInputElement;
    if (file.files && file.files[0]) {
      
      formData.append('file', file.files[0]);
    

      const res1 = await axios.post<requireDataResponse>(
        postmsg.value,
        formData
      );
      let returnData = JSON.stringify(res1.data);
      returnData = returnData.replace(/{([^{}]*)}/g, '{\n$1\n    }'); // 在{}对前面加缩进，后面加换行
      returnData = returnData.replace(/(\[)([a-zA-Z0-9'"])/g, '$1\n$2'); // 在[后面加换行
      returnData = returnData.replace(/([a-zA-Z0-9'"])(\])/g, '$1\n$2'); // 在]后面加换行
      returnData = returnData.replace(/,/g, ',\n'); // 在,后面加换行
      testResponse.value = returnData;
      const param = {
        serviceName: serviceName.value,
      };
      const res2 = await axios.post<copyResponseData>(
        'http://82.156.5.94:5000/service-info',
        param
      );
      basicData[3].value = res2.data.createTime;
      basicData[4].value = res2.data.cpuReserve;
      basicData[5].value = res2.data.memoryReserve;
      indexData[0].funcName = res2.data.function;
      indexData[0].accessTimes = res2.data.acessTimes;
      indexData[0].avgResponseTime = res2.data.averageResponseTime;
      indexData[0].minResponseTime = res2.data.minResponseTime;
      indexData[0].maxResponseTime = res2.data.maxResponseTime;
      indexData[0].firstAccessTime = res2.data.firstAccessTime;
      indexData[0].latestAccessTime = res2.data.lastAccessTime;

    } else {
      Message.error('请选择请求文件');
    }
    };
</script>

<style scoped>
  .layout-demo {
    min-width: 860px;
  }

  .layout-demo :deep(.arco-layout-header),
  .layout-demo :deep(.arco-layout-content),
  .layout-demo :deep(.arco-layout-footer) {
    display: flex;
    color: var(--color-black);
    font-size: 16px;
    font-stretch: condensed;
  }

  .layout-demo :deep(.arco-layout-header) {
    height: 150px;
    background-color: #fff;
  }

  .layout-demo :deep(.arco-layout-content) {
    background-color: #f5f5f5;
  }

  .layout-demo :deep(.arco-layout-footer) {
    height: 50px;
    margin-top: 20px;
    margin-right: 2%;
    margin-left: 2%;
    background-color: #f5f5f5;
  }

  #detailInfo {
    justify-content: flex-end;
    width: 700px;
    margin-top: 70px;
    margin-right: 50px;
    margin-left: auto;
  }

  #overview {
    display: flex;
    flex-direction: column;
  }

  #var {
    display: flex;
  }

  #inputVar,
  #targetVar {
    width: 47%;
    height: 650px;
    margin-left: 2%;
    background-color: #fff;
  }

  .tag {
    margin-top: 15px;
    margin-left: 12px;
    font-weight: bold;
    font-size: 18px;
  }

  .table {
    margin: 0 8px 0 8px;
  }

  #result {
    height: 200px;
    margin-top: 20px;
    margin-right: 2%;
    margin-left: 2%;
    background-color: #fff;
  }

  #resultTag {
    padding-top: 15px;
  }

  #deploy {
    margin-right: 2%;
    margin-left: 2%;
    background-color: #fff;
  }

  .deployheader {
    display: flex;
    flex-direction: row;
  }

  .deployheader #addService {
    justify-content: flex-end;
    margin-top: 15px;
    margin-right: 0;
    margin-bottom: 15px;
    margin-left: auto;
  }

  .deployheader #addTask {
    justify-content: flex-end;
    margin-top: 15px;
    margin-right: 50px;
    margin-bottom: 15px;
    margin-left: 10px;
  }

  #test {
    background-color: white;
  }
</style>
