<template>
  <footer class="site-footer bg-light">
    <b-container>
      <b-row>
        <b-col
          md="6"
          lg="4"
          class="mb-4 mb-lg-0"
        >
          <h3 class="footer-heading mb-4">
            About <strong class="text-primary">Pharmative</strong>
          </h3>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit.
            Eius quae reiciendis distinctio voluptates
            sed dolorum excepturi iure eaque, aut unde.
          </p>
        </b-col>
        <b-col
          lg="3"
          class="mx-auto mb-5 mb-lg-0"
        >
          <h3 class="footer-heading mb-4">
            Navigation
          </h3>
          <ul class="list-unstyled">
            <li>
              <router-link :to="{name: 'home'}">
                Home
              </router-link>
            </li>
            <li>
              <router-link :to="{name: 'catalog'}">
                Shop
              </router-link>
            </li>
            <li>
              <router-link :to="{name: 'about'}">
                About
              </router-link>
            </li>
          </ul>
        </b-col>

        <b-col
          md="6"
          lg="3"
        >
          <h3 class="footer-heading mb-4">
            Contact Info
          </h3>
          <ul class="list-unstyled">
            <li>
              <b-icon-house />203 Fake St. Mountain View, San Francisco, California, USA
            </li>
            <li>
              <b-icon-telephone /><a href="tel://23923929210">+2 392 3929 210</a>
            </li>
            <li>
              <b-icon-envelope />emailaddress@domain.com
            </li>
          </ul>
        </b-col>
      </b-row>

      <b-row class="pt-3 mt-3 text-center">
        <b-col md="12">
          <p>
            <!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
            Copyright &copy; 2020 <a href="mailto:lexxover@gmail.com">Lexover</a>
            All rights reserved | This website is based on a template developed
            by <a
              href="https://colorlib.com"
              target="_blank"
              class="text-primary"
            >Colorlib</a>
            <!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
          </p>
        </b-col>
      </b-row>
    </b-container>
  </footer>
</template>

<script>

import { BIconHouse, BIconTelephone, BIconEnvelope } from 'bootstrap-vue';

export default {

  name: 'FooterComponent',

  components: {
    BIconHouse,
    BIconTelephone,
    BIconEnvelope,
  },

};

</script>
