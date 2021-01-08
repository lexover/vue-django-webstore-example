import { ApiService } from '@/common/api.service';
import { JwtService } from '@/common/jwt.service';
import {
  URL_TOKEN_REFRESH,
  URL_USERS,
  URL_OBTAIN_TOKEN,
  URL_CHECK_USERNAME,
} from '@/common/config';
import {
  REGISTER,
  LOGIN,
  LOGOUT,
  CHECK_AUTH,
  RESET_ERRORS,
  CHECK_UNIQUE,
  FETCH_ITEM,
} from '@/store/actions.types';
import {
  SET_UNIQUE,
  SET_AUTH,
  SET_ITEM,
  REMOVE_AUTH,
  ADD_ERROR,
} from '@/store/mutations.types';
import {
  GET_ITEM,
  IS_AUTH,
  IS_UNIQUE,
} from '@/store/getters.types';

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
    context.commit(RESET_ERRORS, '', { root: true });
    return new Promise((resolve, reject) => {
      ApiService.post(URL_OBTAIN_TOKEN, credentials)
        .then(({ data }) => {
          context.commit(SET_AUTH, { username: credentials.username, access: data.access, refresh: data.refresh });
          resolve(credentials.username);
        })
        .catch(({ response }) => {
          const err = [response.data.detail, response.status];
          context.commit(ADD_ERROR, err, { root: true });
          reject(response);
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
          context.commit(ADD_ERROR, response.data.detail, { root: true });
          reject(response);
        });
    });
  },

  [FETCH_ITEM](context) {
    context.commit(RESET_ERRORS, '', { root: true });
    const token = JwtService.getToken();
    return new Promise((resolve) => {
      ApiService.get(URL_USERS, token.username, true)
        .then(({ data }) => {
          context.commit(SET_ITEM, data);
          resolve(data);
        })
        .catch(({ response }) => {
          const err = [response.data.detail, response.status];
          context.commit(ADD_ERROR, err, { root: true });
        });
    });
  },

  [LOGOUT](context) {
    context.commit(REMOVE_AUTH);
  },

  [CHECK_AUTH](context) {
    const jwtData = JwtService.getToken();
    if (jwtData && jwtData.refresh !== undefined) {
      ApiService.post(URL_TOKEN_REFRESH, { refresh: jwtData.refresh })
        .then((data) => {
          context.commit(SET_AUTH, { username: jwtData.username, access: data.data.access, refresh: jwtData.refresh });
        })
        .catch((error) => {
          if (error.response.status === 401) {
            context.commit(REMOVE_AUTH);
          }
        });
    } else {
      context.commit(REMOVE_AUTH);
    }
  },

  async [CHECK_UNIQUE]({ commit }, payload) {
    if (payload.length < 1) {
      commit(SET_UNIQUE, null);
    } else if (payload.length < 3) {
      commit(SET_UNIQUE, false);
    } else {
      const result = await ApiService.query(URL_CHECK_USERNAME, { username: payload });
      commit(SET_UNIQUE, result.data);
    }
  },
};

const mutations = {
  [SET_ITEM](state, user) { state.user = user; },
  [SET_UNIQUE](state, value) { state.isUnique = value; },
  [SET_AUTH](state, auth) {
    state.isAuthenticated = true;
    const jwtData = JwtService.parseJwt(auth.access);
    state.user.username = auth.username;
    state.user.id = jwtData.user_id;
    state.errors = {};
    JwtService.saveToken(auth);
  },
  [REMOVE_AUTH](state) {
    state.isAuthenticated = false;
    state.user = {};
    state.errors = {};
    JwtService.destroyToken();
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
