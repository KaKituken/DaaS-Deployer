<template>
  <div class="layout-demo">
    <a-layout style="min-height: 950px">
      <a-layout-header style="height: 240px; overflow: visible">
        <!-- 上面一行的样式稍作修改以容纳过多的内容 -->
        <div>
          <a-breadcrumb style="margin-left: 15px">
            <a-breadcrumb-item>主页</a-breadcrumb-item>
            <a-breadcrumb-item><a href="\list">模型</a></a-breadcrumb-item>
            <a-breadcrumb-item
              ><a :href="modelUrl">{{ modelName }}</a></a-breadcrumb-item
            >
            <a-breadcrumb-item>{{ jobName }}</a-breadcrumb-item>
            <template #separator>
              <icon-right />
            </template>
          </a-breadcrumb>
          <div style="height: 200px; margin-left: 10px">
            <p style="font-weight: bold; font-size: 22px">{{ jobName }}</p>
            <p style="width: 600px"
              ><span style="color: gray">端点：</span
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
              :align="{ label: 'left', value: 'left' }"
              :column="6"
              layout="inline-vertical"
            />
          </a-space>
        </div>
      </a-layout-header>
      <a-layout-content>
        <a-tabs
          :default-active-key="activeKey"
          style="width: 100%; height: 100%"
        >
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
              <p id="resultTag" class="tag"
                >运行
                <a-button
                  type="outline"
                  style="margin: 10px; margin-left: 80%"
                  @click="operateNow"
                  >+ 立即执行</a-button
                >
              </p>
              <a-divider />
              <div class="table">
                <a-table :columns="userRunColumns" :data="userRunData">
                  <template #operation="{ record }">
                    <a-space>
                      <a-button @click="onclickRun(record, 'continue')"
                        >继续</a-button
                      >
                      <a-button @click="onclickRun(record, 'pause')"
                        >暂停</a-button
                      >
                      <a-button @click="onclickRun(record, 'stop')"
                        >停止</a-button
                      >
                      <a-button @click="onclickRun(record, 'result')"
                        >结果</a-button
                      >
                      <a-button @click="onclickRun(record, 'delete')"
                        >删除</a-button
                      >
                    </a-space>
                  </template>
                </a-table>
              </div>
            </div>
          </a-tab-pane>
          <a-tab-pane id="overview" key="2" title="测试">
            <div id="var">
              <div id="inputVar">
                <p class="tag" style="margin: 2%"
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

                <div style="position: relative; left: 65%; top: 5%">
                  <a-button type="outline" style="margin: 10px" @click="clear"
                    >清除</a-button
                  >
                  <a-button
                    type="primary"
                    style="margin: 10px"
                    @click="dataSubmit"
                    >提交</a-button
                  >
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

<script lang="ts" setup>
  import { ref, onMounted, reactive } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import axios from 'axios';
  import { Message, Modal } from '@arco-design/web-vue';
  import type {
    jobResponseData,
    testResponseData,
    jobVariables,
  } from '../../api/deployJob';

  const route = useRoute();
  const router = useRouter();
  const jobName = ref('jobName');
  const modelName = ref('modelName');
  jobName.value = route.params.jobName as string; // 工作名称
  modelName.value = route.params.modelName as string; // 模型名称
  const postmsg = ref('');

  const modelUrl = ref(`/detail/${modelName.value}`);

  const activeKey = ref();
  if (route.params.type === 'overview') {
    activeKey.value = '1';
  } else if (route.params.type === 'test') {
    activeKey.value = '2';
  }
  const basicData = reactive([
    {
      label: '类别',
      value: '任务',
    },
    {
      label: '类型',
      value: '批量预测',
    },
    {
      label: '对象',
      value: '-',
    },
    {
      label: '创建时间',
      value: '-',
    },
    {
      label: '运行环境',
      value: '-',
    },
    {
      label: '调度',
      value: '-',
    },
  ]);

  const envVariableColumns = [
    {
      title: '变量',
      dataIndex: 'name',
    },
    {
      title: '值',
      dataIndex: 'value',
    },
  ];
  const userRunColumns = [
    {
      title: 'ID',
      dataIndex: 'id',
    },
    {
      title: '名称',
      dataIndex: 'name',
    },
    {
      title: '开始时间',
      dataIndex: 'createTime',
    },
    {
      title: '持续时间(秒)',
      dataIndex: 'duration',
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
  const paramColumns = [
    {
      title: '顺序',
      dataIndex: 'userSequence',
    },
    {
      title: '参数',
      dataIndex: 'userParam',
    },
  ];
  const inputData = ref(); // 概述页面左边表格数据
  const targetData = ref(); // 概述页面右边表格数据
  const userRunData = ref(); // 概述页面最下面表格数据

  // 测试页面获取的数据
  const runName = ref('');
  const envVariable = ref('');
  const commandParam = ref('');
  const responseData = ref(); // 绑定响应框
  const showCode = ref(); // 显示的curl代码
  const visible = ref(false); // 是否显示悬浮窗

  const initRunData = (data: any) => {
    data.forEach((item: any) => {
      if (item.job_list !== null) {
        item.children = item.job_list;
        delete item.job_list;
      }
    });
    return data;
  };

  // const curTab = ref('1');

  onMounted(async () => {
    // 申请数据
    const param = {
      jobName: jobName.value,
    };
    const res1 = await axios.post<jobResponseData>(
      'http://82.156.5.94:5000/job-info',
      param
    );
    userRunData.value = initRunData(res1.data.runList);
    postmsg.value = res1.data.url.concat(jobName.value); // 获取url
    basicData[2].value = res1.data.modelName;
    basicData[3].value = res1.data.createTime;
    basicData[4].value = res1.data.serverVersion;
    basicData[5].value = res1.data.dispatch;

    const res2 = await axios.post<jobVariables>(
      'http://82.156.5.94:5000/job-variable',
      param
    );
    for (let i = 0; i < res2.data.args.length; i += 1) {
      const newTargetData = {
        userSequence: i,
        userParam: res2.data.args[i],
      };
      targetData.value.push(newTargetData);
    }
    inputData.value = res2.data.env;
  });

  const clear = () => {
    runName.value = '';
    envVariable.value = '';
    commandParam.value = '';
  };

  const dataSubmit = async () => {
    const jobPostData = {
      runName: runName.value,
      variables: envVariable.value,
      args: commandParam.value,
    };
    const res1 = await axios.post<testResponseData>(postmsg.value, jobPostData);
    // console.log(res1.data);

    let returnData = JSON.stringify(res1.data);
    returnData = returnData.replace(/{([^{}]*)}/g, '{\n$1\n    }'); // 在{}对前面加缩进，后面加换行
    returnData = returnData.replace(/(\[)([a-zA-Z0-9'"])/g, '$1\n$2'); // 在[后面加换行
    returnData = returnData.replace(/([a-zA-Z0-9'"])(\])/g, '$1\n$2'); // 在]后面加换行
    returnData = returnData.replace(/,/g, ',\n'); // 在,后面加换行
    responseData.value = returnData;

    const param = {
      jobName: jobName.value,
    };
    const res2 = await axios.post<jobResponseData>(
      'http://82.156.5.94:5000/job-info',
      param
    );
    userRunData.value = initRunData(res2.data.runList);
  };

  const genCode = () => {
    // 构造代码里面的对象
    const codeContent = {
      runName: runName.value,
      variables: envVariable.value,
      args: commandParam.value,
    };

    // 拼接代码
    const urlCode = postmsg.value;
    showCode.value = 'curl --location --request POST '.concat(
      "'",
      urlCode,
      "'"
    );
    showCode.value = showCode.value.concat(
      " --header 'Content-Type:application/json' --data-raw '"
    );
    showCode.value = showCode.value.concat(JSON.stringify(codeContent), "'");

    // 显示浮窗
    visible.value = true;
  };
  const handleOk = () => {
    visible.value = false;
  };

  const operateNow = () => {
    activeKey.value = '2';
    router.push({
      path: `/deployJob/${modelName.value}/${jobName.value}/test`,
    });
  };

  const onclickRun = async (record: any, op: string) => {
    /*
    if (op === 'result') {
      alert('没做');
      return;
    }
    */
    const param = {
      jobName: jobName.value,
      runName: record.name,
      runId: record.id,
      type: op,
    };
    try {
      const res = await axios.post(
        'http://82.156.5.94:5000/operate-run',
        param
      );
      // console.log(res.data);
      if (res.data.status) {
        if (op === 'result') {
          Modal.info({
            content: res.data.res,
          });
          return;
        }
        Message.success('操作成功');
        const res1 = await axios.post<jobResponseData>(
          'http://82.156.5.94:5000/job-info',
          param
        );
        userRunData.value = initRunData(res1.data.runList);
        /*
        if (op === 'result') {
          console.log(1);
        } else if (op === 'delete') {
          userRunData.value.foreach((item: any) => {
            try {
              if (item.runName === record.value) {
                userRunData.value.splice(userRunData.value.indexOf(item), 1);
                throw new Error('break');
              }
            } catch (e: any) {
              if (e.message !== 'break') {
                throw e;
              }
            }
          });
        }
        userRunData.value.foreach((item: any) => {
          try {
            if (item.runName === record.value) {
              item.status = res.data.runStatus;
              throw new Error('break');
            }
          } catch (e: any) {
            if (e.message !== 'break') {
              throw e;
            }
          }
        });
      } else {
        Message.error('失败');
        */
      }
    } catch (error) {
      Message.error(`网络错误：${error}`);
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
    overflow: auto;
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

function foreach(value: any, arg1: (item: any) => void) { throw new
Error('Function not implemented.'); }
