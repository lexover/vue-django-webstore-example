<template>
  <b-col class="feature" lg="4">
    <span v-bind:class="iconClass" class="wrap-icon"/>
    <h3> {{ title }} </h3>
    <p> {{ text }} </p>
    <p>
      <a class="d-flex align-items-center" href="reference">
        <span class="mr-2">Learn more</span>
        <b-icon-chevron-right/>
      </a>
    </p>
  </b-col>
</template>

<script>

import { BIconChevronRight } from 'bootstrap-vue';

export default {

  name: 'Feature',

  components: {
    BIconChevronRight,
  },

  props: {
    iconClass: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    text: {
      type: String,
      required: true,
    },
    reference: {
      type: String,
      required: true,
    },
  },

};

</script>
