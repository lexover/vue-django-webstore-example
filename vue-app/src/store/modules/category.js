import { ApiService } from '@/common/api.service';
import { URL_CATEGORIES } from '@/common/config';
import { FETCH_ITEMS_LIST } from '../actions.types';
import { SET_ITEMS_LIST } from '../mutations.types';
import { GET_ITEMS_LIST } from '../getters.types';

const state = () => ({
  productGroups: [],
});

const getters = {
  [GET_ITEMS_LIST]: (state) => state.productGroups,
};

const actions = {
  async [FETCH_ITEMS_LIST](context) {
    console.log(`Get: ${URL_CATEGORIES}`);
    const { data } = await ApiService.get(URL_CATEGORIES);
    const result = ['All'].concat(data.results);
    context.commit(SET_ITEMS_LIST, result);
    return data;
  },
};

const mutations = {
  [SET_ITEMS_LIST](state, productGroups) {
    state.productGroups = productGroups;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
