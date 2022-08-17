<template>
  <div class="layout-demo">
    <a-layout style="min-height: 600px">
      <a-layout-header>
        <a-breadcrumb style="margin-left: 15px">
          <a-breadcrumb-item>主页</a-breadcrumb-item>
          <a-breadcrumb-item><a href="/list">模型</a></a-breadcrumb-item>
          <a-breadcrumb-item
            ><a :href="modelUrl">{{ modelName }}</a></a-breadcrumb-item
          >
          <a-breadcrumb-item>批量预测高级设置</a-breadcrumb-item>
          <template #separator>
            <icon-right />
          </template>
        </a-breadcrumb>
        <div class="title">{{ modelName }} 批量预测高级设置</div>
      </a-layout-header>
      <a-layout-content>
        <div class="content">
          <a-space direction="vertical" size="large">
            <a-form
              :model="form"
              layout="horizontal"
              @submit="handleSubmit"
              id="form"
            >
              <a-form-item
                field="filename"
                label="文件名"
                :rules="[{ required: true }]"
              >
                <a-input v-model="form.fileName" placeholder="请输入文件名" />
              </a-form-item>
              <a-form-item field="ext" label="扩展名">
                <a-select v-model="form.ext">
                  <a-option v-for="(item, index) in extList" :key="index">
                    {{ item }}
                  </a-option>
                </a-select>
              </a-form-item>
              <a-form-item
                field="jobName"
                label="任务名称"
                :rules="[{ required: true }]"
              >
                <a-input v-model="form.jobName" />
              </a-form-item>
              <a-form-item
                field="jobDescription"
                label="任务描述"
                :rules="[{ required: true }]"
              >
                <a-textarea
                  placeholder="在这里进行任务描述..."
                  allow-clear
                ></a-textarea>
              </a-form-item>
              <a-form-item field="environment" label="任务运行环境">
                <a-select v-model="form.environment">
                  <a-option
                    v-for="(item, index) in environmentList"
                    :key="index"
                  >
                    {{ item }}
                  </a-option>
                </a-select>
              </a-form-item>
              <a-form-item field="variables" label="环境变量">
                <a-input v-model="form.variables" />
              </a-form-item>
              <a-form-item field="args" label="命令参数">
                <a-input v-model="form.args"></a-input>
              </a-form-item>
              <a-form-item
                field="dispatch"
                label="调度"
                :rules="[{ required: true }]"
              >
                <a-radio-group>
                  <a-radio value="demand">按需</a-radio>
                  <a-radio value="schedule">按调度</a-radio>
                </a-radio-group>
              </a-form-item>
              <a-form-item
                field="runName"
                label="运行名称"
                :rules="[{ required: true }]"
              >
                <a-input v-model="form.runName"></a-input>
              </a-form-item>
              <a-form-item>
                <a-button type="primary" html-type="submit">保存</a-button>
              </a-form-item>
            </a-form>
          </a-space>
        </div>
      </a-layout-content>
      <a-layout-footer></a-layout-footer>
    </a-layout>
  </div>
</template>

<script lang="ts" setup>
  import { ref, onMounted, reactive } from 'vue';
  import axios from 'axios';
  import { useRoute } from 'vue-router';
  import type { modelDeploy, addService } from '../../api/addService';

  const route = useRoute();
  const modelName = ref('modelName');
  modelName.value = route.params.modelname as string;
  const modelUrl = ref(`/detail/${modelName.value}`);
  const extList = ref();
  const environmentList = ref();
  const form = reactive({
    fileName: '',
    ext: '',
    jobName: '',
    jobDescription: '',
    environment: '',
    variables: '',
    args: '',
    dispatch: '',
    runName: '',
  });

  const param = {
    modelName: modelName.value,
  };
  onMounted(async () => {
    const res = await axios.post<modelDeploy>(
      'http://82.156.5.94:5000/model-deploy-service',
      param
    );
  });

  const handleSubmit = async () => {
    const res = await axios.post<addService>(
      'http://82.156.5.94:5000/model-deploy-service',
      form
    );
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
    flex-direction: column;
    height: 100px;
    background-color: #fff;
  }

  .layout-demo :deep(.arco-layout-content) {
    background-color: #f5f5f5;
  }

  .layout-demo :deep(.arco-layout-footer) {
    height: 25px;
    margin-top: 20px;
    margin-right: 2%;
    margin-left: 2%;
    background-color: #f5f5f5;
  }

  .title {
    font-size: 22px;
    margin: 20px 0 0 16%;
    font-weight: bold;
  }

  .content {
    width: 94%;
    height: 600px;
    margin-top: 3%;
    margin-left: 3%;
    margin-right: 3%;
    background-color: #fff;
  }

  #form {
    width: 600px;
    margin-left: 10%;
    margin-right: 10%;
    margin-top: 5%;
  }
</style>
