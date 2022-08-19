<template>
  <div class="layout-demo">
    <a-layout style="min-height: 850px">
      <a-layout-header>
        <div>
          <a-breadcrumb style="margin-left: 15px">
            <a-breadcrumb-item>主页</a-breadcrumb-item>
            <a-breadcrumb-item><a href="\list">模型</a></a-breadcrumb-item>
            <a-breadcrumb-item>{{ modelName }}</a-breadcrumb-item>
            <template #separator>
              <icon-right />
            </template>
          </a-breadcrumb>
          <div id="basicInfo">
            <p style="font-weight: bold; font-size: 22px">{{ modelName }}</p>
            <p style="color: grey">{{ modelDescription }}</p>
          </div>
        </div>
        <div id="detailInfo">
          <a-space direction="vertical" size="medium" fill>
            <a-descriptions
              :data="data"
              size="small"
              :align="{ label: 'right', value: 'right' }"
              :column="4"
              layout="inline-vertical"
            />
          </a-space>
        </div>
      </a-layout-header>
      <a-layout-content>
        <a-tabs default-active-key="1" style="width: 100%; height: 100%">
          <a-tab-pane id="overview" key="1" title="概述">
            <div id="var">
              <div id="inputVar">
                <p class="tag">输入变量</p>
                <a-divider />
                <div class="table">
                  <a-table :columns="inputColumns" :data="inputData" />
                </div>
              </div>
              <div id="targetVar">
                <p class="tag">目标变量</p>
                <a-divider />
                <div class="table">
                  <a-table :columns="inputColumns" :data="targetData" />
                </div>
              </div>
            </div>
            <div id="result">
              <p id="resultTag" class="tag">评估结果</p>
              <a-divider />
              <a-empty />
            </div>
          </a-tab-pane>
          <a-tab-pane key="2" title="部署">
            <div id="deploy">
              <div id="deployheader">
                <p class="tag" style="margin-top: 0; padding-top: 15px">部署</p>
                <a-button id="addService" type="primary"
                  ><a :href="addServiceUrl" style="text-decoration: none"
                    >+ 添加服务</a
                  ></a-button
                >
                <a-button id="addTask" type="primary">+ 添加任务</a-button>
              </div>
              <a-divider style="margin-top: 0" />
              <div class="table">
                <a-table :columns="deployColumns" :data="deployData" />
              </div>
              <a-divider />
            </div>
          </a-tab-pane>
          <a-tab-pane key="3" title="测试">
            <div id="test">
              <div style="background-color: #f5f5f5">
                <a-split
                  :style="{
                    height: '600px',
                    width: '100%',
                    minWidth: '250px',
                    border: '1px solid var(--color-border)',
                  }"
                  disabled
                >
                  <template #first>
                    <a-typography-paragraph>
                      <div
                        style="
                          background-color: white;
                          margin: 10px;
                          border-radius: 10px;
                        "
                      >
                        <div class="testtitle" style="margin: 10px">
                          <span
                            class="tag"
                            style="margin: 10px; text-align: left"
                            >输入</span
                          >
                          <a
                            style="
                              text-align: right;
                              color: #165dff;
                              text-decoration: none;
                            "
                            href="#"
                            @click="changeJson"
                            >JSON</a
                          >
                        </div>
                        <a-list v-if="!weatherJson" style="margin: 1%">
                          <a-list-item
                            v-for="(item, index) in nameValueList"
                            :key="index"
                          >
                            &nbsp;&nbsp;&nbsp;{{ item['name'] }}
                            <a-input
                              v-model="item.value"
                              :style="{
                                'width': '96%',
                                'margin': '2%',
                                'background-color': 'white',
                                'border-style': 'solid',
                                'border-color': 'gray',
                                'border-radius': '5px',
                              }"
                              placeholder=""
                              allow-clear
                            />
                          </a-list-item>
                        </a-list>
                        <div v-if="weatherJson" style="height: 362px">
                          <a-textarea
                            v-model="userJson"
                            allow-clear
                            style="
                              background-color: white;
                              margin: 5%;
                              position: relative;
                              width: 90%;
                              border-style: solid;
                              border-color: gray;
                              height: 80%;
                            "
                          />
                        </div>

                        <div style="text-align: right">
                          <a-button
                            type="outline"
                            style="margin: 10px"
                            @click="clear"
                            >清除</a-button
                          >
                          <a-button
                            type="primary"
                            style="margin: 10px"
                            @click="testSubmit"
                            >提交</a-button
                          >
                        </div>
                      </div>
                    </a-typography-paragraph>
                  </template>
                  <template #second>
                    <a-typography-paragraph>
                      <div
                        style="
                          background-color: white;
                          margin: 10px;
                          border-radius: 10px;
                        "
                      >
                        <div class="testtitle" style="margin: 10px">
                          <span
                            class="tag"
                            style="margin: 10px; text-align: left"
                            >输出</span
                          >
                        </div>
                        <a-divider style="position: relative; top: -10px" />
                        <div id="testout" style="height: 362px; margin: 1%">
                          <a-textarea
                            v-model="testOutput"
                            allow-clear
                            style="
                              background-color: white;
                              margin: 2%;
                              width: 95%;
                              border-style: solid;
                              border-color: gray;
                              height: 80%;
                            "
                            disabled
                          />
                        </div>
                      </div>
                    </a-typography-paragraph>
                  </template>
                </a-split>
              </div>
            </div>
          </a-tab-pane>
          <a-tab-pane key="4" title="批量预测">
            <div id="barchPred">
              <div id="batchPredSettings">
                <a-card
                  style="width: 100%; height: 100%"
                  title="批预测脚本设置"
                >
                  <a-form
                    id="predForm"
                    :model="predForm"
                    layout="vertical"
                    @submit="BatchPredFunc"
                  >
                    <a-form-item
                      field="inputDataset"
                      label="输入数据集"
                      placeholder="Please select..."
                      :rules="[{ required: true }]"
                    >
                      <a-select v-model="predForm.inputDataset">
                        <a-option
                          v-for="(item, index) in datasetList"
                          :key="index"
                        >
                          {{ item.name }}
                        </a-option>
                      </a-select>
                    </a-form-item>
                    <a-form-item
                      field="outputDataset"
                      label="输出数据集"
                      :rules="[{ required: true }]"
                    >
                      <a-input v-model="predForm.outputDataset" />
                    </a-form-item>
                    <a-form-item>
                      <a-button type="primary" html-type="submit"
                        >生成批预测脚本</a-button
                      >
                    </a-form-item>
                  </a-form>
                </a-card>
              </div>
              <div id="PredResult">
                <a-card style="width: 100%; height: 100%" title="结果">
                  <template #extra>
                    <a-link :href="batchPredSettingsUrl">高级设置</a-link>
                  </template>
                  <a-textarea
                    v-model="predScript"
                    style="width: 96%; height: 270px"
                    disabled
                  />
                  <a-button
                    type="primary"
                    style="float: right; margin-top: 10px"
                    @click="runBatchPredFunc()"
                    >立即执行</a-button
                  >
                </a-card>
              </div>
            </div>
          </a-tab-pane>
          <a-tab-pane key="5" title="实时预测">
            Content of Tab Panel 5
          </a-tab-pane>
          <a-tab-pane key="6" title="模型评估">
            Content of Tab Panel 6
          </a-tab-pane>
          <a-tab-pane key="7" title="关联脚本">
            Content of Tab Panel 7
          </a-tab-pane>
        </a-tabs>
      </a-layout-content>
      <a-layout-footer> </a-layout-footer>
    </a-layout>
  </div>
</template>

<script lang="ts" setup>
  import { ref, onMounted, reactive } from 'vue';
  import axios from 'axios';
  import { useRoute } from 'vue-router';
  import type {
    modelDescript,
    modelVariable,
    DatasetInfo,
    DatasetList,
    PredictScript,
    modelTestInfo,
  } from '../../api/modelOverview';

  const route = useRoute();
  const modelName = ref('modelName');
  modelName.value = route.params.modelname as string;
  const addServiceUrl = ref(`/addService/${modelName.value}`);

  const modelDescription = ref('this is a simple introduction of the model...');
  const data = reactive([
    {
      label: '修改时间',
      value: '',
    },
    {
      label: '类型',
      value: '',
    },
    {
      label: '算法',
      value: '',
    },
    {
      label: '引擎',
      value: '',
    },
  ]);

  const getData = reactive({
    slength: '',
    swidth: '',
    plength: '',
    pwidth: '',
  });

  const testOutput = ref('');
  const weatherJson = ref(false);
  const userJson = ref(''); // json格式下用户输入

  const inputColumns = [
    {
      title: '字段',
      dataIndex: 'name',
    },
    {
      title: '类型',
      dataIndex: 'dataType',
    },
    {
      title: '测量',
      dataIndex: 'optype',
    },
    {
      title: '维数',
      dataIndex: 'shape',
    },
    {
      title: '取值',
      dataIndex: 'valueRange',
    },
  ];

  const inputData = ref();
  const targetData = ref();
  const nameValueList = ref();

  const deployColumns = [
    {
      title: '名称',
      dataIndex: 'name',
    },
    {
      title: '类型',
      dataIndex: 'type',
    },
    {
      title: '开始时间',
      dataIndex: 'startTime',
    },
    {
      title: '状态',
      dataIndex: 'status',
    },
    {
      title: '操作',
      dataIndex: 'operation',
    },
  ];
  const deployData = reactive([]);

  const param = {
    modelName: modelName.value,
  };

  const datasetList = ref();
  const predForm = reactive({
    modelName: modelName.value,
    modelType: data[1].value,
    inputDataset: '',
    outputDataset: '',
  });
  const predScript = ref();
  const batchPredSettingsUrl = ref(`/batchPredictSettings/${modelName.value}`);
  const runBatchPredFunc = async () => {
    await axios.post('http://82.156.5.94:5000/model-deploy-job', predForm);
  };

  const BatchPredFunc = async () => {
    const res4 = await axios.post<PredictScript>(
      'http://82.156.5.94:5000/generate-script',
      predForm
    );
    predScript.value = res4.data.code;
  };

  onMounted(async () => {
    const res1 = await axios.post<modelDescript>(
      'http://82.156.5.94:5000/model-descript',
      param
    );
    modelDescription.value = res1.data.descript;
    data[0].value = res1.data.createTime;
    data[1].value = res1.data.modelType;
    data[2].value = res1.data.algorithm;
    data[3].value = res1.data.modelEngine;

    const res2 = await axios.post<modelVariable>(
      'http://82.156.5.94:5000/model-variable',
      param
    );

    console.log(res2.data);
    inputData.value = res2.data.inputVariables;
    targetData.value = res2.data.outputVariables;
    // 根据获取的inputData构造nameValueList用于绑定 不定数量的输入框
    nameValueList.value = (() => {
      const arr = Array(inputData.value.length);
      for (let i = 0; i < inputData.value.length; i += 1) {
        arr[i] = {
          name: inputData.value[i].name,
          value: '',
        };
      }
      return arr;
    })();

    const res3 = await axios.post<DatasetList>(
      'http://82.156.5.94:5000/dataset-info',
      param
    );
    datasetList.value = res3.data.datasetList;
  });

  const testSubmit = async () => {
    let testInfo = {};
    if (!weatherJson.value) {
      testInfo = {
        modelName: modelName.value,
        data: {
          inputs: nameValueList.value,
        },
      };
    } else {
      const userData = JSON.parse(userJson.value.replace(/[\r\n\s+]/g, '')); // 从输入框获取用户输入的json字符串，然后解析
      // 构造一个提交的数据表单
      const newNameValueList = (() => {
        const arr = Array(Object.getOwnPropertyNames(userData).length);
        for (
          let i = 0;
          i < Object.getOwnPropertyNames(userData).length;
          i += 1
        ) {
          arr[i] = {
            name: nameValueList.value[i].name,
            value: userData[nameValueList.value[i].name.replace(/ /g, '')],
            // 注意json解析的时候会自动忽略所有空格，所以需要手动按照去掉空格的属性名从用户输入的json中提取属性值
          };
        }
        return arr;
      })();
      // 注意： 用户输入的json的属性名必须加""，目前可以解决json里面的回车字符串，但是不能解决属性名没有""产生的解析错误
      testInfo = {
        modelName: modelName.value,
        data: {
          inputs: newNameValueList,
        },
      };
    }

    console.log(testInfo);

    const res1 = await axios.post<modelTestInfo>(
      'http://82.156.5.94:5000/model-test',
      testInfo
    );
    let returnData = JSON.stringify(res1.data);
    returnData = returnData.replace(/{([^{}]*)}/g, '{\n$1\n    }'); // 在{}对前面加缩进，后面加换行
    returnData = returnData.replace(/(\[)([a-zA-Z0-9'"])/g, '$1\n$2'); // 在[后面加换行
    returnData = returnData.replace(/([a-zA-Z0-9'"])(\])/g, '$1\n$2'); // 在]后面加换行
    returnData = returnData.replace(/,/g, ',\n'); // 在,后面加换行
    testOutput.value = returnData;
  };

  const clear = () => {
    nameValueList.value = (() => {
      const arr = Array(inputData.value.length);
      for (let i = 0; i < inputData.value.length; i += 1) {
        arr[i] = {
          name: inputData.value[i].name,
          value: '',
        };
      }
      return arr;
    })();

    if (!weatherJson.value) {
      // 输入框清空
      for (let i = 0; i < nameValueList.value.length; i += 1) {
        nameValueList.value[i].value = '';
      }
    } else {
      userJson.value = ''; // 文本框清空
    }
  };

  const changeJson = () => {
    weatherJson.value = !weatherJson.value;
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

  #basicInfo {
    width: 350px;
    margin-left: 20px;
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
    height: 400px;
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

  #deployheader {
    display: flex;
    flex-direction: row;
  }

  #deployheader #addService {
    justify-content: flex-end;
    margin-top: 15px;
    margin-right: 0;
    margin-bottom: 15px;
    margin-left: auto;
  }

  #deployheader #addTask {
    justify-content: flex-end;
    margin-top: 15px;
    margin-right: 50px;
    margin-bottom: 15px;
    margin-left: 10px;
  }

  #test {
    background-color: white;
  }

  #barchPred {
    display: flex;
  }
  #batchPredSettings {
    width: 30%;
    height: 400px;
    margin-left: 2%;
    background-color: #fff;
  }
  #PredResult {
    width: 64%;
    height: 400px;
    margin-left: 2%;
    background-color: #fff;
  }
</style>
