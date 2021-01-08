<template>
  <b-container fluid>
    <b-row v-if="isReviewsListEmpty">
      <p class="p-3">
        There are no reviews yet. You can add the first one.
      </p>
    </b-row>
    <b-row
      v-for="review in reviewsList"
      :key="review.id"
    >
      <b-col md="12">
        <div class="review-item pt-3 pb-3">
          <span>Rating: </span>
          <rating-component :value="review.rating" />
          <div class="review-content py-2">
            {{ review.review }}
          </div>
        </div>
      </b-col>
    </b-row>
    <b-row
      v-if="showEditor"
      class="review-editor"
    >
      <b-col md="12">
        <b-form>
          <div class="py-3">
            <span>Your product rating: </span>
            <rating-component
              v-model="formData.rating"
              :editable="true"
              :votes-number="0"
            />
          </div>
          <b-form-textarea
            v-model="formData.review"
            rows="3"
            max-rows="6"
            placeholder="Write your review here..."
          />
          <div class="text-right">
            <b-button
              variant="outline-primary"
              class="height-auto my-3 mr-2"
              @click="cancelReview"
            >
              Cancel
            </b-button>
            <b-button
              variant="primary"
              class="height-auto my-3"
              :disabled="!createActive"
              @click="createReview"
            >
              Create review
            </b-button>
          </div>
        </b-form>
      </b-col>
    </b-row>
    <b-row v-if="!showEditor">
      <b-col
        md="12"
        class="text-right"
      >
        <b-button
          v-if="isCreateReviewAvailable"
          variant="primary"
          class="height-auto px-2 py-1 my-3"
          @click="showEditor=true"
        >
          Create review
        </b-button>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import {
  REVIEW,
  USER,
} from '@/store/namespaces.types';
import {
  FETCH_ITEMS_LIST,
  FETCH_ITEM,
  CREATE_ITEM,
} from '@/store/actions.types';
import {
  GET_ITEMS_LIST,
  GET_ITEM,
  IS_AUTH,
} from '@/store/getters.types';
import RatingComponent from '@/components/RatingComponent.vue';

export default {
  name: 'ReviewComponent',
  components: {
    RatingComponent,
  },
  props: {
    productId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      showEditor: false,
      formData: { rating: 0, review: '' },
    };
  },
  computed: {
    ...mapGetters({
      reviewsList: `${REVIEW}${GET_ITEMS_LIST}`,
      usersReview: `${REVIEW}${GET_ITEM}`,
      user: `${USER}${GET_ITEM}`,
      isAuth: `${USER}${IS_AUTH}`,
    }),
    createActive() {
      return this.formData.rating > 0;
    },
    isReviewsListEmpty() {
      return !(typeof this.reviewsList !== 'undefined' && this.reviewsList.length > 0);
    },
    isCreateReviewAvailable() {
      return this.isAuth && !this.usersReview;
    },
  },
  created() {
    this.$store.dispatch(`${REVIEW}${FETCH_ITEMS_LIST}`, { product: this.productId });
    this.$store.dispatch(`${REVIEW}${FETCH_ITEM}`, { product: this.productId, user: this.user.id });
  },
  methods: {
    createReview() {
      this.$store.dispatch(`${REVIEW}${CREATE_ITEM}`, { ...this.formData, product: this.productId });
      this.cancelReview();
    },
    cancelReview() {
      this.formData = { rating: 0, review: '' };
      this.showEditor = false;
    },
  },
};
</script>

<style lang="scss" scoped>
.review-item {
    border-bottom: 1px solid lightgray;
    flex: 1;
}
</style>
