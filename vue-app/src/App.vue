<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>

import { mapActions } from 'vuex';
import { CART } from '@/store/namespaces.types';
import { INITIALIZE } from '@/store/actions.types';

export default {

  name: 'App',

  created() {
    this.initializeCart(this.$store);
  },

  methods: {
    ...mapActions({
      initializeCart: `${CART}${INITIALIZE}`,
    }),
  },
};

</script>
