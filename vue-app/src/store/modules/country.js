import { ApiService } from '@/common/api.service';
import { URL_COUNTRIES } from '@/common/config';
import { FETCH_ITEMS_LIST } from '../actions.types';
import { SET_ITEMS_LIST } from '../mutations.types';
import { GET_ITEMS_LIST } from '../getters.types';

const state = () => ({
  countries: [],
});

const getters = {
  [GET_ITEMS_LIST]: (state) => state.countries,
};

const mutations = {
  [SET_ITEMS_LIST](state, payload) { state.countries = payload; },
};

const actions = {
  async [FETCH_ITEMS_LIST]({ commit }) {
    const { data } = await ApiService.get(URL_COUNTRIES);
    commit(SET_ITEMS_LIST, data.results);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
