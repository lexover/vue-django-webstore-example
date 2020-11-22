<template>
    <b-container class="filter-panel">
      <b-row>
        <b-col lg="4">
          <label for="category" class="text-uppercase text-black d-block">Category:</label>
          <b-dropdown block id="category"
                      class="mx-1"
                      variant="primary"
                      menu-class="w-100"
                      :text="group">
            <b-dropdown-item @click="changeGroup()">All</b-dropdown-item>
            <b-dropdown-item v-for="group in group_list"
                             :key="group.id"
                             @click="changeGroup(group)">
                                {{ group.name }}
            </b-dropdown-item>
          </b-dropdown>
        </b-col>
        <b-col lg="4">
          <label for="price-range" class="text-uppercase text-black d-block">
            Price: {{ value[0] | currency(currency_format) }}
             - {{ value[1] | currency(currency_format) }}
          </label>
          <double-range-slider id="price-range"
                               :minThreshold="prices_range.min"
                               :maxThreshold="prices_range.max"
                               :min="prices_range.min"
                               :max="prices_range.max"
                               @update="updateValue"
                               @change="$emit('change-price', $event)"/>
        </b-col>
        <b-col lg="4" class="text-lg-right">
          <label for="order" class="text-uppercase text-black d-block">Order by:</label>
          <b-dropdown block id="order" variant="primary" menu-class="w-100" :text="order">
            <b-dropdown-item v-for="order_item in order_items"
                             :key="order_item.id"
                             @click="changeOrder(order_item)">
                                {{ order_item.text }}
            </b-dropdown-item>
          </b-dropdown>
        </b-col>
      </b-row>
    </b-container>
</template>

<script>

import { mapGetters } from 'vuex';
import DoubleRangeSlider from '@/components/DoubleRangeSlider/DoubleRangeSlider.vue';
import {
  PRODUCT_CATEGORIES, PRODUCT, FETCH_LIST, RESET_FILTER,
  GET_ITEMS_LIST, GET_PRICES_RANGE, GET_CURRENCY,
} from '@/store/types';

export default {

  name: 'ProductsFilter',

  components: {
    DoubleRangeSlider,
  },

  data() {
    return {
      value: [0, 0],
      group: 'All',
      order: 'Relevance',
      order_items: [
        { id: 0, filter: 'relevance', text: 'Relevance' },
        { id: 1, filter: 'name', text: 'Name, A to Z' },
        { id: 2, filter: '-name', text: 'Name, Z to A' },
        { id: 3, filter: 'price', text: 'Price, low to high' },
        { id: 4, filter: '-price', text: 'Price, high to low' },
      ],
    };
  },

  created() {
    this.$store.dispatch(`${PRODUCT_CATEGORIES}${FETCH_LIST}`);
  },

  computed: {
    ...mapGetters({
      prices_range: `${PRODUCT}${GET_PRICES_RANGE}`,
      group_list: `${PRODUCT_CATEGORIES}${GET_ITEMS_LIST}`,
      currency_format: `${GET_CURRENCY}`,
    }),
  },

  methods: {
    updateValue(event) {
      this.value = [event.min, event.max];
    },
    changeGroup(groupVal) {
      let groupId = {};
      if (groupVal !== undefined) {
        groupId = { group: groupVal.id };
        this.group = groupVal.name;
      } else {
        this.group = 'All';
      }
      this.$store.dispatch(`${PRODUCT}${RESET_FILTER}`);
      this.$store.dispatch(`${PRODUCT}${FETCH_LIST}`, groupId);
    },
    changeOrder(orderItem) {
      this.$emit('change-order', orderItem.filter);
      this.order = orderItem.text;
    },
  },

};

</script>
