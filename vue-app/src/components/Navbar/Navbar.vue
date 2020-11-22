<template>
  <div>
    <search-bar v-if="search_shown" @search="search"/>
    <b-navbar v-else toggleable="lg">
      <b-navbar-brand href="/" class="site-logo">
        <strong class="text-primary">Pharma</strong>tive
      </b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="site-navigation">
          <b-nav-item :to="{name: 'home'}" exact active-class="active">Home</b-nav-item>
          <b-nav-item :to="{name: 'catalog'}" exact @click="goShop" active-class="active">
            Shop
          </b-nav-item>
          <b-nav-item :to="{name: 'about'}">About</b-nav-item>
        </b-navbar-nav>
        <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <b-nav-item @click="toggleSearch">
              <b-icon-search/>
            </b-nav-item>
            <b-nav-item class="bag">
              <router-link :to="{name: 'cart'}">
                <b-icon-handbag/>
                <span v-if="items_in_cart > 0" class="number">{{ items_in_cart }}</span>
              </router-link>
            </b-nav-item>
            <b-nav-item v-if="!isAuth" right :to="{name: 'login'}">
              <b-icon-person/>
            </b-nav-item>
            <b-nav-item-dropdown right v-else>
              <!-- Using 'button-content' slot -->
              <template v-slot:button-content>
              <b-icon-person-fill/>
              </template>
              <b-dropdown-item @click="goToProfile" style="text-transform: capitalize;">{{ user.username }}</b-dropdown-item>
              <b-dropdown-item @click="logout">Sign Out</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-navbar-nav>
      </b-collapse>
    </b-navbar>

  </div>
</template>

<script>

import { BIconSearch, BIconHandbag, BIconPerson, BIconPersonFill } from 'bootstrap-vue';
import { mapGetters } from 'vuex';
import {
  PRODUCT, PRODUCT_CATEGORIES, CART, FETCH_LIST, RESET_FILTER,
  GET_ITEMS_COUNT, GET_ITEMS_LIST, USER, GET_ITEM, IS_AUTH, LOGOUT,
} from '@/store/types';
import SearchBar from './SearchBar.vue';

export default {

  name: 'Navbar',

  components: {
    SearchBar,
    BIconSearch, 
    BIconHandbag,
    BIconPerson, 
    BIconPersonFill, 
  },

  data() {
    return {
      search_shown: false,
      input: '',
    };
  },

  computed: {
    ...mapGetters({
      group_list: `${PRODUCT_CATEGORIES}${GET_ITEMS_LIST}`,
      items_in_cart: `${CART}${GET_ITEMS_COUNT}`,
      user: `${USER}${GET_ITEM}`,
      isAuth: `${USER}${IS_AUTH}`,
    }),
  },

  methods: {
    toggleSearch() {
      this.search_shown = !this.search_shown;
    },
    search(event) {
      this.$router.push({ name: 'catalog' });
      this.$store.dispatch(`${PRODUCT}${FETCH_LIST}`, { search: event });
      this.search_shown = !this.search_shown;
    },
    goShop() {
      if (this.$router.currentRoute.fullPath === '/catalog/') {
        this.$store.dispatch(`${PRODUCT}${RESET_FILTER}`);
        this.$store.dispatch(`${PRODUCT}${FETCH_LIST}`);
      } else {
        this.$router.push({ name: 'catalog' });
      }
    },
    goToProfile() {
      if (this.$router.currentRoute.name !== 'profile') {
        this.$router.push({ name: 'profile' });
      }
    },
    logout() {
      this.$store.dispatch(`${USER}${LOGOUT}`);
      this.$router.go(-1);
    },
  },

};

</script>
