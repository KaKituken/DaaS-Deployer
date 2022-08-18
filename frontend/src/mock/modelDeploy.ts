import Mock from 'mockjs';
import setupMock, { successResponseWrap } from '@/utils/setup-mock';

setupMock({
  setup() {
    Mock.mock(new RegExp('/api/modelDeploy/info'), () => {
      const version = [1, 2];
      const webEnvironment = ['Python 3.7 - Function as a Service'];
      return successResponseWrap({
        serverURL: 'https://192.168.64.3:30931/api/svc/pmml/xgb-iris-svc',
        modelVersion: version,
        environment: webEnvironment,
      });
    });
  },
});
