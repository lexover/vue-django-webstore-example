import { ApiService } from '@/common/api.service';
import { URL_ORDERS } from '@/common/config';
import {
  ADD_ITEM,
  REMOVE_ITEM,
  CHANGE_ITEM,
  LOAD_DATA,
  SAVE_DATA,
  CLEAR_DATA,
  INITIALIZE,
  CHECKOUT,
  RESET_ERRORS,
} from '../actions.types';
import {
  SET_ITEM_QUANTITY,
  SET_ITEMS_LIST,
  ADD_ERROR,
} from '../mutations.types';
import {
  GET_ITEMS_COUNT,
  GET_ITEMS_LIST,
  GET_SUBTOTAL,
  GET_TOTAL,
} from '../getters.types';

const state = () => ({
  cart_items_list: [],
});

const getters = {
  [GET_ITEMS_LIST]: (state) => state.cart_items_list,
  [GET_ITEMS_COUNT]: (state) => state.cart_items_list.reduce((total, line) => total + line.quantity, 0),
  [GET_SUBTOTAL]: (state) => state.cart_items_list.reduce(
    (subtotal, line) => subtotal + (line.quantity * line.product.price), 0,
  ),
  [GET_TOTAL]: (state) => state.cart_items_list.reduce(
    (total, line) => total + (line.quantity * line.product.sale_price), 0,
  ),
};

const actions = {
  async [CHECKOUT]({ commit }, payload) {
    commit(RESET_ERRORS, '', { root: true });
    return new Promise((resolve, reject) => {
      ApiService.post(URL_ORDERS, payload, true)
        .then((response) => {
          resolve(response.data.id);
        })
        .catch(({ response }) => {
          const err = [response.data.detail, response.status];
          commit(ADD_ERROR, err, { root: true });
          reject(response.data);
        });
    });
  },

  [ADD_ITEM]({ state, commit }, payload) {
    const line = state.cart_items_list.find((item) => item.product.id === payload.product.id);
    if (line != null) {
      const quantity = line.quantity + payload.quantity;
      commit(SET_ITEM_QUANTITY, { ...payload, quantity });
    } else {
      commit(ADD_ITEM, payload);
    }
  },

  [REMOVE_ITEM]({ state, commit }, lineToRemove) {
    const index = state.cart_items_list.findIndex((line) => line === lineToRemove);
    if (index > -1) {
      commit(REMOVE_ITEM, index);
    }
  },

  [CHANGE_ITEM]({ commit }, payload) {
    commit(SET_ITEM_QUANTITY, payload);
  },

  [LOAD_DATA]({ commit }) {
    const data = localStorage.getItem('cart');
    if (data != null) {
      commit(SET_ITEMS_LIST, JSON.parse(data));
    }
  },

  [SAVE_DATA]({ state }) {
    localStorage.setItem('cart', JSON.stringify(state.cart_items_list));
  },

  [CLEAR_DATA]({ commit }) {
    commit(SET_ITEMS_LIST, []);
  },

  [INITIALIZE]({ dispatch }, store) {
    dispatch(LOAD_DATA);
    store.watch((state) => state.CART.cart_items_list,
      () => dispatch(SAVE_DATA, { deep: true }));
  },
};

const mutations = {
  [ADD_ITEM]: (state, item) => state.cart_items_list.push(item),
  [REMOVE_ITEM]: (state, index) => state.cart_items_list.splice(index, 1),
  [SET_ITEMS_LIST](state, data) { state.cart_items_list = data; },
  [SET_ITEM_QUANTITY](state, payload) {
    const line = state.cart_items_list.find((row) => row.product.id === payload.product.id);
    if (line) {
      line.quantity = payload.quantity;
    }
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
