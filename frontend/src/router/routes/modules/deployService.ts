import { DEFAULT_LAYOUT } from '@/router/constants';
import { AppRouteRecordRaw } from '../types';

const MODELOVERVIEW: AppRouteRecordRaw = {
  path: '/deployService',
  name: 'deployService',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.deployService',
    requiresAuth: false,
    icon: 'icon-dashboard',
    order: 2,
  },
  children: [
    {
      path: '/deployService/:serviceName',
      name: 'deployServce',
      component: () => import('@/views/deployService/index.vue'),
      meta: {
        locale: 'menu.deployService',
        requiresAuth: false,
        roles: ['*'],
      },
    },
  ],
};

export default MODELOVERVIEW;
