<template>
  <div class="site-section">
    <b-container>
      <b-row class="row mb-5">
        <b-form class="col-md-12" method="post">
          <div class="site-blocks-table">
           <table class="table">
              <thead>
                <tr>
                  <th>Image</th>
                  <th>Product</th>
                  <th>Price</th>
                  <th>Quantity</th>
                  <th>Total</th>
                  <th>Remove</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in cart" v-bind:key="item.product.id">
                  <td class="product-thumbnail">
                    <b-img  v-bind:src="item.product.image" alt="Image" class="img-fluid" style="height: 200px;"/>
                  </td>
                  <td class="product-name align-middle">
                    <h2 class="h5 text-black">{{ item.product.name}}</h2>
                  </td>
                  <td v-if="item.product.sale_price > 0" class="align-middle">
                    {{ item.product.sale_price | currency(currency_format) }}
                    </td>
                  <td v-else class="align-middle">{{ item.product.price | currency(currency_format) }}</td>
                  <td class="align-middle">
                    <number-spinner :min="0" :max="10" :value="item.quantity"
                    v-on:input="changeQuantity($event, item)">
                    </number-spinner>
                    {{ item.quanitity }}
                  </td>
                  <td class="align-middle">{{ (item.product.sale_price * item.quantity) | currency(currency_format) }}</td>
                  <td class="align-middle">
                    <b-button variant="primary"
                    class="height-auto btn-sm"
                    @click="deleteItem(item)">
                      X
                    </b-button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </b-form>
      </b-row>

      <b-row>
        <b-col md="6">
          <b-row class="mb-5">
            <b-col md="6">
              <b-button :to="{name: 'catalog'}" variant="outline-primary" class="btn-md btn-block">
                Continue Shopping
              </b-button>
            </b-col>
          </b-row>
        </b-col>
        <b-col md="6">
          <b-row class="justify-content-end">
            <b-col md="7">
              <b-row>
                <b-col md="12" class="text-right border-bottom mb-5">
                  <h3 class="text-black h4 text-uppercase">Cart Totals</h3>
                </b-col>
              </b-row>
              <b-row class="mb-3">
                <b-col md="6">
                  <span class="text-black">Subtotal</span>
                </b-col>
                <b-col md="6" class="text-right">
                  <span class="text-black">{{ subtotal | currency(currency_format) }}</span>
                </b-col>
              </b-row>
              <b-row class="mb-5">
                <b-col md="6">
                  <span class="text-black">Total</span>
                </b-col>
                <b-col md="6" class="text-right">
                  <strong class="text-black">{{ total | currency(currency_format) }} </strong>
                </b-col>
              </b-row>

              <b-row>
                <b-col md="12">
                  <b-button variant="primary" class="btn-md btn-block" :to="{name: 'checkout'}" :disabled="!total">
                    Proceed To Checkout
                  </b-button>
                </b-col>
              </b-row>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>

import { mapGetters } from 'vuex';
import {
  CART, REMOVE_ITEM, CHANGE_ITEM, GET_ITEMS_LIST, GET_TOTAL, GET_SUBTOTAL, GET_CURRENCY,
} from '@/store/types';
import NumberSpinner from '@/components/NumberSpinner.vue';

export default {

  name: 'Cart',

  components: {
    NumberSpinner,
  },

  computed: {
    ...mapGetters({
      cart: `${CART}${GET_ITEMS_LIST}`,
      total: `${CART}${GET_TOTAL}`,
      subtotal: `${CART}${GET_SUBTOTAL}`,
      currency_format: `${GET_CURRENCY}`,
    }),
  },

  methods: {
    deleteItem(item) {
      this.$store.dispatch(`${CART}${REMOVE_ITEM}`, item);
    },
    changeQuantity(event, item) {
      const value = { ...item, quantity: event };
      this.$store.dispatch(`${CART}${CHANGE_ITEM}`, value);
    },
  },

};

</script>
