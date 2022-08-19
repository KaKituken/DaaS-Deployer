import { DEFAULT_LAYOUT } from '@/router/constants';
import { AppRouteRecordRaw } from '../types';

const MODELOVERVIEW: AppRouteRecordRaw = {
  path: '/import',
  name: 'import',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.import',
    requiresAuth: false,
    icon: 'icon-dashboard',
    order: 1,
  },
  children: [
    {
      path: '/import/model',
      name: 'importModel',
      component: () => import('@/views/import/model/index.vue'),
      meta: {
        locale: 'menu.import.model',
        requiresAuth: false,
        roles: ['*'],
      },
    },
    {
      path: '/import/dataset',
      name: 'importDataset',
      component: () => import('@/views/import/dataset/index.vue'),
      meta: {
        locale: 'menu.import.dataset',
        requiresAuth: false,
        roles: ['*'],
      },
    },
  ],
};

export default MODELOVERVIEW;
