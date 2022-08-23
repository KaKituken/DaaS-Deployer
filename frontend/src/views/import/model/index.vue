<template>
  <a-card>
    <a-breadcrumb style="margin-left: 15px">
      <a-breadcrumb-item>主页</a-breadcrumb-item>
      <a-breadcrumb-item><a href="\list\model">模型列表</a></a-breadcrumb-item>
      <a-breadcrumb-item>导入模型</a-breadcrumb-item>
    </a-breadcrumb>
    <a-form
      :model="form"
      auto-label-width
      style="width: 50%; margin-left: auto; margin-right: auto; margin-top: 5%"
      @submit="handleSubmit"
    >
      <a-form-item
        field="name"
        label="名称"
        :rules="[{ required: true, message: '请输入模型名称' }]"
      >
        <a-input v-model="form.name" placeholder="请输入模型名称" />
      </a-form-item>
      <a-form-item field="descript" label="描述">
        <a-textarea
          v-model="form.descript"
          placeholder="请输入模型描述（可选）"
        />
      </a-form-item>
      <a-form-item
        field="type"
        label="类型"
        :rules="[{ required: true, message: '请选择模型类型' }]"
      >
        <a-select v-model="form.type" placeholder="请选择模型类型">
          <a-option value="pmml">pmml</a-option>
          <a-option value="onnx">onnx</a-option>
        </a-select>
      </a-form-item>
      <a-form-item field="file" label="模型文件">
        <input id="fileUpload" type="file" placeholder="请选择模型文件" />
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">添加模型</a-button>
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
    name: '',
    descript: '',
    type: '',
  });

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('name', form.name);
    formData.append('descript', form.descript);
    formData.append('type', form.type);

    const file = document.querySelector('#fileUpload') as HTMLInputElement;
    if (file.files && file.files[0]) {
      formData.append('file', file.files[0]);
    } else {
      Message.error('请选择模型文件');
    }

    const res = (
      await axios.post('http://82.156.5.94:5000/model-upload', formData)
    ).data;
    if (res.status) {
      Message.success('添加成功');
      router.push({
        path: '/list/model',
      });
    } else {
      Message.error('错误：重名模型');
    }
  };
</script>
