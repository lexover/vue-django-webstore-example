<template>

  <div id="app">
    <router-view/>
  </div>

</template>

<script>

import { mapActions } from 'vuex';
import { CART, INITIALIZE } from '@/store/types';

export default {

  name: 'app',

  methods: {
    ...mapActions({
      initializeCart: `${CART}${INITIALIZE}`,
    }),
  },

  created() {
    this.initializeCart(this.$store);
  },

};

</script>
