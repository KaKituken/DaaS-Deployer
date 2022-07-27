import Mock from 'mockjs';
import setupMock, { successResponseWrap } from '@/utils/setup-mock';

setupMock({
  setup() {
    Mock.mock(new RegExp('/api/modelOverview/info'), () => {
      return successResponseWrap({
        modelName: 'Xgb-iris',
        modelDescription: 'this introduction is from mock',
        updateTime: '2022-07-27 23:16',
        type: 'PMML',
        algorithm: 'MiningModel(classfication)',
        engine: 'PyPMML',
      });
    });

    Mock.mock(new RegExp('/api/modelOverview/var'), () => {
      const inputData = [
        {
          key: '1',
          field: 'sepal length(cm)',
          type: 'double',
          measure: 'continuous',
          value: '',
        },
        {
          key: '2',
          field: 'sepal width(cm)',
          type: 'double',
          measure: 'continuous',
          value: '',
        },
        {
          key: '3',
          field: 'petal length(cm)',
          type: 'double',
          measure: 'continuous',
          value: '',
        },
        {
          key: '4',
          field: 'petal width(cm)',
          type: 'double',
          measure: 'continuous',
          value: '',
        },
      ];
      const targetData = [
        {
          key: '1',
          field: 'Species',
          type: 'integer',
          measure: 'norminal',
          value: '0,1,2',
        },
      ];
      return successResponseWrap({
        inputData,
        targetData,
      });
    });
  },
});
