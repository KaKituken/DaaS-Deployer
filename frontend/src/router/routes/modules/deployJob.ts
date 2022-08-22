import { DEFAULT_LAYOUT } from '@/router/constants';
import { AppRouteRecordRaw } from '../types';

const MODELOVERVIEW: AppRouteRecordRaw = {
  path: '/deployJob',
  name: 'deployJob',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.deployJob',
    requiresAuth: false,
    icon: 'icon-dashboard',
    order: 3,
  },
  children: [
    {
      path: '/deployJob/:modelName/:jobName',
      name: 'deployJob',
      component: () => import('@/views/deployJob/index.vue'),
      meta: {
        locale: 'menu.deployJob',
        requiresAuth: false,
        roles: ['*'],
      },
    },
    {
      path: '/deployJob/:modelName/:jobName/:type',
      name: 'deployJobName',
      component: () => import('@/views/deployJob/index.vue'),
      meta: {
        locale: 'menu.deployJob',
        requiresAuth: false,
        roles: ['*'],
      },
    },
  ],
};

export default MODELOVERVIEW;
