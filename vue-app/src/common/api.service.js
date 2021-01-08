import axios from 'axios';
import { JwtService } from '@/common/jwt.service';
import { API_URL } from '@/common/config';

function axiosInstance(auth = false) {
  const instance = axios.create();
  instance.defaults.headers.common.Accept = 'application/json';
  if (auth) {
    const token = JwtService.getToken();
    if (token && token.access !== undefined) {
      instance.defaults.headers.common.Authorization = `Bearer ${token.access}`;
    }
  }
  return instance;
}

export const ApiService = {

  async query(resource, parameters, auth = false) {
    try {
      return axiosInstance(auth).get(`${API_URL}/${resource}/`, { params: parameters });
    } catch (error) {
      throw new Error(`[RWV] ApiService ${error}`);
    }
  },

  async get(resource, slug = '', auth = false) {
    try {
      return axiosInstance(auth).get(`${API_URL}/${resource}/${slug}/`);
    } catch (error) {
      throw new Error(`[RWV] ApiService ${error}`);
    }
  },

  async post(resource, params, auth = false) {
    try {
      return axiosInstance(auth).post(`${API_URL}/${resource}/`, params);
    } catch (error) {
      throw new Error(`[RWV] ApiService ${error}`);
    }
  },

  async update(resource, slug, params, auth = false) {
    try {
      return axiosInstance(auth).put(`${API_URL}/${resource}/${slug}/`, params);
    } catch (error) {
      throw new Error(`[RWV] ApiService ${error}`);
    }
  },

  async put(resource, params, auth = false) {
    try {
      return axiosInstance(auth).put(`${API_URL}/${resource}/`, params);
    } catch (error) {
      throw new Error(`[RWV] ApiService ${error}`);
    }
  },

  async delete(resource, auth = false) {
    try {
      return axiosInstance(auth).delete(resource);
    } catch (error) {
      throw new Error(`[RWV] ApiService ${error}`);
    }
  },
};

export default ApiService;
