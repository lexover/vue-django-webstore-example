<template>
  <div class="search-bar">
    <vue-bootstrap-typeahead
      v-model="search_string"
      :data="products"
      debounce="500"
      placeholder="Search"
      @hit="$emit('search', $event)"
    >
      <template slot="append">
        <button
          class="back-btn"
          @click="$emit('search')"
        >
          <b-icon-back />
        </button>
      </template>
    </vue-bootstrap-typeahead>
  </div>
</template>

<script>

import VueBootstrapTypeahead from 'vue-bootstrap-typeahead';
import { BIconBack } from 'bootstrap-vue';
import { mapGetters } from 'vuex';
import { PRODUCT } from '@/store/namespaces.types';
import { FETCH_NAMES } from '@/store/actions.types';
import { GET_NAMES_LIST } from '@/store/getters.types';

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

  watch: {
    search_string(input) { this.getProducts(input); },
  },

  methods: {
    getProducts(input) {
      if (input.length > 1) {
        this.$store.dispatch(`${PRODUCT}${FETCH_NAMES}`, { search: input });
      }
    },
  },

};

</script>
