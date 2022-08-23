import { DEFAULT_LAYOUT } from '@/router/constants';
import { AppRouteRecordRaw } from '../types';

const MODELOVERVIEW: AppRouteRecordRaw = {
  path: '/modelDeploy',
  name: 'modelDeploy',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.modelDeploy',
    requiresAuth: false,
    icon: 'icon-dashboard',
    order: 0,
  },
  children: [
    {
      path: '/addService/:modelname',
      name: 'addService',
      component: () => import('@/views/addService/index.vue'),
      meta: {
        locale: 'menu.modelDeploy.addService',
        requiresAuth: false,
        roles: ['*'],
      },
    },
  ],
};

export default MODELOVERVIEW;
