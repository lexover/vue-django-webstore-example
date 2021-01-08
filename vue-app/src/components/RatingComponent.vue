<template>
  <ul
    v-if="editable"
    class="rating"
  >
    <li
      v-for="n in 5"
      :key="n"
      :class="{'rating-active': checkRating(n)}"
      @mouseenter="updateRating(n)"
      @mouseleave="resetRating()"
      @click="$emit('input', n)"
    >
      <a>&#9734;</a>
    </li>
    <li v-if="votes">
      ({{ votes }})
    </li>
  </ul>
  <ul
    v-else
    class="rating"
  >
    <li
      v-for="n in 5"
      :key="n"
      :class="{'rating-active': checkRating(n)}"
    >
      &#9734;
    </li>
    <li v-if="votes">
      ({{ votes }})
    </li>
  </ul>
</template>

<script>
export default {
  name: 'RatingComponent',
  props: {
    value: {
      type: Number,
      required: true,
    },
    votes: {
      type: Number,
      default: NaN,
    },
    editable: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      current_rating: 0,
    };
  },
  beforeMount() {
    this.current_rating = this.value;
  },
  methods: {
    checkRating(n) {
      return n <= Math.round(this.current_rating);
    },
    updateRating(n) {
      this.current_rating = n;
    },
    resetRating() {
      this.current_rating = this.value;
    },
  },
};
</script>

<style lang="scss" scoped>
    .rating-active:before {
        content: "\2605";
        position: absolute;
        cursor: pointer;
    }
    ul{
        padding: 0;
        display: inline;
        li {
            display: inline-block;
            position: relative;
            width: 1.1em;
            cursor: default;
        }
    }

</style>
