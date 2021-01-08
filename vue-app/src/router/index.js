import Vue from 'vue';
import VueRouter from 'vue-router';

import TheMainView from '@/views/TheMainView.vue';
import TheProductsListView from '@/views/TheProductsListView.vue';
import TheProductView from '@/views/TheProductView.vue';
import TheShopView from '@/views/TheShopView.vue';
import TheCartView from '@/views/TheCartView.vue';
import TheCheckoutView from '@/views/TheCheckoutView.vue';
import TheHomeView from '@/views/TheHomeView.vue';
import TheLoginView from '@/views/TheLoginView.vue';
import TheRegisterView from '@/views/TheRegisterView.vue';
import TheProfileView from '@/views/TheProfileView.vue';
import TheAboutView from '@/views/TheAboutView.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    component: TheMainView,
    children: [{
      name: 'home',
      path: '/',
      component: TheHomeView,
    },
    {
      path: 'catalog',
      component: TheShopView,
      children: [{
        path: '/',
        name: 'catalog',
        component: TheProductsListView,
        props: true,
      },
      {
        path: 'product/:id',
        name: 'product',
        component: TheProductView,
        props(route) {
          const props = { ...route.params };
          props.id = +props.id;
          return props;
        },
      },
      ],
    },
    {
      path: 'cart',
      name: 'cart',
      component: TheCartView,
    },
    {
      path: 'checkout',
      name: 'checkout',
      component: TheCheckoutView,
    },
    {
      path: 'login',
      name: 'login',
      component: TheLoginView,
    },
    {
      path: 'register',
      name: 'register',
      component: TheRegisterView,
    },
    {
      path: 'profile',
      name: 'profile',
      component: TheProfileView,
    },
    {
      path: 'about',
      name: 'about',
      component: TheAboutView,
    },
    ],
  },
  {
    path: '*', redirect: '/',
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
