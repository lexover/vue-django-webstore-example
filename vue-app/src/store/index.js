import Vue from 'vue';
import Vuex, { createLogger } from 'vuex';

import { 
  GET_CURRENCY, GET_ERRORS, APPEND_ERROR, RESET_ERRORS,
  SET_PATH, GET_PATH,
 } from '@/store/types';

import productGroup from './modules/product_group';
import product from './modules/product';
import cart from './modules/cart';
import user from './modules/user';
import country from './modules/country';
import order from './modules/order';

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production';

export default new Vuex.Store({

  modules: {
    product,
    productGroup,
    cart,
    user,
    country,
    order,
  },

  state: () => ({

    currency: 'USD',
    errors: [],
    path: [],

  }),

  getters: {
    
    [GET_CURRENCY]: (state) => state.currency,

    [GET_ERRORS]: (state) => state.errors,

    [GET_PATH]: (state) => state.path,

  },

  actions: {

    [RESET_ERRORS]({ commit }) {
      commit(RESET_ERRORS);
    },

    [SET_PATH]({ commit }, payload) {
      let result = [{text: 'home', to: { name: 'home' }}];
      for (let element of payload.fullPath.split('/')) {
        if (element) {
          result.push({text: element, to: {name: element}});
          if (element === 'product') {
            break;
          }
        }
      }
      commit(SET_PATH, result);
    },

  },

  mutations: {

    [APPEND_ERROR](state, payload) { state.errors.push(payload); },
    
    [SET_PATH](state, payload) { state.path = payload },

    [RESET_ERRORS](state) { state.errors = []; },

  },

  strict: debug,

  plugins: debug ? [createLogger()] : [],

});
