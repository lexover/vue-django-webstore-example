import ApiService from '@/common/api.service';
import { URL_COUNTRIES } from '@/common/config.js';
import { FETCH_LIST, SET_LIST, GET_ITEMS_LIST } from '../types';

const state = () => ({
  countries: [],
});

const getters = {
  [GET_ITEMS_LIST]: (state) => state.countries,
};

const mutations = {
  [SET_LIST](state, payload) { state.countries = payload; },
};

const actions = {
  async [FETCH_LIST]({ commit }) {
    const { data } = await ApiService.get(URL_COUNTRIES);
    commit(SET_LIST, data.results);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
