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
          <a-breadcrumb-item>添加服务</a-breadcrumb-item>
          <template #separator>
            <icon-right />
          </template>
        </a-breadcrumb>
        <div class="title">部署 {{ modelName }} 为一项网络服务</div>
      </a-layout-header>
      <a-layout-content>
        <div class="content">
          <a-space direction="vertical" size="large">
            <a-form
              id="form"
              :model="form"
              layout="horizontal"
              @submit="handleSubmit"
            >
              <a-form-item
                field="serviceName"
                label="名称"
                :rules="[{ required: true, message: '请输入服务名称' }]"
              >
                <a-input
                  v-model="form.serviceName"
                  placeholder="请输入名称"
                  @input="nameInput"
                />
              </a-form-item>
              <a-form-item field="serverURL" label="URL">
                <a-input v-model="serverURL" disabled />
              </a-form-item>
              <a-form-item
                field="serverVersion"
                label="模型版本"
                :rules="[{ required: true, message: '请选择模型版本' }]"
              >
                <a-select
                  v-model="form.serverVersion"
                  placeholder="Please select..."
                >
                  <a-option v-for="(item, index) in modelVersion" :key="index">
                    {{ item }}
                  </a-option>
                </a-select>
              </a-form-item>
              <a-form-item field="cpu" label="预留cpu">
                <a-slider
                  v-model="form.cpuReserve"
                  :default-value="0"
                  :min="0"
                  :max="8"
                  :style="{ width: '200px' }"
                />
                <a-input-number
                  v-model="form.cpuReserve"
                  :default-value="0"
                  :min="0"
                  :max="8"
                  :precision="0"
                  placeholder="0~8"
                  :style="{ width: '90px', margin: '0 0 0 50px' }"
                />
              </a-form-item>
              <a-form-item field="memory" label="预留内存(M)">
                <a-slider
                  v-model="form.memoryReserve"
                  :default-value="0"
                  :min="0"
                  :max="4096"
                  :step="1"
                  :style="{ width: '200px' }"
                />
                <a-input-number
                  v-model="form.memoryReserve"
                  :default-value="0"
                  :min="0"
                  :max="4093"
                  :step="1"
                  :precision="1"
                  placeholder="0~4096"
                  :style="{ width: '90px', margin: '0 0 0 50px' }"
                />
              </a-form-item>
              <a-form-item
                field="replicas"
                label="副本"
                :rules="[{ required: true, message: '请输入副本数量' }]"
              >
                <a-input-number v-model="form.replicas" :default-value="2" />
              </a-form-item>
              <a-form-item>
                <a-button type="primary" html-type="submit">添加模型</a-button>
              </a-form-item>
            </a-form>
            {{ form }}
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
  import { useRoute, useRouter } from 'vue-router';
  import { Message } from '@arco-design/web-vue';
  import type { addService, modelDeploy, status } from '../../api/addService';
  import type { modelDescript } from '../../api/modelOverview';

  const route = useRoute();
  const router = useRouter();
  const serverURL = ref();
  const serverURLpred = ref('');
  const modelName = ref('modelName');
  modelName.value = route.params.modelname as string;
  const modelUrl = ref(`/detail/${modelName.value}`);
  const form = reactive({
    modelName: modelName.value,
    modelType: '',
    serviceName: '',
    serverVersion: 'test',
    cpuReserve: 0,
    memoryReserve: 0,
    replicas: 2,
  });
  const modelVersion = ref();
  onMounted(async () => {
    const res1 = await axios.get<modelDeploy>(
      'http://82.156.5.94:5000/env-version'
    );
    modelVersion.value = res1.data.version;

    const res2 = await axios.get<addService>(
      'http://82.156.5.94:5000/model-deploy-service'
    );
    serverURLpred.value = res2.data.restfulUrl;
    serverURL.value = res2.data.restfulUrl;

    const param = {
      modelName: modelName.value,
    };
    const res3 = await axios.post<modelDescript>(
      'http://82.156.5.94:5000/model-descript',
      param
    );
    form.modelType = res3.data.modelType;
  });

  const nameInput = () => {
    serverURL.value = serverURLpred.value.concat(form.serviceName);
  };
  const handleSubmit = async () => {
    const res = await axios.post<status>(
      'http://82.156.5.94:5000/model-deploy-service',
      form
    );
    if (res.data.status === true) {
      Message.success('添加服务成功');
      router.push({
        path: `/deployService/${modelName.value}/${form.serviceName}`,
      });
    } else {
      Message.error('添加服务失败，请重试');
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
    margin: 20px 0 0 19%;
    font-weight: bold;
  }

  .content {
    width: 94%;
    height: 500px;
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
