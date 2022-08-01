import { DEFAULT_LAYOUT } from '@/router/constants';
import { AppRouteRecordRaw } from '../types';

const MODELOVERVIEW: AppRouteRecordRaw = {
  path: '/deploy',
  name: 'deploy',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.deploy',
    requiresAuth: false,
    icon: 'icon-dashboard',
    order: 2,
  },
  children: [
    {
      path: '/deploy',
      name: 'deploy',
      component: () => import('@/views/deploy/index.vue'),
      meta: {
        locale: 'menu.deploy',
        requiresAuth: false,
        roles: ['*'],
      },
    },
  ],
};

export default MODELOVERVIEW;
