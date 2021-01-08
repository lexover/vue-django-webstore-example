<template>
  <div>
    <products-filter-component
      :min="prices_range.min"
      :max="prices_range.max"
      @change-order="changeOrder"
      @change-price="changePrice"
    />
    <div class="site-section bg-light">
      <b-container>
        <b-row v-if="!loading">
          <template v-for="product in products">
            <b-col
              :key="product.id"
              sm="6"
              lg="4"
              class="text-center item mb-4 item-v2"
            >
              <span
                v-if="product.sale"
                class="onsale"
              >Sale</span>
              <router-link :to="{name: 'product', params: {id: product.id}}">
                <b-img :src="product.image" />
                <h3>
                  <a>{{ product.name }}</a>
                </h3>
                <p class="price">
                  <span v-if="product.sale_price < product.price">
                    <del>{{ product.price | currency(currency_format) }}</del> -
                  </span>
                  {{ product.sale_price| currency(currency_format) }}
                </p>
              </router-link>
            </b-col>
          </template>
        </b-row>
        <b-row v-else-if="errors.length > 0">
          <error-component :errors="errors" />
        </b-row>
        <b-row
          v-else
          class="text-center"
        >
          <b-col md="12">
            <b-icon-arrow-clockwise
              animation="spin"
              font-scale="4"
            />
          </b-col>
        </b-row>
        <b-row class="mt-5">
          <b-col
            md="12"
            class="text-center"
          >
            <b-pagination
              pills
              :total-rows="products_number"
              :per-page="items_per_page"
              class="site-block-27"
              align="center"
              @change="changePage"
            />
          </b-col>
        </b-row>
      </b-container>
    </div>
  </div>
</template>

<script>

import { BIconArrowClockwise, BPagination } from 'bootstrap-vue';
import { mapGetters } from 'vuex';
import { PRODUCT } from '@/store/namespaces.types';
import { FETCH_ITEMS_LIST } from '@/store/actions.types';
import {
  GET_ITEMS_LIST,
  GET_ITEMS_COUNT,
  GET_PRICES_RANGE,
  GET_CURRENCY,
  GET_ERRORS,
  IS_LOADING,
} from '@/store/getters.types';
import ProductsFilterComponent from '@/components/ProductsFilterComponent.vue';
import ErrorComponent from '@/components/ErrorComponent.vue';

export default {

  name: 'TheProductsListView',

  components: {
    BIconArrowClockwise,
    BPagination,
    ProductsFilterComponent,
    ErrorComponent,
  },

  data() {
    return {
      items_per_page: 6,
    };
  },

  computed: {
    ...mapGetters({
      products: `${PRODUCT}${GET_ITEMS_LIST}`,
      loading: `${PRODUCT}${IS_LOADING}`,
      products_number: `${PRODUCT}${GET_ITEMS_COUNT}`,
      prices_range: `${PRODUCT}${GET_PRICES_RANGE}`,
      currency_format: `${GET_CURRENCY}`,
      errors: `${GET_ERRORS}`,
    }),
  },

  created() {
    this.$store.dispatch(`${PRODUCT}${FETCH_ITEMS_LIST}`);
  },

  methods: {
    changeOrder(ordering) {
      this.$store.dispatch(`${PRODUCT}${FETCH_ITEMS_LIST}`, { ordering });
    },
    changePage(page) {
      const offset = (Number(page) - 1) * this.items_per_page;
      this.$store.dispatch(`${PRODUCT}${FETCH_ITEMS_LIST}`, { limit: this.items_per_page, offset });
    },
    changePrice(price) {
      this.$store.dispatch(`${PRODUCT}${FETCH_ITEMS_LIST}`, { max_price: price.max, min_price: price.min });
    },
  },
};

</script>
