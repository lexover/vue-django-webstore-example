<template>
  <body>
    <div class="site-wrap">
      <navbar-component />
      <b-breadcrumb
        v-if="path.length > 1"
        :items="path"
        class="bg-light py-3"
      />
      <router-view />
      <footer-component />
    </div>
  </body>
</template>

<script>

import { mapGetters } from 'vuex';
import { GET_PATH } from '@/store/getters.types';
import NavbarComponent from '@/components/Navbar/NavbarComponent.vue';
import FooterComponent from '@/components/FooterComponent.vue';

export default {

  name: 'TheMainView',

  components: {
    NavbarComponent,
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
