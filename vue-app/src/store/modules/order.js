import { ApiService } from '@/common/api.service';
import { URL_ORDERS } from '@/common/config';
import { FETCH_ITEMS_LIST } from '../actions.types';
import { SET_ITEMS_LIST, SET_LOADING, ADD_ERROR } from '../mutations.types';
import { GET_ITEMS_COUNT, GET_ITEMS_LIST, GET_TOTAL } from '../getters.types';

const state = () => ({
  orders: [],
  loading: false,
});

const getters = {
  [GET_ITEMS_COUNT]: (state) => state.orders.reduce((total, line) => total + line.quantity, 0),
  [GET_ITEMS_LIST]: (state) => state.orders,
  [GET_TOTAL]: (state) => state.orders.reduce(
    (total, line) => total + (line.order_items.quantity * line.order_items.price), 0,
  ),
};

const actions = {
  async [FETCH_ITEMS_LIST]({ commit }) {
    commit(SET_LOADING, true);
    try {
      const { data } = await ApiService.get(URL_ORDERS, '', true);
      commit(SET_ITEMS_LIST, data.results);
      commit(SET_LOADING, false);
    } catch (error) {
      commit(ADD_ERROR, error, { root: true });
    }
  },

};

const mutations = {
  [SET_ITEMS_LIST](state, data) { state.orders = data; },
  [SET_LOADING](state, payload) { state.loading = payload; },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
