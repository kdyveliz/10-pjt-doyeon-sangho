import { createRouter, createWebHistory } from 'vue-router';
import ExchangeCalculator from '@/components/ExchangeCalculator.vue';

const routes = [
  { path: '/', component: ExchangeCalculator },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
