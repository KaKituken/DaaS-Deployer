<template>
  <div class="layout-demo">
    <a-layout style="min-height: 950px">
      <a-layout-header style="height: 240px; overflow:visible;">
        <!-- 上面一行的样式稍作修改以容纳过多的内容 -->
        <div>
          <a-breadcrumb style="margin-left: 15px">
            <a-breadcrumb-item>主页</a-breadcrumb-item>
            <a-breadcrumb-item><a href="\list">模型</a></a-breadcrumb-item>
            <a-breadcrumb-item><a :href="modelUrl">{{ modelName }}</a></a-breadcrumb-item>
            <a-breadcrumb-item>{{ jobName }}</a-breadcrumb-item>
            <template #separator>
              <icon-right />
            </template>
          </a-breadcrumb>
          <div style="height: 200px; margin-left: 10px">
            <p style="font-weight: bold; font-size: 22px">{{ jobName }}</p>
            <p style="width: 600px"
              ><span style="color: gray">端点: </span
              ><span style="colro: black; font-weight: bold">POST </span
              ><span style="color: purple">{{ postmsg }}</span></p
            >
            <p style="color: grey">部署令牌:</p>
          </div>
        </div>
        <div id="detailInfo">
          <a-space direction="vertical" size="medium" fill>
            <a-descriptions
              :data="basicData"
              size="small"
              :align="{ label: 'left', value: 'left' }"
              column="6"
              layout="inline-vertical"
            />
          </a-space>
        </div>
      </a-layout-header>
      <a-layout-content>
        <a-tabs default-active-key="1" style="width: 100%; height: 100%">
          <a-tab-pane key="1" title="概述">
             <div id="var">
              <div id="inputVartest">
                <p class="tag">默认环境变量</p>
                <a-divider />
                <div class="table">
                  <a-table :columns="envVariableColumns" :data="inputData" />
                </div>
              </div>
              <div id="targetVartest">
                <p class="tag">默认命令参数</p>
                <a-divider />
                <div class="table">
                  <a-table :columns="paramColumns" :data="targetData" />
                </div>
              </div>
            </div>
            <div id="result">
              <p id="resultTag" class="tag">运行
                 <a-button type="outline" style="margin: 10px; margin-left:80%;" @click="operateNow">+ 立即执行</a-button>
              </p>
              <a-divider />
              <div class="table">
                  <a-table :columns="userRunColumns" :data="userRunData" />
              </div>
            </div>
          </a-tab-pane>
          <a-tab-pane id="overview" key="2" title="测试">
            <div id="var">
              <div id="inputVar">
                <p class="tag" style="margin: 2%">请求
                <a @click='genCode' style="text-align:right; color: #165dff; text-decoration:none; font-weight:normal; margin-left: 5%;" href="#">生成代码</a>
                </p>
                <!-- 显示curl代码的悬浮窗 -->
                <a-modal v-model:visible="visible" @ok="handleOk" hide-cancel>
                  <template #title>
                    生成的curl代码
                  </template>
                  <div style="white-space: pre-line;">{{showCode}}</div>
                </a-modal>
                <a-divider />
                <p style="margin-left: 2%">runName</p>
                 <a-input
                  v-model="runName"
                  :style="{
                    'width': '94%',
                    'margin': '2%',
                    'background-color': 'white',
                    'border-style': 'solid',
                    'border-color': 'gray',
                    'border-radius': '5px',
                  }"
                  placeholder="runName"
                  allow-clear
                />
                <p style="margin-left: 2%">环境变量</p>
                <a-input
                  v-model="envVariable"
                  :style="{
                    'width': '94%',
                    'margin': '2%',
                    'background-color': 'white',
                    'border-style': 'solid',
                    'border-color': 'gray',
                    'border-radius': '5px',
                  }"
                  placeholder="形如key1=value1;key2=value2"
                  allow-clear
                />
                <p style="margin-left: 2%">命令参数</p>
                <a-input
                  v-model="commandParam"
                  :style="{
                    'width': '94%',
                    'margin': '2%',
                    'background-color': 'white',
                    'border-style': 'solid',
                    'border-color': 'gray',
                    'border-radius': '5px',
                  }"
                  placeholder="请直接输入args的值"
                  allow-clear
                />
                <div style="position: relative; left: 65%; top: 10%;">
                  <a-button type="outline" style="margin: 10px" @click="clear">清除</a-button>
                  <a-button type="primary" style="margin: 10px" @click="dataSubmit">提交</a-button>
                </div>
              </div>
              <div id="targetVar">
                <p class="tag">响应</p>
                <a-divider />
                <a-textarea
                  v-model="responseData"
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

<script type="ts" lang="ts" setup>
  import { ref,onMounted,reactive} from 'vue'
  import axios from 'axios'
  import { useRoute } from 'vue-router';

  import type {
    jobResponseData,
    testResponseData
  } from '../../api/deployJob';

  const route = useRoute();
  const jobName = ref('jobName');
  const modelName = ref('modelName');
  jobName.value = route.params.jobName as string;  // 工作名称
  modelName.value = route.params.modelName as string;  // 模型名称
  const postmsg = ref('');
  
  const modelUrl = ref(`/detail/${modelName.value}`);
  
  const basicData = reactive([{
          label: '类别',
          value: '网络服务',
      }, {
          label: '类型',
          value: '默认实时预测',
      }, {
          label: '对象',
          value: 'xgb-iris'
      }, {
          label: '创建时间',
          value: '2019-7-9',
      }, {
          label: '运行环境',
          value: 'Python3.7 - Script as a Service'
      }, {
          label: '调度',
          value: 'On demand'
      },
      {
          label: 'CPU核数',
          value: '-'
      }, {
          label: '内存(GB)',
          value: '-'
      }
  ],

    );

  
  const envVariableColumns=[
      {
          title:'变量',
          dataIndex:'userVarialbe',
      },
      {
          title:"值",
          dataIndex:'userNumber',
      }
  ];
  const userRunColumns=[
    {
      title: 'ID',
      dataIndex: 'runId'
    },
    {
      title: '名称',
      dataIndex: 'runName'
    },
    {
      title: '开始时间',
      dataIndex: 'runBeginTime'
    },
    {
      title: '持续时间(秒)',
      dataIndex: 'runSpanTime'
    },
    {
      title: '状态',
      dataIndex: 'runStatus'
    },
    {
      title: '操作',
      dataIndex: 'runOperation'
    }
  ];
   const paramColumns=[
      {
          title:'顺序',
          dataIndex:'userSequence',
      },
      {
          title:"参数",
          dataIndex:'userParam',
      }
  ];
  const inputData = ref()  // 概述页面左边表格数据
  const targetData = ref()  // 概述页面右边表格数据
  const userRunData = ref()  // 概述页面最下面表格数据

 
  const deployData = reactive([]);

  // 测试页面获取的数据
  const runName = ref();
  const envVariable = ref();
  const commandParam = ref();
  const responseData = ref();  // 绑定响应框
  const showCode = ref();  // 显示的curl代码
  const visible = ref(false);  // 是否显示悬浮窗

  onMounted(async ()=>{
      axios.get('/api/modelOverview/info')
      .then(response=>{

      })

      axios.get('/api/modelOverview/var')
      .then(response=>{
          inputData.value = response.data.inputData;
          targetData.value = response.data.targetData;
      });

      // 申请数据
      const param = {
        'jobName': jobName.value
      };
      const res1 = await axios.post<jobResponseData>('http://82.156.5.94:5000/job-info', param);
      console.log(res1.data);
      postmsg.value = res1.data.url.concat(jobName.value);  // 获取url
      
  });

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
      title: '中间响应时间(ms)',
      dataIndex: 'midResponseTime',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: '最小响应时间',
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
      }
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
    }
  ];
  const indexData = reactive([
    {
      funcName: 'predict',
      accessTimes: 2,
      avgResponseTime: 205.0,
      midResponseTime: 205.0,
      minResponseTime: 12.0,
      maxResponseTime: 398.0,
      firstAccessTime: '2019-09-28 17:30:59',
      latestAccessTime: '2019-09-28 17:31:40',
    },
  ]);

  const copyColumns = [
    {
      title: '名称',
      dataIndex: 'copyName',
    },
    {
      title: '状态',
      dataIndex: 'copyStatus',
    },
    {
      title: '操作',
      dataIndex: 'operation'
    }
  ];

  const copyData = reactive([
    {
      copyName: 'd-pmml-xgb-iris-svc-5854487d5b-zbsjn',
      copyStatus: '运行中',
      operation: '默认'
    },
  ]);

  const clear = () => {
    runName.value = '';
    envVariable.value = '';
    commandParam.value = '';
  };

  const dataSubmit = async () => {
    const jobPostData = {
      "runName": runName.value,
      "variables": envVariable.value,
      "args": commandParam.value
    };
    const res1 = await axios.post<testResponseData>(postmsg.value, jobPostData);
    // console.log(res1.data);
   
    let returnData = JSON.stringify(res1.data);
    returnData = returnData.replace(/{([^{}]*)}/g, "{\n$1\n    }");  // 在{}对前面加缩进，后面加换行
    returnData = returnData.replace(/(\[)([a-zA-Z0-9'"])/g, "$1\n$2");  // 在[后面加换行
    returnData = returnData.replace(/([a-zA-Z0-9'"])(\])/g, "$1\n$2");  // 在]后面加换行
    returnData = returnData.replace(/,/g, ",\n");  // 在,后面加换行
    responseData.value = returnData;
  }

  const genCode = () => {
    // 构造代码里面的对象
    const codeContent = {
      "runName": runName.value,
      "variables": envVariable.value,
      "args": commandParam.value
    };

    // 拼接代码
    const urlCode = postmsg.value;
    showCode.value = 'curl --location --request POST '.concat("'", urlCode, "'");
    showCode.value = showCode.value.concat(" --header 'Content-Type:application/json' --data-raw '");
    showCode.value = showCode.value.concat(JSON.stringify(codeContent), "'");
    
    // 显示浮窗
    visible.value = true;
  }
  const handleOk = () => {
    visible.value = false;
  }

  const operateNow = () => {
    alert('立即执行')
  }



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
    height: 500px;
    margin-left: 2%;
    background-color: #fff;
  }

  #inputVartest,
  #targetVartest {
    width: 47%;
    height: 400px;
    margin-left: 2%;
    background-color: #fff;
    overflow:auto;
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
    height: 300px;
    margin-top: 20px;
    margin-right: 2%;
    margin-left: 2%;
    background-color: #fff;
    overflow: auto;
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
