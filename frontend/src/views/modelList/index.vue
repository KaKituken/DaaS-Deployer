<template>
  <a-tabs :default-active-key="activeKey">
    <a-tab-pane key="1" title="模型列表">
      <a-card>
        <a-space>
          <div style="font-weight: bold; margin-left: 20px; margin-right: 300px"
            >模型</div
          >
          <a-button style="margin-left: 200px" @click="redirectImport('model')"
            >导入模型</a-button
          >
        </a-space>
        <a-divider />
        <a-table :columns="modelColumns" :data="mData">
          <template #operation="{ record }">
            <a-button @click="onclickColumn(record)">详情</a-button>
          </template>
        </a-table>
      </a-card>
    </a-tab-pane>
    <a-tab-pane key="2" title="数据集列表">
      <a-card>
        <a-space>
          <div style="font-weight: bold; margin-left: 20px; margin-right: 300px"
            >数据集</div
          >
          <a-button
            style="margin-left: 200px"
            @click="redirectImport('dataset')"
            >导入数据集</a-button
          >
        </a-space>
        <a-divider />
        <a-table :columns="datasetColumns" :data="dData">
          <template #operation="{ record }">
            <a-button @click="onclickColumn(record)">详情</a-button>
          </template>
        </a-table>
      </a-card>
    </a-tab-pane>
  </a-tabs>
</template>

<script lang="ts" setup>
  import { onMounted, ref } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import axios from 'axios';

  const router = useRouter();
  const route = useRoute();

  const activeKey = ref('1');
  if (route.params.type === 'dataset') {
    activeKey.value = '2';
  }

  const modelColumns = [
    {
      title: '编号',
      dataIndex: 'key',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: '名称',
      dataIndex: 'modelName',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: '类型',
      dataIndex: 'modelType',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: '创建时间',
      dataIndex: 'createTime',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: '操作',
      slotName: 'operation',
    },
  ];

  const datasetColumns = [
    {
      title: '编号',
      dataIndex: 'key',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: '名称',
      dataIndex: 'name',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: '类型',
      dataIndex: 'type',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: '尺寸',
      dataIndex: 'size',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: '来源',
      dataIndex: 'source',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: '创建时间',
      dataIndex: 'create_time',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
  ];

  const redirectImport = (type: string) => {
    router.push({
      path: `/import/${type}`,
    });
  };
  const onclickColumn = (record: any) => {
    router.push({
      path: `/detail/${record.modelName}`,
    });
  };
  const mData = ref();
  const dData = ref();

  onMounted(async () => {
    const modelData = await axios.get('http://82.156.5.94:5000/model-info');
    mData.value = modelData.data.modelList;
    const datasetData = await axios.get('http://82.156.5.94:5000/dataset-info');
    dData.value = datasetData.data.datasetList;
  });
</script>
