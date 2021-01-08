import { ApiService } from '@/common/api.service';
import { URL_REVIEWS } from '@/common/config';

import {
  FETCH_ITEMS_LIST,
  FETCH_ITEM,
  CREATE_ITEM,
  CHANGE_ITEM,
} from '../actions.types';
import {
  SET_ITEMS_LIST,
  SET_ITEM,
  SET_LOADING,
  ADD_ITEM,
  ADD_ERROR,
} from '../mutations.types';
import {
  GET_ITEMS_LIST,
  GET_ITEM,
} from '../getters.types';

const state = () => ({
  reviews: [],
  review: {},
  loading: false,
});

const getters = {
  [GET_ITEMS_LIST]: (state) => state.reviews,
  [GET_ITEM]: (state) => state.review,
};

const actions = {
  async [FETCH_ITEMS_LIST]({ commit }, payload) {
    commit(SET_LOADING, true);
    try {
      const { data } = await ApiService.query(URL_REVIEWS, payload);
      commit(SET_ITEMS_LIST, data.results);
      commit(SET_LOADING, false);
    } catch (error) {
      commit(ADD_ERROR, error, { root: true });
    }
  },
  async [FETCH_ITEM]({ commit }, payload) {
    const { data } = await ApiService.query(URL_REVIEWS, payload);
    if (data.results) {
      commit(SET_ITEM, data.results[0]);
    }
  },

  async [CREATE_ITEM]({ commit }, payload) {
    ApiService.post(URL_REVIEWS, payload, true)
      .then((data) => {
        commit(SET_ITEM, data.data);
        commit(ADD_ITEM, data.data);
      })
      .catch((error) => { console.log(error); });
  },

  async [CHANGE_ITEM]({ commit }, payload) {
    ApiService.put(URL_REVIEWS, payload, true)
      .then((data) => {
        commit(SET_ITEM, data.data);
        commit(CHANGE_ITEM, data.data);
      });
  },
};

const mutations = {
  [SET_ITEMS_LIST](state, payload) { state.reviews = payload; },
  [SET_ITEM](state, payload) { state.review = payload; },
  [SET_LOADING](state, payload) { state.loading = payload; },
  [ADD_ITEM](state, payload) { state.reviews.push(payload); },
  [CHANGE_ITEM](state, payload) {
    const pos = state.reviews.findIndex((element) => element.id === payload.id);
    state.reviews[pos] = payload;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
