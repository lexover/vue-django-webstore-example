import axios from 'axios';
import JwtService from '@/common/jwt.service';
import { API_URL } from '@/common/config';

const axios_instance = function (auth=false) {
  const instance = axios.create(); 
  instance.defaults.headers.common['Accept'] = 'application/json';
  if (auth) {
    let token = JwtService.getToken();
    if ( token && token.access != undefined) {
      instance.defaults.headers.common['Authorization'] =  `Bearer ${token.access}`;
    }
  }
  return instance;
}

export const ApiService = {

  query(resource, parameters, auth=false) {
    return axios_instance(auth).get(`${API_URL}/${resource}/`, { params: parameters }).catch((error) => {
      throw new Error(`[RWV] ApiService ${error}`);
    });
  },

  get(resource, slug = '', auth=false) {
    return axios_instance(auth).get(`${API_URL}/${resource}/${slug}/`).catch((error) => {
      throw new Error(`[RWV] ApiService ${error}`);
    });
  },

  post(resource, params, auth=false) {
    return axios_instance(auth).post(`${API_URL}/${resource}/`, params);
  },

  update(resource, slug, params, auth=false) {
    return axios_instance(auth).put(`${API_URL}/${resource}/${slug}/`, params);
  },

  put(resource, params, auth=false) {
    return axios_instance(auth).put(`${API_URL}/${resource}/`, params);
  },

  delete(resource, auth=false) {
    return axios_instance(auth).delete(resource).catch((error) => {
      throw new Error(`[RWV] ApiService ${error}`);
    });
  },
};

export default ApiService;
