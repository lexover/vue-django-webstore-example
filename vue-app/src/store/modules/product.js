import  ApiService from '@/common/api.service';
import  { URL_PRODUCTS, URL_PRODUCTS_NAMES } from '@/common/config.js';
import {
  FETCH_ITEM, FETCH_LIST, FETCH_NAMES, RESET_FILTER,
  SET_ITEM, SET_LIST, SET_ITEM_COUNT_ON_PAGE, SET_LOADING, SET_PRICES_RANGE,
  SET_LAST_PARAMS, SET_NAMES_LIST, GET_ITEMS_LIST, GET_ITEM, GET_LOADING, GET_ITEMS_COUNT,
  GET_NAMES_LIST, GET_PRICES_RANGE, APPEND_ERROR
} from '../types';

const state = () => ({
  products: [],
  product: {},
  products_names: [],
  products_number: 0,
  loading: false,
  last_params: {},
  prices: { min: 0, max: 100 },
});

const getters = {
  [GET_ITEMS_LIST]: (state) => state.products,
  [GET_ITEM]: (state) => state.product,
  [GET_LOADING]: (state) => state.loading,
  [GET_ITEMS_COUNT]: (state) => state.products_number,
  [GET_NAMES_LIST]: (state) => state.products_names,
  [GET_PRICES_RANGE]: (state) => state.prices,
};

const actions = {
  async [FETCH_LIST]({ commit, state }, payload) {
    commit(SET_LOADING, true);
    const lastVal = state.last_params;
    const parameters = { ...lastVal, ...payload };
    try{
      console.log("Parameters: " + parameters);
      const { data } = await ApiService.query(URL_PRODUCTS, parameters);
      commit(SET_LIST, data);
      commit(SET_LAST_PARAMS, parameters);
      commit(SET_LOADING, false);
    } catch(error) {
      commit(APPEND_ERROR, error, { root: true });
    }
  },

  async [FETCH_ITEM]({ commit }, id) {
    commit(SET_LOADING, true);
    try {
      const { data } = await ApiService.get(URL_PRODUCTS, id);
      commit(SET_ITEM, data);
      commit(SET_LOADING, false);
    } catch(error) {
      commit(APPEND_ERROR, error, { root: true });
    }
  },

  async [FETCH_NAMES]({ commit }, payload) {
    const { data } = await ApiService.query(URL_PRODUCTS_NAMES, payload);
    commit(SET_NAMES_LIST, data);
  },

  [RESET_FILTER]({ commit }) {
    commit(SET_LAST_PARAMS, {});
    commit(SET_PRICES_RANGE, { min: 0, max: 0 });
  },
};

const mutations = {
  [SET_LIST](state, payload) {
    state.products = payload.results;
    state.products_number = payload.count;
    // Only firs time we have initialyse prices_range
    if (state.prices.max === 0) {
      let minVal = Math.ceil(payload.min_price) - 1;
      if (minVal < 0) { minVal = 0; }
      const maxVal = Math.ceil(payload.max_price);
      state.prices = { min: minVal, max: maxVal };
    }
  },

  [SET_LAST_PARAMS](state, payload) {
    delete payload.offset;
    state.last_params = payload;
  },

  [SET_ITEM](state, payload) { state.product = payload; },
  [SET_ITEM_COUNT_ON_PAGE](state, payload) { state.products_on_page = payload; },
  [SET_LOADING](state, payload) { state.loading = payload; },
  [SET_PRICES_RANGE](state, payload) { state.prices = payload; },
  [SET_NAMES_LIST](state, payload) { state.products_names = payload; },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
