import { DEFAULT_LAYOUT } from '@/router/constants';
import { AppRouteRecordRaw } from '../types';

const MODELOVERVIEW: AppRouteRecordRaw = {
  path: '/modelList',
  name: 'modelList',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.modelList',
    requiresAuth: false,
    icon: 'icon-dashboard',
    order: 3,
  },
  children: [
    {
      path: '/list',
      name: 'list',
      component: () => import('@/views/modelList/index.vue'),
      meta: {
        locale: 'menu.modelList',
        requiresAuth: false,
        roles: ['*'],
      },
    },
  ],
};

export default MODELOVERVIEW;
