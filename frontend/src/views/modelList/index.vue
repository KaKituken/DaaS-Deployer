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
            <a-space>
              <a-button @click="onclickColumn(record)">详情</a-button>
              <a-button @click="onclickDeleteModel(record)">删除</a-button>
            </a-space>
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
            <a-space>
              <a-button @click="onclickDeleteDataset(record)">删除</a-button>
              <a-button><a :href="`http://82.156.5.94:5000/download/`+ record.name " style="text-decoration: none">下载</a></a-button>
            </a-space>
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
  import { Message } from '@arco-design/web-vue';
  import type { status } from '../../api/addService';
  import type {download} from '../../api/modelOverview'


  const router = useRouter();
  const route = useRoute();

  const activeKey = ref('1');
  if (route.params.type === 'dataset') {
    activeKey.value = '2';
  }

  const modelColumns = [
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
    {
      title: '操作',
      slotName: 'operation',
    },
  ];
  const mData = ref();
  const dData = ref();
  
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
  const onclickDeleteModel = async (record: any) => {
    const params = {
      modelName: record.modelName,
      operation: "delete"
    }
    const res = await axios.post<status>(
      'http://82.156.5.94:5000/operate-model',
      params
    )
    if(res.data.status === false){
      Message.error(`删除模型失败，error type: ${res.data.detailed}`)
    }
    else{
      Message.success('删除模型成功')
      const modelData = await axios.get('http://82.156.5.94:5000/model-info');
      mData.value = modelData.data.modelList;
    }
  };
  const onclickDeleteDataset = async (record: any) => {
    const params = {
      dataset: record.name,
      operation: "delete"
    }
    const res = await axios.post<status>(
      'http://82.156.5.94:5000/operate-dataset',
      params
    )
    if(res.data.status === false){
      Message.error(`删除数据集失败，error type: ${res.data.detailed}`)
    }
    else{
      Message.success('删除数据集成功')
      const datasetData = await axios.get('http://82.156.5.94:5000/dataset-info');
      dData.value = datasetData.data.datasetList;
    }
  }

  onMounted(async () => {
    const modelData = await axios.get('http://82.156.5.94:5000/model-info');
    mData.value = modelData.data.modelList;
    const datasetData = await axios.get('http://82.156.5.94:5000/dataset-info');
    dData.value = datasetData.data.datasetList;
  });
</script>