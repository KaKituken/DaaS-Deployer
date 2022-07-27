<template>
    <div class="layout-demo">
        <a-layout style="min-height: 850px">
            <a-layout-header>
                <div>
                    <a-breadcrumb style="margin-left:15px;">
                        <a-breadcrumb-item>主页</a-breadcrumb-item>
                        <a-breadcrumb-item>模型</a-breadcrumb-item>
                        <a-breadcrumb-item>{{ modelName }}</a-breadcrumb-item>
                        <template #separator>
                            <icon-right />
                        </template>
                    </a-breadcrumb>
                    <div id="basicInfo">
                        <p style="font-size: 20px; font-weight:bold;">{{ modelName }}</p>
                        <p style="color: grey;">{{ modelDescription }}</p>
                    </div>    
                </div>
                <div id="detailInfo">
                    <a-space direction="vertical" size="medium" fill>
                        <a-descriptions :data="data" size="small" :align="{label:'right',value:'right'}" column="4" layout="inline-vertical"/>
                    </a-space>
                </div>
            </a-layout-header>
            <a-layout-content>
                <a-tabs default-active-key="1" style="width:100%;height:100%">
                    <a-tab-pane key="1" title="概述" id="overview">
                        <div id="var">
                            <div id="inputVar">
                                <p class="tag">输入变量</p>
                                <a-divider/>
                            </div>
                            <div id="targetVar">
                                <p class="tag">目标变量</p>
                                <a-divider />
                            </div>
                        </div>
                        <div id="result">
                            <p class="tag" id="resultTag">评估结果</p>
                            <a-divider />
                            <a-empty />
                        </div>
                    </a-tab-pane>
                    <a-tab-pane key="2" title="部署">
                        Content of Tab Panel 2
                    </a-tab-pane>
                    <a-tab-pane key="3" title="测试">
                        <a-button>新建</a-button>
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
            <a-layout-footer>
            </a-layout-footer>
        </a-layout>
    </div>
</template>

<script type="ts" setup>
    import { ref } from 'vue'

    const modelName = ref('xgb-iris')
    const modelDescription = ref('this is a simple introduction of the model...')
    const data = [{
            label: '修改时间',
            value: '2022-07-27 13:28',
        }, {
            label: '类型',
            value: 'PMML',
        }, {
            label: '算法',
            value: 'MiningModel(classfication)'
        }, {
            label: '引擎',
            value: 'PyPMML',
        }
    ];

</script>

<style scoped>
.layout-demo{
    min-width:860px;
}
.layout-demo :deep(.arco-layout-header),
.layout-demo :deep(.arco-layout-content),
.layout-demo :deep(.arco-layout-footer){
    display:flex;
    color: var(--color-black);
    font-size: 16px;
    font-stretch: condensed;
}

.layout-demo :deep(.arco-layout-header) {
    background-color:#fff;
    height:150px;
}

.layout-demo :deep(.arco-layout-content) {
    background-color:#F5F5F5;
}

.layout-demo :deep(.arco-layout-footer) {
    background-color:#F5F5F5;
    height:50px;
    margin-top:20px;
    margin-left:2%;
    margin-right:2%;
}

#basicInfo{
    width:350px;
    margin-left:20px;
}

#detailInfo{
    margin-top:50px;
    margin-right:50px;
    width:700px;
    justify-content: flex-end;
    margin-left: auto;
}

#overview{
    display:flex;
    flex-direction: column;
}

#var{
    display:flex;
}

#inputVar,#targetVar{
    width:47%;
    height:400px;
    background-color:#fff;
    margin-left:2%
}

.tag{
    margin-top:15px;
    margin-left:12px;
    font-size:18px;
    font-weight:bold;
}

#result{
    background-color:#fff;
    height:200px;
    margin-top:20px;
    margin-left:2%;
    margin-right:2%;
}

#resultTag{
    padding-top:15px;
}
</style>