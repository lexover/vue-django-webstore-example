<template>
  <div class="site-section">
    <b-container>
      <b-row v-if="errors.length > 0">
        <error-component errors="errors"/>
      </b-row>
      <b-row v-else-if="loading" class="text-center">
        <b-col md="12">
          <b-icon-arrow-clockwise animation="spin" font-scale="4"/>
        </b-col>
      </b-row>
      <b-row v-else>
        <b-col md="5" class="mr-auto">
          <div class="border text-center">
            <b-img :src="product.image" alt="Image" class="img-fluid p-5"/>
          </div>
        </b-col>
        <b-col md="6">
          <h2 class="text-black">{{ product.name }}</h2>
          <p>{{ product.description }} </p>
          <p >
            <del v-if="product.sale_price < product.price">
              {{ product.price| currency(currency_format) }}
            </del>
            <strong class="text-primary h4">{{ product.sale_price | currency(currency_format) }}</strong>
          </p>
          <div class="mb-5">
              <number-spinner :min="0" :max="10" v-model="quantity"/>
          </div>
          <p>
            <b-button variant="primary" class="buy-now height-auto px-4 py-3" @click="addToCart">
              Add To Cart
            </b-button>
          </p>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>

import { BIconArrowClockwise } from 'bootstrap-vue';
import { mapGetters } from 'vuex';
import {
  PRODUCT, CART, FETCH_ITEM, ADD_ITEM, GET_ITEM, GET_LOADING, GET_CURRENCY, GET_ERRORS,
} from '@/store/types';
import NumberSpinner from '@/components/NumberSpinner.vue';
import ErrorComponent from '@/components/ErrorComponent.vue'

export default {

  name: 'ProductInfo',

  components: {
    NumberSpinner,
    ErrorComponent,
    BIconArrowClockwise,
  },

  props: {
    id: {
      required: true,
    },
  },

  data() {
    return {
      quantity: 1,
    };
  },

  created() {
    this.$store.dispatch(`${PRODUCT}${FETCH_ITEM}`, this.id);
  },

  computed: {
    ...mapGetters({
      product: `${PRODUCT}${GET_ITEM}`,
      loading: `${PRODUCT}${GET_LOADING}`,
      currency_format: `${GET_CURRENCY}`,
      errors: `${GET_ERRORS}`,
    }),
  },

  methods: {
    addToCart() {
      const quantityVal = Number(this.quantity);
      if (quantityVal > 0) {
        this.$store.dispatch(`${CART}${ADD_ITEM}`, { product: this.product, quantity: quantityVal });
      }
    },
  },

};

</script>
