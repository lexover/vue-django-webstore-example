import Vue from 'vue';
import VueRouter from 'vue-router';

import iMain from '@/views/Main';
import ProductsList from '@/views/ProductsList';
import ProductInfo from '@/views/ProductInfo';
import Shop from '@/views/Shop';
import Cart from '@/views/Cart';
import Checkout from '@/views/Checkout';
import Home from '@/views/Home';
import Login from '@/views/Login';
import Register from '@/views/Register';
import Profile from '@/views/Profile';
import About from '@/views/About';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    component: iMain,
    children: [{
      name: 'home',
      path: '/',
      component: Home,
    },
    {
      path: 'catalog',
      component: Shop,
      children: [{
        path: '/',
        name: 'catalog',
        component: ProductsList,
        props: true,
      },
      {
        path: 'product/:id',
        name: 'product',
        component: ProductInfo,
        props: true,
      },
      ],
    },
    {
      path: 'cart',
      name: 'cart',
      component: Cart,
    },
    {
      path: 'checkout',
      name: 'checkout',
      component: Checkout,
    },
    {
      path: 'login',
      name: 'login',
      component: Login,
    },
    {
      path: 'register',
      name: 'register',
      component: Register,
    },
    {
      path: 'profile',
      name: 'profile',
      component: Profile,
    },
    {
      path: 'about',
      name: 'about',
      component: About,
    }
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
