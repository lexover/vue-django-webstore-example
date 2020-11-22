<template>
  <div class="site-section">
    <b-container>
      <b-row class="mb-5">
        <b-col md="12">
          <div v-if="!isAuth" class="bg-light rounded p-3">
            <p class="mb-0">
              Returning shipping_address? <router-link :to="{name: 'login'}">Click here</router-link> to login
            </p>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col md="6" class=" mb-5 mb-md-0">
            <h2 class="h3 mb-3 text-black">Billing Details</h2>
            <div class="p-3 p-lg-5 border">
              <b-row class="form-group" style="padding: 0 15px;">
                <label for="c_country" class="text-black">
                  Country <span class="text-danger">*</span>
                </label>
                <b-form-select v-model="shipping_address.country"
                               :options="countries" value-field="id"
                               text-field="name">
                </b-form-select>
              </b-row>
              <b-row class="form-group">
                <b-col md="6">
                  <label for="c_fname" class="text-black">
                    First Name <span class="text-danger">*</span>
                  </label>
                  <b-input type="text"
                           class="form-control"
                           id="c_fname"
                           name="c_fname"
                           placeholder="First name"
                           v-model="shipping_address.first_name"
                           :state="firstNameState"/>
                  <b-form-invalid-feedback id="input-live-feedback">
                    Only letters allowed in name
                  </b-form-invalid-feedback>
                </b-col>
                <b-col md="6">
                  <label for="c_lname" class="text-black">
                    Last Name <span class="text-danger">*</span>
                  </label>
                  <b-input type="text"
                           class="form-control"
                           id="c_lname"
                           name="c_lname"
                           placeholder="Last name"
                           v-model="shipping_address.last_name"
                           :state="lastNameState"/>
                  <b-form-invalid-feedback id="input-live-feedback">
                    Only letters allowed in name
                  </b-form-invalid-feedback>
                </b-col>
              </b-row>
              <b-row class="form-group">
                <b-col md="12">
                  <label for="c_address" class="text-black">
                    Address <span class="text-danger">*</span>
                  </label>
                  <b-input type="text"
                           class="form-control"
                           id="c_address"
                           name="c_address"
                           placeholder="Address"
                           v-model="shipping_address.address"
                           :state="addressState"/>
                  <b-form-invalid-feedback id="input-live-feedback">
                    Address can't be shorter than 10 symbols
                  </b-form-invalid-feedback>
                </b-col>
              </b-row>
              <b-row class="form-group">
                <b-col md="12" >
                  <label for="c_email_address" class="text-black">
                    Email Address <span class="text-danger">*</span>
                  </label>
                  <b-input type="text"
                           class="form-control"
                           id="c_email_address"
                           name="c_email_address"
                           placeholder="E-mail"
                           v-model="shipping_address.email"
                           :state="emailState"/>
                  <b-form-invalid-feedback id="input-live-feedback">
                    Invalid email format
                  </b-form-invalid-feedback>
                </b-col>
              </b-row>
              <b-row class="form-group mb-5">
                <b-col md="12" >
                  <label for="c_phone" class="text-black">
                    Phone<span class="text-danger">*</span>
                  </label>
                  <b-input type="text"
                           class="form-control"
                           id="c_phone"
                           name="c_phone"
                           placeholder="Phone Number"
                           v-model="shipping_address.phone"
                           :state="phoneState"/>
                  <b-form-invalid-feedback id="input-live-feedback">
                    Invalid phone format
                  </b-form-invalid-feedback>
                </b-col>
              </b-row>
              <div class="form-group">
                <label for="c_order_notes" class="text-black">Order Notes</label>
                <textarea name="c_order_notes"
                          id="c_order_notes"
                          cols="30"
                          rows="5"
                          class="form-control"
                          placeholder="Write your notes here..."></textarea>
              </div>
            </div>
          </b-col>

          <b-col md="6">
            <b-row class="mb-5">
              <b-col md="12">
                <h2 class="h3 mb-3 text-black">Your Order</h2>
                <div class="p-3 p-lg-5 border">
                  <b-table-simple small class="mb-5">
                    <b-thead>
                      <b-th>Product</b-th>
                      <b-th>Total</b-th>
                    </b-thead>
                    <b-tbody>
                      <b-tr v-for="item in cart" v-bind:key="item.product.id">
                        <b-td>
                          {{ item.product.name }}
                           <strong class="mx-2">x</strong>
                            {{ item.quantity }}
                        </b-td>
                        <b-td>
                          {{ (item.product.sale_price * item.quantity) | currency(currency_format) }}
                        </b-td>
                      </b-tr>
                      <b-tr>
                        <b-td class="text-black font-weight-bold">
                          <strong>Cart Subtotal</strong>
                        </b-td>
                        <b-td class="text-black">{{ subtotal | currency(currency_format) }}</b-td>
                      </b-tr>
                      <b-tr>
                        <b-td class="text-black font-weight-bold">
                          <strong>Order Total</strong>
                        </b-td>
                        <b-td class="text-black font-weight-bold">
                          <strong>{{ total | currency(currency_format) }}</strong>
                        </b-td>
                      </b-tr>
                    </b-tbody>
                  </b-table-simple>

                  <div class="border mb-3">
                    <h3 class="h6 mb-0">
                      <a class="d-block p-4"
                         data-toggle="collapse"
                         href="#collapsebank"
                         role="button"
                         aria-expanded="false"
                         aria-controls="collapsebank">
                            Direct Bank Transfer
                      </a>
                    </h3>

                    <div class="collapse" id="collapsebank">
                      <div class="py-2 px-4">
                        <p class="mb-0">Make your payment directly into our bank account.
                           Please use your Order ID as the payment reference. Your order won't
                            be shipped until the funds have cleared in our account.</p>
                      </div>
                    </div>
                  </div>

                  <div class="border mb-5">
                    <h3 class="h6 mb-0">
                      <a class="d-block p-4"
                         data-toggle="collapse"
                         href="#collapsepaypal"
                         role="button"
                         aria-expanded="false"
                         aria-controls="collapsepaypal">
                            Paypal
                      </a>
                    </h3>

                    <div class="collapse" id="collapsepaypal">
                      <div class="py-2 px-4">
                        <p class="mb-0">Make your payment directly into our bank account.
                           Please use your Order ID as the payment reference. Your order won't
                            be shipped until the funds have cleared in our account.</p>
                      </div>
                    </div>
                  </div>

                  <div class="form-group">
                    <b-button variant="primary"
                              class="btn-lg btn-block"
                              :disabled="submitState"
                              @click="placeOrder">
                                Place Order
                    </b-button>
                  </div>

                  <div>
                    <ul>
                      <li v-for="(v, k) in errors" :key="k" class="text-danger">{{ v | error }} </li>
                    </ul>
                  </div>

                </div>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
    </b-container>
  </div>
</template>

<script>

import { mapGetters } from 'vuex';
import {
  COUNTRY, USER, FETCH_LIST, CART, CHECKOUT, GET_ITEMS_LIST, 
  GET_TOTAL, GET_SUBTOTAL, GET_CURRENCY, GET_ERRORS, CLEAR_DATA, IS_AUTH,
} from '@/store/types';

export default {

  name: 'Checkout',

  data() {
    return {
      otherAddress: false,
      createAccount: false,
      shipping_address: {
        country: '',
        first_name: '',
        last_name: '',
        address: '',
        email: '',
        phone: '',
      },
      creat_account: false,
      password: '',
      coupon_code: '',
    };
  },

  created() {
    this.$store.dispatch(`${COUNTRY}${FETCH_LIST}`);
  },

  computed: {
    ...mapGetters({
      cart: `${CART}${GET_ITEMS_LIST}`,
      total: `${CART}${GET_TOTAL}`,
      subtotal: `${CART}${GET_SUBTOTAL}`,
      countries: `${COUNTRY}${GET_ITEMS_LIST}`,
      currency_format: `${GET_CURRENCY}`,
      errors: `${GET_ERRORS}`,
      isAuth: `${USER}${IS_AUTH}`,
    }),

    firstNameState() {
      if (this.shipping_address.first_name < 1) return null;
      const re = /^\p{L}+$/gu;
      return re.test(this.shipping_address.first_name.toLowerCase());
    },

    lastNameState() {
      if (this.shipping_address.last_name < 1) return null;
      const re = /^\p{L}+$/gu;
      return re.test(this.shipping_address.last_name.toLowerCase());
    },

    addressState() {
      if (this.shipping_address.address < 1) return null;
      const val = !((this.shipping_address.address.length < 10));
      return val;
    },

    phoneState() {
      if (this.shipping_address.phone.length < 1) return null;
      const re = /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/i;
      return re.test(this.shipping_address.phone.toLowerCase());
    },

    emailState() {
      if (this.shipping_address.email.length < 1) return null;
      const re = /.+@.+\..+/i;
      return re.test(this.shipping_address.email.toLowerCase());
    },

    submitState() {
      return !(this.firstNameState && this.lastNameState && this.addressState
        && this.phoneState && this.emailState && this.total > 0);
    },

  },

  methods: {
    placeOrder() {
      const orderItemsData = [];
      this.cart.forEach((element) => {
        orderItemsData.push({ product: element.product.id, quantity: element.quantity });
      });
      this.$store.dispatch(`${CART}${CHECKOUT}`, { shipping_address: this.shipping_address, order_items: orderItemsData })
        .then(( id ) => {
          const add = (this.isAuth) ? 'You can see state of it in your profile.' :
           'You can not check it on website because you are not regitered yet';
          this.$bvModal.msgBoxOk(`Your order #${id} successfully placed. ${add}`)
            .then(() => {
              this.$store.dispatch(`${CART}${CLEAR_DATA}`);
              this.$router.push({ name: 'home' });
            })
        })
    },
  },

};

</script>
