import Vue from 'vue';
import {
  LayoutPlugin, 
  NavbarPlugin, 
  BreadcrumbPlugin,
  ButtonPlugin, 
  ImagePlugin,
  FormPlugin,
  FormInputPlugin,
  FormSelectPlugin,
  InputGroupPlugin,
  ListGroupPlugin,
  TableSimplePlugin,
  FormCheckboxPlugin,
  ModalPlugin,
  FormGroupPlugin
} from 'bootstrap-vue';

import App from './App.vue';
import router from './router';
import store from './store';

import { USER, CHECK_AUTH, RESET_ERRORS, SET_PATH } from './store/types';
import ErrorFilter from './common/error.filter';
import CurrencyFilter from './common/currency.filter';
import DateTimeFilter from './common/dateTime.filter';
import StatusFilter from './common/status.filter';

import './assets/scss/app.scss';

Vue.config.productionTip = false;
Vue.use(NavbarPlugin);
Vue.use(LayoutPlugin);
Vue.use(ButtonPlugin);
Vue.use(ImagePlugin);
Vue.use(BreadcrumbPlugin);
Vue.use(FormPlugin);
Vue.use(FormGroupPlugin);
Vue.use(FormInputPlugin);
Vue.use(FormSelectPlugin);
Vue.use(InputGroupPlugin);
Vue.use(ListGroupPlugin);
Vue.use(TableSimplePlugin);
Vue.use(FormCheckboxPlugin);
Vue.use(ModalPlugin);

Vue.filter('dateTime', DateTimeFilter);
Vue.filter('status', StatusFilter);
Vue.filter('error', ErrorFilter);
Vue.filter('currency', CurrencyFilter);

router.beforeEach((to, from, next) => Promise.all([
  store.dispatch(`${RESET_ERRORS}`),
  store.dispatch(`${USER}${CHECK_AUTH}`),
]).then(next)); 

router.afterEach((to) => {
  store.dispatch(`${SET_PATH}`, to);
});

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
