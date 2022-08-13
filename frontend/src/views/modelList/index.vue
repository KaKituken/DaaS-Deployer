<template>
  <a-card>
    <a-space>
      <div style="font-weight: bold; margin-left: 20px; margin-right: 300px"
        >模型</div
      >
      <a-button style="margin-left: 200px" @click="redirectImport"
        >导入模型</a-button
      >
    </a-space>
    <a-divider />
    <a-table :columns="columns" :data="data">
      <template #operation="{ record }">
        <a-button @click="onclickColumn(record)">详情</a-button>
      </template>
    </a-table>
  </a-card>
</template>

<script lang="ts" setup>
  import { reactive } from 'vue';
  import { useRouter } from 'vue-router';

  const router = useRouter();

  const columns = [
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
      title: '更新时间',
      dataIndex: 'time',
      sortable: {
        sortDirections: ['ascend', 'descend'],
      },
    },
    {
      title: '操作',
      slotName: 'operation',
    },
  ];
  const data = reactive([
    {
      key: '1',
      name: '测试样例',
      type: 'PMML',
      time: 'some time 我也不知道会怎么呈现',
    },
  ]);

  const redirectImport = () => {
    router.push({
      name: 'import',
    });
  };
  const onclickColumn = (record: any) => {
    router.push({
      path: `/detail/${record.name}`,
    });
  };
</script>
