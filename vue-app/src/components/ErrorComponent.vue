<template>
  <b-container>
    <b-row>
      <b-col
        md="12"
        class="text-center pt-5"
      >
        <h1>Oops!</h1>
        <h2>Something Going Wrong</h2>
      </b-col>
    </b-row>
    <b-row>
      <b-col
        md="12"
        class="text-center"
      >
        <div>
          Sorry, an error has occured!
        </div>
        <div
          v-for="error in errors"
          :key="error.message"
        >
          {{ error }}
        </div>
      </b-col>
    </b-row>
    <b-row>
      <b-col
        md="12"
        class="text-center my-5"
      >
        <b-button
          variant="primary"
          class="m-2 p-2 navigate-button"
          :to="{ name: 'home'}"
        >
          <b-icon-house /> Take Me Home
        </b-button>
        <b-button
          variant="outline-primary"
          class="m-2 p-2 navigate-button"
          href="mailto: example@domen.dom"
        >
          <b-icon-envelope /> Contact Support
        </b-button>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>

import { BIconHouse, BIconEnvelope } from 'bootstrap-vue';

export default {

  name: 'ErrorComponent',

  components: {
    BIconHouse,
    BIconEnvelope,
  },

  props: {
    errors: {
      type: String,
      required: true,
    },
  },
};

</script>

<style lang="scss" scoped>
.navigate-button{
    width: 15em;
}
</style>
