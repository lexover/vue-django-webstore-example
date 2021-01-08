import { URL_REVIEWS } from '../config';

const reviews = {
  1: {
    product: 1, user: 1, rating: 3, review: 'Test_1',
  },
  2: {
    product: 1, user: 2, rating: 4, review: 'Test_2',
  },
};

export const ApiService = {
  call_parameters: {},
  get(resource, slug, auth = false) {
    this.call_parameters = {
      method: 'get', resource, slug, auth,
    };
    return new Promise((resolve, reject) => {
      switch (resource) {
        case URL_REVIEWS: resolve({ data: reviews[slug] }); break;
        default: reject();
      }
    });
  },
  query(resource, parameters, auth = false) {
    this.call_parameters = {
      method: 'query', resource, parameters, auth,
    };
    return new Promise((resolve, reject) => {
      switch (resource) {
        case URL_REVIEWS: resolve({ data: { results: Object.values(reviews) } }); break;
        default: reject();
      }
    });
  },
  post(resource, params, auth = false) {
    this.call_parameters = {
      method: 'post', resource, parameters: params, auth,
    };
    return new Promise((resolve, reject) => {
      switch (resource) {
        case URL_REVIEWS: resolve({ data: params }); break;// { ...params, id: 1 } }); break;
        default: reject();
      }
    });
  },
  put(resource, params, auth = false) {
    this.call_parameters = {
      method: 'put', resource, parameters: params, auth,
    };
    return new Promise((resolve, reject) => {
      switch (resource) {
        case URL_REVIEWS: resolve({ data: params }); break;
        default: reject();
      }
    });
  },
};

export default ApiService;
