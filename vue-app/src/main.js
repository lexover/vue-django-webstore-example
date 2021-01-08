import Vue from 'vue';
import { BootstrapVue } from 'bootstrap-vue';
import { USER } from '@/store/namespaces.types';
import {
  CHECK_AUTH,
  RESET_ERRORS,
  CHANGE_PATH,
} from '@/store/actions.types';
import App from './App.vue';
import router from './router';
import store from './store';

import ErrorFilter from './common/error.filter';
import CurrencyFilter from './common/currency.filter';
import DateTimeFilter from './common/dateTime.filter';
import StatusFilter from './common/status.filter';

import './assets/scss/app.scss';

Vue.config.productionTip = false;
Vue.use(BootstrapVue);

Vue.filter('dateTime', DateTimeFilter);
Vue.filter('status', StatusFilter);
Vue.filter('error', ErrorFilter);
Vue.filter('currency', CurrencyFilter);

router.beforeEach((to, from, next) => Promise.all([
  store.dispatch(`${RESET_ERRORS}`),
  store.dispatch(`${USER}${CHECK_AUTH}`),
]).then(next));

router.afterEach((to) => {
  store.dispatch(`${CHANGE_PATH}`, to);
});

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
