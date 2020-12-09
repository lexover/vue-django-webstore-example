import cart from "@/store/modules/cart.js"
import { POP_ITEM, 
         PUSH_ITEM, 
         SET_ITEM_QUANTITY, 
         SET_LIST,
         ADD_ITEM, 
         REMOVE_ITEM,
         CHANGE_ITEM,
         SAVE_DATA,
         LOAD_DATA,
         CLEAR_DATA,
         GET_ITEMS_COUNT,
         GET_SUBTOTAL,
         GET_TOTAL} from "../../../src/store/types"


describe("Cart actions and mutations", () => {
    const items = [
        { product: { id: 1, price: 20 }, quantity: 3 },
        { product: { id: 2, price: 10 }, quantity: 5 }
    ];
    const state = { cart_items: [] };

    it('Add item action new', () => {
        const commit = jest.fn();
        const newProduct = { product: { id: 3, price: 20} , quantity: 10 };
        cart.actions[ADD_ITEM]({ state, commit }, newProduct);

        expect(commit).toHaveBeenCalledWith(PUSH_ITEM, newProduct);
    })
    
    it('Add item action additional', () => {
        const commit = jest.fn();
        state.cart_items = items
        const newProduct = { product: { id: 1, price: 20 }, quantity: 10};
        cart.actions[ADD_ITEM]({ state, commit }, newProduct);
        
        const result = Object.assign(newProduct, { quantity: 13 });
        expect(commit).toHaveBeenCalledWith(SET_ITEM_QUANTITY, result);
    })

    it('Remove item acion', () => {
        const commit = jest.fn();
        cart.actions[REMOVE_ITEM]({ state, commit }, items[0]);
        
        expect(commit).toHaveBeenCalledWith(POP_ITEM, 0);
    })

    it('Change item action', () => {
        const commit = jest.fn();
        const product = { product: { id: 1, price: 20 }, quantity: 10 };
        cart.actions[CHANGE_ITEM]({ state, commit }, product);

        expect(commit).toHaveBeenCalledWith(SET_ITEM_QUANTITY, product);
    })

    it('Clear data', () => {
        const commit = jest.fn();
        cart.actions[CLEAR_DATA]({ commit });

        expect(commit).toHaveBeenCalledWith(SET_LIST, []);
    })

    it('Prersistance check', () => {
        state.cart_items = items;
        cart.actions[SAVE_DATA]({ state });
        const commit = jest.fn();
        cart.actions[LOAD_DATA]({ commit });

        expect(commit).toHaveBeenCalledWith(SET_LIST, items); 
    })
})

describe("Cart actions", () => {
        const items = [
            { product: {id: 1, price: 20}, quantity: 3 },
            { product: {id: 2, price: 10}, quantity: 5 }
        ];
        const state = { cart_items: [] };

    it('Add item action new', () => {
        const commit = jest.fn();
        const newProduct = { product: { id: 3, price: 20 }, quantity: 10 };
        cart.actions[ADD_ITEM]({ state, commit }, newProduct);

        expect(commit).toHaveBeenCalledWith(PUSH_ITEM, newProduct);
    })
    
    it('Add item action additional', () => {
        const commit = jest.fn();
        state.cart_items = items;
        const newProduct = { product: { id: 1, price: 20 }, quantity: 10 };
        cart.actions[ADD_ITEM]({ state, commit }, newProduct);
        
        const result = Object.assign(newProduct, { quantity: 13 });
        expect(commit).toHaveBeenCalledWith(SET_ITEM_QUANTITY, result);
    })

    it('Remove item acion', () => {
        const commit = jest.fn();
        state.cart_items = items;
        cart.actions[REMOVE_ITEM]({ state, commit }, items[0]);
        
        expect(commit).toHaveBeenCalledWith(POP_ITEM, 0);
    })

    it('Change item action', () => {
        const commit = jest.fn();
        const product = { product: { id: 1, price: 20 }, quantity: 10 };
        cart.actions[CHANGE_ITEM]({ state, commit }, product);

        expect(commit).toHaveBeenCalledWith(SET_ITEM_QUANTITY, product);
    })

    it('Clear data', () => {
        const commit = jest.fn();
        cart.actions[CLEAR_DATA]({ commit });

        expect(commit).toHaveBeenCalledWith(SET_LIST, []);
    })

    it('Prersistance check', () => {
        state.cart_items = items;
        cart.actions[SAVE_DATA]({ state });
        const commit = jest.fn();
        cart.actions[LOAD_DATA]({ commit });

        expect(commit).toHaveBeenCalledWith(SET_LIST, items); 
    })
})

describe("Cart item store", () => {
        const items = [
            { product: { id: 1, price: 10, sale_price: 5 }, quantity: 3 },
            { product: { id: 2, price: 20, sale_price: 15 }, quantity: 5 }
        ];
        const state = { cart_items: items };

    it('Get items count', () => {
        expect(cart.getters[GET_ITEMS_COUNT](state)).toEqual(8);
    })

    it('Get subtotal', () => {
        expect(cart.getters[GET_SUBTOTAL](state)).toEqual(130);
    })
    
    it('Get total', () => {
        expect(cart.getters[GET_TOTAL](state)).toEqual(90);
    })
})
