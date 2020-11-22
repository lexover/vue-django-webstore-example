<template>
  <body>
    <div class="site-wrap">
      <navbar/>
      <b-breadcrumb v-if="path.length > 1" :items="path" class="bg-light py-3"></b-breadcrumb>
      <router-view/>
      <footer-component/>
    </div>
  </body>
</template>

<script>

import { mapGetters } from 'vuex';
import { GET_PATH } from '@/store/types';
import Navbar from '@/components/Navbar/Navbar.vue';
import FooterComponent from '@/components/Footer.vue';

export default {

  name: 'iMain',

  components: {
    Navbar,
    FooterComponent,
  },

  data() {
    return {
      search_shown: false,
      search_string: 'Hello',
    };
  },

  computed: {
    ...mapGetters({
      path: GET_PATH,
    }),
  },

};

</script>

<style lang="scss">
.breadcrumb {
  border-radius: 0;
  text-transform: capitalize;
}
</style>