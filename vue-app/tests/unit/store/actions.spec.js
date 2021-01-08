import review from '@/store/modules/review';
import cart from '@/store/modules/cart';
import { ApiService } from '@/common/api.service';
import { URL_REVIEWS } from '@/common/config';
import {
  FETCH_ITEM,
  FETCH_ITEMS_LIST,
  CREATE_ITEM,
  CHANGE_ITEM,
  SAVE_DATA,
  LOAD_DATA,
  CLEAR_DATA,
} from '@/store/actions.types';

import {
  SET_ITEM,
  SET_ITEMS_LIST,
  SET_LOADING,
  ADD_ITEM,
  REMOVE_ITEM,
  SET_ITEM_QUANTITY,
} from '@/store/mutations.types';

jest.mock('@/common/api.service');

describe('Review actions test case', () => {
  it('Get review item', () => {
    const commit = jest.fn();
    expect.assertions(2);
    return review.actions[FETCH_ITEM]({ commit }, 1, false)
      .then(() => {
        expect(commit).toHaveBeenNthCalledWith(1, SET_ITEM, {
          product: 1, user: 1, rating: 3, review: 'Test_1',
        });
        expect(ApiService.call_parameters).toEqual({
          method: 'query', resource: URL_REVIEWS, parameters: 1, auth: false,
        });
      });
  });

  it('Get reviews list', () => {
    const commit = jest.fn();
    expect.assertions(4);
    return review.actions[FETCH_ITEMS_LIST]({ commit }, 1, false).then(() => {
      expect(commit).toHaveBeenNthCalledWith(1, SET_LOADING, true);
      expect(commit).toHaveBeenNthCalledWith(2, SET_ITEMS_LIST,
        [{
          product: 1, user: 1, rating: 3, review: 'Test_1',
        },
        {
          product: 1, user: 2, rating: 4, review: 'Test_2',
        }]);
      expect(ApiService.call_parameters).toEqual({
        method: 'query', resource: URL_REVIEWS, parameters: 1, auth: false,
      });
      expect(commit).toHaveBeenNthCalledWith(3, SET_LOADING, false);
    });
  });

  it('Create review', () => {
    const commit = jest.fn();
    const result = { product: 1, rating: 3, review: 'Test' };
    expect.assertions(3);
    return review.actions[CREATE_ITEM]({ commit }, result).then(() => {
      expect(ApiService.call_parameters).toEqual({
        method: 'post',
        resource: URL_REVIEWS,
        parameters: result,
        auth: true,
      });
      expect(commit).toHaveBeenNthCalledWith(1, SET_ITEM, result);
      expect(commit).toHaveBeenNthCalledWith(2, ADD_ITEM, result);
    });
  });

  it('Change review', () => {
    const commit = jest.fn();
    const result = { product: 1, rating: 3, review: 'Test' };
    expect.assertions(3);
    return review.actions[CHANGE_ITEM]({ commit }, result).then(() => {
      expect(ApiService.call_parameters).toEqual({
        method: 'put',
        resource: URL_REVIEWS,
        parameters: result,
        auth: true,
      });
      expect(commit).toHaveBeenNthCalledWith(1, SET_ITEM, result);
      expect(commit).toHaveBeenNthCalledWith(2, CHANGE_ITEM, result);
    });
  });
});

describe('Cart actions test case', () => {
  const items = [
    { product: { id: 1, price: 20 }, quantity: 3 },
    { product: { id: 2, price: 10 }, quantity: 5 },
  ];
  const state = { cart_items_list: [] };

  it('Add item action new', () => {
    const commit = jest.fn();
    const newProduct = { product: { id: 3, price: 20 }, quantity: 10 };
    cart.actions[ADD_ITEM]({ state, commit }, newProduct);

    expect(commit).toHaveBeenCalledWith(ADD_ITEM, newProduct);
  });

  it('Add item action additional', () => {
    const commit = jest.fn();
    state.cart_items_list = items;
    const newProduct = { product: { id: 1, price: 20 }, quantity: 10 };
    cart.actions[ADD_ITEM]({ state, commit }, newProduct);

    const result = Object.assign(newProduct, { quantity: 13 });
    expect(commit).toHaveBeenCalledWith(SET_ITEM_QUANTITY, result);
  });

  it('Remove item action', () => {
    const commit = jest.fn();
    cart.actions[REMOVE_ITEM]({ state, commit }, items[0]);

    expect(commit).toHaveBeenCalledWith(REMOVE_ITEM, 0);
  });

  it('Change item action', () => {
    const commit = jest.fn();
    const product = { product: { id: 1, price: 20 }, quantity: 10 };
    cart.actions[CHANGE_ITEM]({ state, commit }, product);

    expect(commit).toHaveBeenCalledWith(SET_ITEM_QUANTITY, product);
  });

  it('Clear data', () => {
    const commit = jest.fn();
    cart.actions[CLEAR_DATA]({ commit });

    expect(commit).toHaveBeenCalledWith(SET_ITEMS_LIST, []);
  });

  it('Prersistance check', () => {
    state.cart_items_list = items;
    cart.actions[SAVE_DATA]({ state });
    const commit = jest.fn();
    cart.actions[LOAD_DATA]({ commit });

    expect(commit).toHaveBeenCalledWith(SET_ITEMS_LIST, items);
  });
});
