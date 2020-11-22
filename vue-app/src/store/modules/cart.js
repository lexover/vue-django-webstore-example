import ApiService from '@/common/api.service';
// import JwtService from '@/common/jwt.service'
import { URL_ORDERS } from '@/common/config.js'
import {
  ADD_ITEM, REMOVE_ITEM, CHANGE_ITEM, LOAD_DATA, SAVE_DATA, CLEAR_DATA, INITIALIZE,
  PUSH_ITEM, POP_ITEM, SET_ITEM_QUANTITY, SET_LIST, CHECKOUT,
  GET_ITEMS_COUNT, GET_ITEMS_LIST, GET_SUBTOTAL, GET_TOTAL, RESET_ERRORS, APPEND_ERROR
} from '../types';

const state = () => ({
  cart_items: [],
});

const getters = {
  [GET_ITEMS_COUNT]: (state) => state.cart_items.reduce((total, line) => total + line.quantity, 0),
  [GET_ITEMS_LIST]: (state) => state.cart_items,
  [GET_SUBTOTAL]: (state) => state.cart_items.reduce(
    (subtotal, line) => subtotal + (line.quantity * line.product.price), 0
  ),
  [GET_TOTAL]: (state) => state.cart_items.reduce(
    (total, line) => total + (line.quantity * line.product.sale_price), 0
  ),
};

const actions = {
  async [CHECKOUT](context, payload) {
    context.commit(RESET_ERRORS, '', { root: true });
    return new Promise((resolve, reject) => {
    ApiService.post(URL_ORDERS, payload, true)
        .then(( response ) => {
          resolve( response.data.id );
        })
        .catch(({ response }) => {
          const err = [response.data.detail, response.status];
          context.commit(APPEND_ERROR, err, { root: true });
          console.log(JSON.stringify(response));
          reject(response.data);
        });
     });
  },

  [ADD_ITEM]({ state, commit }, payload) {
    const line = state.cart_items.find((line) => line.product.id === payload.product.id);
    if (line != null) {
      payload.quantity = line.quantity + payload.quantity;
      commit(SET_ITEM_QUANTITY, payload);
    } else {
      commit(PUSH_ITEM, payload);
    }
  },

  [REMOVE_ITEM]({ state, commit }, lineToRemove) {
    const index = state.cart_items.findIndex((line) => line === lineToRemove);
    if (index > -1) {
      commit(POP_ITEM, index);
    }
  },

  [CHANGE_ITEM]({ commit }, payload) {
    commit(SET_ITEM_QUANTITY, payload);
  },

  [LOAD_DATA](context) {
    const data = localStorage.getItem('cart');
    if (data != null) {
      context.commit(SET_LIST, JSON.parse(data));
    }
  },

  [SAVE_DATA](context) {
    localStorage.setItem('cart', JSON.stringify(context.state.cart_items));
  },

  [CLEAR_DATA](context) {
    context.commit(SET_LIST, []);
  },

  [INITIALIZE](context, store) {
    context.dispatch(LOAD_DATA);
    store.watch((state) => state.cart.cart_items,
      () => context.dispatch(SAVE_DATA, { deep: true }));
  },

};

const mutations = {
  [PUSH_ITEM]: (state, item) => state.cart_items.push(item),
  [POP_ITEM]: (state, index) => state.cart_items.splice(index, 1),
  [SET_LIST](state, data) { state.cart_items = data; },
  [SET_ITEM_QUANTITY](state, payload) {
    const line = state.cart_items.find((line) => line.product.id === payload.product.id);
    line.quantity = payload.quantity;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
