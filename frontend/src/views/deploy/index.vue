<template>
  <div class="layout-demo">
    <a-layout style="min-height: 950px">
      <a-layout-header style="height: 180px">
        <div>
          <a-breadcrumb style="margin-left: 15px">
            <a-breadcrumb-item>主页</a-breadcrumb-item>
            <a-breadcrumb-item>模型</a-breadcrumb-item>
            <a-breadcrumb-item>{{ modelName }}</a-breadcrumb-item>
            <template #separator>
              <icon-right />
            </template>
          </a-breadcrumb>
          <div style="height: 200px; margin-left: 10px">
            <p style="font-weight: bold; font-size: 22px">{{ modelName }}</p>
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
              :align="{ label: 'right', value: 'right' }"
              column="6"
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
                <a-table :columns="copyColumns" :data="copyData" />
              </div>
              <a-divider />
            </div>
          </a-tab-pane>
          <a-tab-pane id="overview" key="2" title="测试">
            <div id="var">
              <div id="inputVar">
                <p class="tag" style="margin-left: 2%">请求</p>
                <a-divider />
                <p style="margin-left: 2%">* 函数名</p>
                <a-input
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
                />
                <p style="margin-left: 10px">* 请求正文</p>
                <a-textarea
                  v-model="output"
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
                <div style="position: relative; left: 65%">
                  <a-button type="outline" style="margin: 10px">清除</a-button>
                  <a-button type="primary" style="margin: 10px">提交</a-button>
                </div>
              </div>
              <div id="targetVar">
                <p class="tag">响应</p>
                <a-divider />
                <a-textarea
                  v-model="output"
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

<script type="ts" setup>
  import { ref,onMounted,reactive} from 'vue'
  import axios from 'axios'

  const modelName = ref('xgb-iris')
  const postmsg = ref('https://192.168.64.3:30931/api/vt/svc/pmml/xgb-iris-svc/predict')
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
          label: 'CPU核数',
          value: '-'
      }, {
          label: '内存(GB)',
          value: '-'
      }
  ],

    );
  const inputColumns=[
      {
          title:'字段',
          dataIndex:'field',
      },
      {
          title:"类型",
          dataIndex:'type',
      },
      {
          title:"测量",
          dataIndex:'measure',
      },
      {
          title:"取值",
          dataIndex:'value',
      }
  ];
  const inputData = ref()
  const targetData = ref()
  const deployColumns=[
      {
          title:'名称',
          dataIndex:'name',
      },
      {
          title:"类型",
          dataIndex:'type',
      },
      {
          title:"开始时间",
          dataIndex:'startTime',
      },
      {
          title:"状态",
          dataIndex:'status',
      },
      {
          title:"操作",
          dataIndex:'operation',
      }
  ];
  const deployData = reactive([]);

  onMounted(()=>{
      axios.get('/api/modelOverview/info')
      .then(response=>{

      })

      axios.get('/api/modelOverview/var')
      .then(response=>{
          inputData.value = response.data.inputData;
          targetData.value = response.data.targetData;
      })
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
