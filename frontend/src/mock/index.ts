import Mock from 'mockjs';

import './user';
import './message-box';
import './modelOverview';

import '@/views/dashboard/workplace/mock';

Mock.setup({
  timeout: '600-1000',
});
