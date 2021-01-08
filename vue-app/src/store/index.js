import Vue from 'vue';
import Vuex, { createLogger } from 'vuex';

import { GET_CURRENCY, GET_ERRORS, GET_PATH } from '@/store/getters.types';
import { RESET_ERRORS, CHANGE_PATH } from '@/store/actions.types';
import { SET_PATH, ADD_ERROR } from '@/store/mutations.types';

import CATEGORY from './modules/category';
import PRODUCT from './modules/product';
import CART from './modules/cart';
import USER from './modules/user';
import COUNTRY from './modules/country';
import ORDER from './modules/order';
import REVIEW from './modules/review';

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production';

export default new Vuex.Store({

  modules: {
    PRODUCT,
    CATEGORY,
    CART,
    USER,
    COUNTRY,
    ORDER,
    REVIEW,
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

    [CHANGE_PATH]({ commit }, payload) {
      const result = [{ text: 'home', to: { name: 'home' } }];
      const elements = payload.fullPath.split('/');
      elements.forEach((element) => {
        if (element) {
          result.push({ text: element, to: { name: element } });
        }
      });
      commit(SET_PATH, result);
    },

  },

  mutations: {
    [ADD_ERROR](state, payload) { state.errors.push(payload); },
    [SET_PATH](state, payload) { state.path = payload; },
    [RESET_ERRORS](state) { state.errors = []; },
  },

  strict: debug,
  plugins: debug ? [createLogger()] : [],

});
