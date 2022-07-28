import Mock from 'mockjs';

import './user';
import './message-box';
import './modelOverview';
import './modelDeploy';

import '@/views/dashboard/workplace/mock';

Mock.setup({
  timeout: '600-1000',
});
