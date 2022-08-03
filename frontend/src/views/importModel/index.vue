<template>
  <a-card>
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
        <a-input v-model="form.name" placeholder="请输入名称" />
      </a-form-item>
      <a-form-item field="desc" label="描述">
        <a-textarea v-model="form.desc" placeholder="请输入模型描述（可选）" />
      </a-form-item>
      <a-form-item
        field="type"
        label="类型"
        :rules="[{ required: true, message: '请选择模型类型' }]"
      >
        <a-select v-model="form.type" placeholder="请选择模型类型">
          <a-option value="PMML">PMML</a-option>
          <a-option value="ONNX">ONNX</a-option>
        </a-select>
      </a-form-item>
      <a-form-item
        field="file"
        label="模型文件"
        :rules="[{ required: true, message: '请选择模型文件' }]"
      >
        <a-input v-model="form.file" type="file" placeholder="请选择模型文件" />
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">添加模型</a-button>
      </a-form-item>
    </a-form>
    {{ form }}
  </a-card>
</template>

<script lang="ts" setup>
  import { reactive } from 'vue';

  const form = reactive({
    name: '',
    desc: '',
    type: '',
    file: '',
  });
  const handleSubmit = () => {
    alert('没做');
  };
  

</script>
