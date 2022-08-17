import { DEFAULT_LAYOUT } from '@/router/constants';
import { AppRouteRecordRaw } from '../types';

const MODELOVERVIEW: AppRouteRecordRaw = {
  path: '/importModel',
  name: 'importModel',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.importModel',
    requiresAuth: false,
    icon: 'icon-dashboard',
    order: 1,
  },
  children: [
    {
      path: '/import/model',
      name: 'importModel',
      component: () => import('@/views/importModel/index.vue'),
      meta: {
        locale: 'menu.importModel',
        requiresAuth: false,
        roles: ['*'],
      },
    },
  ],
};

export default MODELOVERVIEW;
