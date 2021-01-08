<template>
  <div class="site-section">
    <b-container>
      <b-row v-if="errors.length > 0">
        <error-component errors="errors" />
      </b-row>
      <b-row
        v-else-if="loading"
        class="text-center"
      >
        <b-col md="12">
          <b-icon-arrow-clockwise
            animation="spin"
            font-scale="4"
          />
        </b-col>
      </b-row>
      <b-row v-else>
        <b-col
          md="5"
          class="mr-auto"
        >
          <div class="border text-center">
            <b-img
              :src="product.image"
              alt="Image"
              class="img-fluid p-5"
            />
          </div>
        </b-col>
        <b-col md="6">
          <h2 class="text-black">
            {{ product.name }}
          </h2>
          <p>{{ product.description }} </p>
          <p>
            <rating-component
              :value="product.rating.value"
              :votes="product.rating.votes"
              :editable="false"
            />
          </p>
          <p>
            <del v-if="product.sale_price < product.price">
              {{ product.price| currency(currency_format) }}
            </del>
            <strong class="text-primary h4">
              {{ product.sale_price | currency(currency_format) }}
            </strong>
          </p>
          <div class="mb-5">
            <number-spinner-component
              v-model="quantity"
              :min="0"
              :max="10"
            />
          </div>
          <p>
            <b-button
              variant="primary"
              class="buy-now height-auto px-4 py-3"
              @click="addToCart"
            >
              Add To Cart
            </b-button>
          </p>
          <b-tabs class="py-4">
            <b-tab
              title="Specification"
              active
            >
              <p class="p-3">
                {{ product.description }}
              </p>
            </b-tab>
            <b-tab title="Reviews">
              <review-component :product-id="id" />
            </b-tab>
          </b-tabs>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import { BIconArrowClockwise } from 'bootstrap-vue';
import { mapGetters } from 'vuex';
import {
  PRODUCT,
  CART,
  USER,
} from '@/store/namespaces.types';
import {
  FETCH_ITEM,
  ADD_ITEM,
  CREATE_ITEM,
} from '@/store/actions.types';
import {
  GET_ITEM,
  IS_LOADING,
  GET_CURRENCY,
  GET_ERRORS,
  IS_AUTH,
} from '@/store/getters.types';
import NumberSpinnerComponent from '@/components/NumberSpinnerComponent.vue';
import ErrorComponent from '@/components/ErrorComponent.vue';
import RatingComponent from '@/components/RatingComponent.vue';
import ReviewComponent from '@/components/ReviewComponent.vue';

export default {

  name: 'TheProductView',

  components: {
    NumberSpinnerComponent,
    ErrorComponent,
    BIconArrowClockwise,
    RatingComponent,
    ReviewComponent,
  },

  props: {
    id: {
      type: Number,
      required: true,
    },
  },

  data() {
    return {
      quantity: 1,
      rating: 3,
      votesNumber: 21,
    };
  },

  computed: {
    ...mapGetters({
      product: `${PRODUCT}${GET_ITEM}`,
      loading: `${PRODUCT}${IS_LOADING}`,
      currency_format: `${GET_CURRENCY}`,
      errors: `${GET_ERRORS}`,
      isAuthenticated: `${USER}${IS_AUTH}`,
    }),
  },

  created() {
    this.$store.dispatch(`${PRODUCT}${FETCH_ITEM}`, this.id);
  },

  methods: {
    addToCart() {
      const quantityVal = Number(this.quantity);
      if (quantityVal > 0) {
        this.$store.dispatch(`${CART}${ADD_ITEM}`, { product: this.product, quantity: quantityVal });
      }
    },
    setRating(rating) {
      this.$store.dispatch(`${PRODUCT}${CREATE_ITEM}`, { product: this.product.id, rating, review: '' });
    },
  },
};
</script>
