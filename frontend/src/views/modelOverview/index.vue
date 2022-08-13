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
              column="4"
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
                <a-button id="addService"
                  ><a :href="addServiceUrl">+ 添加服务</a></a-button
                >
                <a-button id="addTask">+ 添加任务</a-button>
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
                    minWidth: '500px',
                    border: '1px solid var(--color-border)',
                  }"
                  disabled="True"
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
                          <span class="tag" style="margin: 10px">输入</span>
                          <span
                            style="
                              position: relative;
                              left: 450px;
                              color: #165dff;
                            "
                            >JSON</span
                          >
                        </div>
                        <a-list>
                          <a-list-item>
                            &nbsp;&nbsp;&nbsp;sepal-length (cm)<br />
                            <a-input
                              v-model="getData.slength"
                              :style="{
                                'width': '520px',
                                'margin': '2px',
                                'background-color': 'white',
                                'border-style': 'solid',
                                'border-color': 'gray',
                                'border-radius': '5px',
                              }"
                              placeholder=""
                              allow-clear
                            />
                          </a-list-item>
                          <a-list-item>
                            &nbsp;&nbsp;&nbsp;sepal-width (cm)<br />
                            <a-input
                              v-model="getData.swidth"
                              :style="{
                                'width': '520px',
                                'margin': '2px',
                                'background-color': 'white',
                                'border-style': 'solid',
                                'border-color': 'gray',
                                'border-radius': '5px',
                              }"
                              placeholder=""
                              allow-clear
                            />
                          </a-list-item>
                          <a-list-item>
                            &nbsp;&nbsp;&nbsp;petal-length (cm)<br />
                            <a-input
                              v-model="getData.plength"
                              :style="{
                                'width': '520px',
                                'margin': '2px',
                                'background-color': 'white',
                                'border-style': 'solid',
                                'border-color': 'gray',
                                'border-radius': '5px',
                              }"
                              placeholder=""
                              allow-clear
                            />
                          </a-list-item>
                          <a-list-item>
                            &nbsp;&nbsp;&nbsp;petal-width (cm)<br />
                            <a-input
                              v-model="getData.pwidth"
                              :style="{
                                'width': '520px',
                                'margin': '2px',
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
                        <div style="text-align: right">
                          <a-button
                            type="outline"
                            style="margin: 10px"
                            @click="clear"
                            >清除</a-button
                          >
                          <a-button type="primary" style="margin: 10px"
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
                          <span class="tag" style="margin: 10px">输出</span>
                        </div>
                        <a-divider style="position: relative; top: -10px" />
                        <div id="testout" style="height: 362px">
                          <a-textarea
                            v-model="output"
                            placeholder="Please enter something"
                            allow-clear
                            style="
                              background-color: white;
                              margin: 20px;
                              position: relative;
                              top: -20px;
                              width: 560px;
                              border-style: solid;
                              border-color: gray;
                              height: 80%;
                            "
                          />
                        </div>
                      </div>
                    </a-typography-paragraph>
                  </template>
                </a-split>
              </div>
            </div>
          </a-tab-pane>
          <a-tab-pane key="4" title="实时预测">
            Content of Tab Panel 4
          </a-tab-pane>
          <a-tab-pane key="5" title="批量预测">
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
  import type { modelDescript, modelVariable } from '../../api/modelOverview';

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

  const getData = reactive([
    {
      label: 'slength',
      value: '',
    },
    {
      label: 'swidth',
      value: '',
    },
    {
      label: 'plength',
      value: '',
    },
    {
      label: 'pwidth',
      value: '',
    },
    {
      label: 'output',
      value: '',
    },
  ]);

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
      title: '取值',
      dataIndex: 'valueRange',
    },
  ];
  const inputData = ref();
  const targetData = ref();
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

  onMounted(async () => {
    const res1 = await axios.post<modelDescript>(
      'http://82.156.5.94:5000/model-descript',
      param
    );
    modelDescription.value = res1.data.descript;
    data[1].value = res1.data.modelType;
    data[2].value = res1.data.algorithm;
    data[3].value = res1.data.modelEngine;

    const res2 = await axios.post<modelVariable>(
      'http://82.156.5.94:5000/model-variable',
      param
    );
    inputData.value = res2.data.inputVariables;
    targetData.value = res2.data.outputVariables;
  });
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
</style>
