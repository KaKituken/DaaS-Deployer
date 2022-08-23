import { DEFAULT_LAYOUT } from '@/router/constants';
import { AppRouteRecordRaw } from '../types';

const MODELOVERVIEW: AppRouteRecordRaw = {
  path: '/modelPredict',
  name: 'modelPredict',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.modelPredict',
    requiresAuth: false,
    icon: 'icon-dashboard',
    order: 0,
  },
  children: [
    {
      path: '/batchPredictSettings/:modelname',
      name: 'batchPredictSettings',
      component: () => import('@/views/batchPredictSettings/index.vue'),
      meta: {
        locale: 'menu.modelPredict.batchPredictSettings',
        requiresAuth: false,
        roles: ['*'],
      },
    },
  ],
};

export default MODELOVERVIEW;
