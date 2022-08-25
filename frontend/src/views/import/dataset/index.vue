<template>
  <a-card>
    <a-breadcrumb style="margin-left: 15px">
      <a-breadcrumb-item>主页</a-breadcrumb-item>
      <a-breadcrumb-item
        ><a href="\list\dataset">数据集列表</a></a-breadcrumb-item
      >
      <a-breadcrumb-item>导入数据集</a-breadcrumb-item>
    </a-breadcrumb>
    <a-form
      :model="form"
      auto-label-width
      style="width: 50%; margin-left: auto; margin-right: auto; margin-top: 5%"
      @submit="handleSubmit"
    >
      <a-form-item
        field="fileName"
        label="名称"
        :rules="[{ required: true, message: '请输入数据集名称' }]"
      >
        <a-input v-model="form.fileName" placeholder="请输入数据集名称" />
      </a-form-item>
      <a-form-item
        field="dataSource"
        label="类型"
        :rules="[{ required: true, message: '请选择数据集类型' }]"
      >
        <a-select v-model="form.dataSource" placeholder="请选择数据集类型">
          <a-option value="local">local</a-option>
          <a-option value="remote">remote</a-option>
        </a-select>
      </a-form-item>
      <a-form-item field="file" label="数据集文件">
        <input id="fileUpload" type="file" placeholder="请选择数据集文件" />
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">添加数据集</a-button>
      </a-form-item>
    </a-form>
  </a-card>
</template>

<script lang="ts" setup>
  import { reactive } from 'vue';
  import { useRouter } from 'vue-router';
  import { Message } from '@arco-design/web-vue';
  import axios from 'axios';

  const router = useRouter();

  const form = reactive({
    fileName: '',
    dataSource: '',
  });

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('fileName', form.fileName);
    formData.append('dataSource', form.dataSource);

    const file = document.querySelector('#fileUpload') as HTMLInputElement;
    if (file.files && file.files[0]) {
      formData.append('file', file.files[0]);
    } else {
      Message.error('请选择数据集文件');
    }

    const res = (
      await axios.post('http://82.156.5.94:5000/add-dataset', formData)
    ).data;
    if (res.status) {
      Message.success('添加成功');
      router.push({
        path: '/list/dataset',
      });
    } else {
      Message.error(`导入失败, error type: ${res.detailed}`);
    }
  };
</script>
