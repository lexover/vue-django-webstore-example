import cart from '@/store/modules/cart';
import {
  GET_ITEMS_COUNT,
  GET_SUBTOTAL,
  GET_TOTAL,
} from '@/store/getters.types';

describe('Cart item store', () => {
  const items = [
    { product: { id: 1, price: 10, sale_price: 5 }, quantity: 3 },
    { product: { id: 2, price: 20, sale_price: 15 }, quantity: 5 },
  ];
  const state = { cart_items_list: items };

  it('Get items count', () => {
    expect(cart.getters[GET_ITEMS_COUNT](state)).toEqual(8);
  });

  it('Get subtotal', () => {
    expect(cart.getters[GET_SUBTOTAL](state)).toEqual(130);
  });

  it('Get total', () => {
    expect(cart.getters[GET_TOTAL](state)).toEqual(90);
  });
});
