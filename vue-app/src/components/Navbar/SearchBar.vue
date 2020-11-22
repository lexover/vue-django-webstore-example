<template>
  <div class="search-bar">
    <vue-bootstrap-typeahead v-model="search_string"
                             :data="products"
                             @hit="$emit('search', $event)"
                             debounce=500
                             placeholder="Search">
      <template slot="append">
        <button class="back-btn" @click="$emit('search')">
          <b-icon-back/>
        </button>
      </template>
    </vue-bootstrap-typeahead>
  </div>
</template>

<script>

import VueBootstrapTypeahead from 'vue-bootstrap-typeahead';
import {BIconBack} from 'bootstrap-vue';
import { mapGetters } from 'vuex';
import { PRODUCT, FETCH_NAMES, GET_NAMES_LIST } from '@/store/types';

export default {

  name: 'SearchBar',

  porps: {
    input: {
      type: String,
      default: '',
    },
  },

  components: {
    VueBootstrapTypeahead,
    BIconBack,
  },

  data() {
    return {
      search_string: '',
    };
  },

  computed: {
    ...mapGetters({
      products: `${PRODUCT}${GET_NAMES_LIST}`,
    }),
  },

  methods: {
    getProducts(input) {
      if (input.length > 1) {
        this.$store.dispatch(`${PRODUCT}${FETCH_NAMES}`, { search: input });
      }
    },
  },

  watch: {
    search_string(input) { this.getProducts(input); },
  },

};

</script>
