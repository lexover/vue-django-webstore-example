import ApiService from '@/common/api.service';
import JwtService from '@/common/jwt.service';
import { URL_TOKEN_REFRESH, URL_USERS, URL_OBTAIN_TOKEN, URL_CHECK_USERNAME } from '@/common/config.js'
import {
  REGISTER, SET_AUTH, GET_ITEM,
  IS_AUTH, APPEND_ERROR, PURGE_AUTH, LOGIN, LOGOUT, CHECK_AUTH, RESET_ERRORS,
  IS_UNIQUE, CHECK_UNIQUE, SET_UNIQUE, FETCH_ITEM, SET_ITEM
} from '../types';

const state = () => ({
  user: {},
  isAuthenticated: false,
  isUnique: null,
});

const getters = {
  [GET_ITEM]: (state) => state.user,
  [IS_AUTH]: (state) => state.isAuthenticated,
  [IS_UNIQUE]: (state) => state.isUnique,
};

const actions = {

  [LOGIN](context, credentials) {
    context.commit(RESET_ERRORS, '', {root: true});
    return new Promise((resolve, reject) => {
      ApiService.post(URL_OBTAIN_TOKEN, credentials)
        .then(({ data }) => {
          context.commit(SET_AUTH, {username: credentials.username, access: data.access, refresh: data.refresh});
          resolve(credentials.username);
        })
        .catch(({ response }) => {
          const err = [response.data.detail, response.status];
          context.commit(APPEND_ERROR, err, { root: true });
          reject(response)
        });
    });
  },
 
  [REGISTER](context, credentials) {
    context.commit(RESET_ERRORS, '', { root: true });
    return new Promise((resolve, reject) => {
      ApiService.post('users', credentials)
        .then(() => {
          context.dispatch(LOGIN, credentials);
          resolve(credentials.username);
        })
        .catch(({ response }) => {
          context.commit(APPEND_ERROR, response.data.detail, { root: true });
          reject(response);
        });
    });
  },


  [FETCH_ITEM](context) {
    context.commit(RESET_ERRORS, '', {root: true});
    let token = JwtService.getToken();
    return new Promise((resolve) => {
      ApiService.get(URL_USERS, token.username, true)
      .then(({ data }) => {
        context.commit(SET_ITEM, data);
        resolve(data); })
      .catch(({ response }) => {
          const err = [response.data.detail, response.status];
          context.commit(APPEND_ERROR, err, { root: true });
      });
    });
  },

  [LOGOUT](context) {
    context.commit(PURGE_AUTH);
  },

  [CHECK_AUTH](context) {
    let jwt_data = JwtService.getToken() 
    if (jwt_data && jwt_data.refresh !== undefined) {
      ApiService.post(URL_TOKEN_REFRESH, { refresh: jwt_data.refresh })
      .then((data) => { 
         context.commit(SET_AUTH, { username: jwt_data.username, access: data.data.access,  refresh: jwt_data.refresh });
      })
      .catch((error) => { 
        if (error.response.status === 401) {
          context.commit(PURGE_AUTH);
        } 
      })
    } else {
      context.commit(PURGE_AUTH);
    }
  },

  async [CHECK_UNIQUE]({ commit }, payload) {
    if (payload.length < 1) {
      commit(SET_UNIQUE, null);
    } else if (payload.length < 3) {
      commit(SET_UNIQUE, false);
    } else {
      const result = await ApiService.query(URL_CHECK_USERNAME, {username: payload});
      commit(SET_UNIQUE, result.data)
    }
  }
};

const mutations = {
  [SET_AUTH](state, auth) {
    state.isAuthenticated = true;
    state.user.username = auth.username;
    state.errors = {};
    JwtService.saveToken(auth);
  },

  [PURGE_AUTH](state) {
    state.isAuthenticated = false;
    state.user = {};
    state.errors = {};
    JwtService.destroyToken();
  },

  [SET_ITEM](state, user) { state.user = user; },
  [SET_UNIQUE](state, value) { state.isUnique = value; },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
