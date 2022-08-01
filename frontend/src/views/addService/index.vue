<template>
    <div class="layout-demo">
        <a-layout style="min-height: 600px">
            <a-layout-header>
                <a-breadcrumb style="margin-left: 15px">
                    <a-breadcrumb-item>主页</a-breadcrumb-item>
                    <a-breadcrumb-item>模型</a-breadcrumb-item>
                    <a-breadcrumb-item>{{ modelName }}</a-breadcrumb-item>
                    <a-breadcrumb-item>添加服务</a-breadcrumb-item>
                    <template #separator>
                        <icon-right />
                    </template>
                </a-breadcrumb>
                <div class="title">部署 {{ modelName }} 为一项网络服务</div>
            </a-layout-header>
            <a-layout-content>
                <div class='content'>
                  <a-space direction="vertical" size="large">
                    <a-form :model="form" layout="horizontal" @submit="handleSubmit" id="form">
                      <a-form-item field="name" label="名称" :rules="[{ required: true }]">
                        <a-input v-model="form.name" placeholder="请输入名称" />
                      </a-form-item>
                      <a-form-item field="serverURL" label="URL">
                        <a-input v-model="serverURL" disabled/>
                      </a-form-item>
                      <a-form-item field="modelVersion" label="模型版本" :rules="[{ required: true }]">
                        <a-select v-model="form.modelVersion"  placeholder="Please select...">
                          <a-option v-for="(item, index) in modelVersion" :key="index">
                            {{ item }}
                          </a-option>
                        </a-select>
                      </a-form-item>
                      <a-form-item field="environment" label="运行环境" :rules="[{ required: true }]">
                        <a-select v-model="form.environment" placeholder="Please select...">
                          <a-option v-for="(item, index) in environment" :key="index">
                            {{ item }}
                          </a-option>
                        </a-select>
                      </a-form-item>
                      <a-form-item field="cpu" label="预留cpu">
                        <a-slider v-model="form.cpu" :default-value=0 min=0 max=8 :style="{ width: '200px' }"/>
                        <a-input-number v-model="form.cpu" :default-value=0 min=0 max=8 precision="0" placeholder="0~8" :style="{width:'85px',margin:'0 0 0 50px'}" />
                      </a-form-item>
                      <a-form-item field="memory" label="预留内存(G)">
                        <a-slider v-model="form.memory" :default-value=0 min=0.0 max=32.0 step=0.1 :style="{ width: '200px' }" />
                        <a-input-number v-model="form.memory" :default-value=0 min=0.0 max=32.0 step=0.1 precision="1" placeholder="0~32.0" :style="{width:'85px',margin:'0 0 0 50px'}" />
                      </a-form-item>
                      <a-form-item field="copyNum" label="副本">
                        <a-input-number v-model="form.copyNum" :default-value="1"/>
                      </a-form-item>
                      <a-form-item>
                        <a-button type="primary" html-type="submit">添加模型</a-button>
                      </a-form-item>
                    </a-form>
                  </a-space>
                </div>
            </a-layout-content>
            <a-layout-footer></a-layout-footer>
        </a-layout>
    </div>
</template>

<script type="ts" setup>
    import { ref,onMounted,reactive } from 'vue'
    import axios from 'axios'

    const serverURL = ref();
    const modelName = ref('xgb-iris');
    const form = reactive({
      name:'',
      modelVersion:'',
      environment:'',
      cpu:'',
      memory:'',
      copyNum:'',
    });
    const modelVersion = ref();
    const environment = ref();
    
    onMounted(()=>{
        axios.get('/api/modelOverview/info')
        .then(response=>{
            modelName.value = response.data.modelName;
        })

        axios.get('/api/modelDeploy/info')
        .then(response=>{
            serverURL.value = response.data.serverURL;
        })

        axios.get('/api/modelDeploy/info')
        .then(response=>{
            modelVersion.value = response.data.modelVersion;
            environment.value = response.data.environment;
        })
    });

    const handleSubmit = () => {
      alert('没做');
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

  .title{
    font-size:22px;
    margin:20px 0 0 19%;
    font-weight:bold;
  }

  .content{
    width:94%;
    height:500px;
    margin-top:3%;
    margin-left:3%;
    margin-right:3%;
    background-color:#fff;
  }

  #form{
    width: 600px;
    margin-left: 10%;
    margin-right: 10%;
    margin-top: 5%;
  }
</style>