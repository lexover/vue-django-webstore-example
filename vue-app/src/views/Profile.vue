<template>
  <b-container v-if="user" class="pb-5">

    <b-row class="pt-3">
      <h3 class="mb-3 text-black text-capitalize">{{ user.username }} profile:</h3>
    </b-row>
    <b-form class="py-3 ">
        <b-form-group label-cols="4" label-cols-lg="2" label="Fist name:" label-for='c_first_name'>
            <b-input type="text" 
                     id="c_first_name" 
                     class="form-control" 
                     placeholder="Fist name" 
                     :disabled="!isChange"
                     :value="user.first_name"/>
        </b-form-group>
        <b-form-group label-cols="4" label-cols-lg="2" label="Last name:" label-for='c_last_name'>
            <b-input type="text" 
                     id="c_last_name" 
                     class="form-control" 
                     placeholder="Last name" 
                     :disabled="!isChange"
                     :value="user.last_name"/>
        </b-form-group>
        <b-form-group label-cols="4" label-cols-lg="2" label="Last name:" label-for='c_last_name'>
            <b-input type="text"
                      id="c_email"
                      class="form-control"
                      placeholder="E-mail"
                      :disabled="!isChange"
                      :value="user.email"/>
            <b-form-invalid-feedback id="input-live-feedback">
              Invalid email format
            </b-form-invalid-feedback>
        </b-form-group>
        <div class="text-right">
        <b-button v-if="isChange" variant="primary" class="px-5" @click="cancel">
          Cancel 
        </b-button>
        <b-button variant="outline-primary" class="mx-3 px-5" @click="change" :disabled=true>
          Change
        </b-button>
        </div>
        <ul>
          <li v-for="(v, k) in errors" :key="k" class="text-danger">{{ v | error }} </li>
        </ul>
    </b-form>

    <b-row> 
      <b-col md=12 class="px-5">
        <h4>Orders:</h4>
      </b-col>
    </b-row>
    <b-row class="px-3 px-lg-5">
      <b-table-simple>
        <b-thead>
          <b-th> Order #</b-th>
          <b-th> Date </b-th>
          <b-th> Total Price </b-th>
          <b-th> Status </b-th>
        </b-thead>
        <b-tr v-for="order in orders" :key="order.id">
          <b-td>{{ order.id }}</b-td>
          <b-td>{{ order.order_created | dateTime }}</b-td>
          <b-td>{{ order.total | currency(currency_format) }}</b-td>
          <b-td>{{ order.order_status | status }}</b-td>
        </b-tr>
      </b-table-simple>
    </b-row>
  </b-container>
</template>

<script>

import { mapGetters } from 'vuex';
import { USER, ORDER, FETCH_LIST, FETCH_ITEM, GET_ITEMS_LIST, GET_ITEM, GET_ERRORS, GET_CURRENCY} from '@/store/types'

export default {

  name: 'Profile',

  data() {
    return {
      isChange: false,
      userForm: {},
      oldValue: {},
    }
  },

  computed: {
    ...mapGetters({
      user: `${USER}${GET_ITEM}`,
      orders: `${ORDER}${GET_ITEMS_LIST}`,
      errors: `${GET_ERRORS}`,
      currency_format: `${GET_CURRENCY}`,
    }),
  },

  created() {
    this.$store.dispatch(`${USER}${FETCH_ITEM}`);
    this.$store.dispatch(`${ORDER}${FETCH_LIST}`);
  },

  methods: {
    change() {
      this.isChange = !this.isChange;
    },
    cancel() {
      this.isChange = false;
    }
  },

};

</script>
