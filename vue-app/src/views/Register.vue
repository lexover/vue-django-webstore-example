<template>
  <b-container class="pb-5">
    <b-row class="py-5">
      <b-col md="12" class=" mb-5 mb-md-0">
        <h3 class="mb-3 text-black">Register:</h3>
        <div class="p-3 p-lg-5 border">
          <b-row class="form-group">
            <b-col md="6">
              <label for="c_first_name" class="text-black">First name:</label>
              <b-input type="text"
                       id="c_first_name"
                       class="form-control"
                       name="c_first_name"
                       placeholder="Fist name"
                       v-model="form.first_name"/>
            </b-col>
            <b-col md="6">
              <label for="c_last_name" class="text-black">Last name:</label>
              <b-input type="text"
                       id="c_last_name"
                       class="form-control"
                       name="c_last_name"
                       placeholder="Last name"
                       v-model="form.last_name"/>
            </b-col>
          </b-row>
          <b-row class="form-group">
            <b-col md="12">
              <label for="c_login" class="text-black">User name(login):</label>
              <b-input type="text"
                       id="c_username"
                       class="form-control"
                       name="c_username"
                       placeholder="Login"
                       v-model="form.username"
                       debounce="500"
                       @update="checkUnique"
                       :formatter="formatter"
                       :state="loginState"/>
              <b-form-invalid-feedback id="input-live-feedback">
                User with such name already registered, please choose another
              </b-form-invalid-feedback>
            </b-col>
          </b-row>
          <b-row class="form-group">
            <b-col md="12">
              <label for="c_email" class="text-black">E-mail:</label>
              <b-input type="text"
                       id="c_email"
                       class="form-control"
                       name="c_email"
                       placeholder="E-mail"
                       v-model="form.email"
                       :state="emailState"/>
              <b-form-invalid-feedback id="input-live-feedback">
                Invalid email format
              </b-form-invalid-feedback>
            </b-col>
          </b-row>
          <b-row class="form-group">
            <b-col md="6">
              <label for="c_password" class="text-black">Password:</label>
              <b-input type="password"
                       id="c_password"
                       class="form-control"
                       name="c_password"
                       placeholder="Password"
                       v-model="form.password"
                       :state="passwordState"/>
              <b-form-invalid-feedback id="input-live-feedback">
                Enter at least 6 symbols
              </b-form-invalid-feedback>
            </b-col>
            <b-col md="6">
              <label for="c_repeatpassword" class="text-black">Repeat the password:</label>
              <b-input type="password"
                       id="c_repeatpassword"
                       placeholder="Password"
                       v-model="password_repeat"
                       :state="repeatPasswordState"/>
              <b-form-invalid-feedback id="input-live-feedback">
                The entered password does not match the previous
              </b-form-invalid-feedback>
            </b-col>
          </b-row>
          <b-row>
            <b-col md="8" class="text-left" style="color: red;">
              <span v-if="errors.length > 0">{{ errors | error }}</span>
            </b-col>
            <b-col md="4" class="text-right">
              <b-button type="submit"
                        variant="primary"
                        class="px-5"
                        @click="onSubmit"
                        :disabled="buttonState">
                          Register
              </b-button>
            </b-col>
          </b-row>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>

import { mapGetters } from 'vuex';
import { USER, REGISTER, GET_ERRORS, IS_UNIQUE, CHECK_UNIQUE } from '@/store/types';

export default {

  name: 'Register',

  data() {
    return {
      form: {
        first_name: '',
        last_name: '',
        email: '',
        username: '',
        password: '',
      },
      password_repeat: '',
    };
  },

  computed: {
    ...mapGetters({
      errors: `${GET_ERRORS}`,
      loginState: `${USER}${IS_UNIQUE}`,
    }),
    passwordState() {
      if (this.form.password.length < 1) return null;
      return this.form.password.length > 5;
    },
    repeatPasswordState() {
      if (this.password_repeat.length < 1) return null;
      return this.password_repeat === this.form.password;
    },
    emailState() {
      if (this.form.email.length < 1) return null;
      const re = /.+@.+\..+/i;
      return re.test(this.form.email.toLowerCase());
    },
    buttonState() {
      return !(this.passwordState
            && this.repeatPasswordState
            && this.loginState
            && this.emailState);
    },
  },

  methods: {
    async onSubmit(evt) {
      evt.preventDefault();
      this.$store.dispatch(`${USER}${REGISTER}`, this.form).then(username => {
        this.$bvModal.msgBoxOk(`${username} successful registered!`)
          .then(() => {
             this.$router.push({name: 'profile'});
          })
      });
    },
    checkUnique() {
      this.$store.dispatch(`${USER}${CHECK_UNIQUE}`, this.form.username)
    },
    formatter(value) {
      if (/^[a-zA-Z0-9_]+$/gi.test(value)) {
        return value;
      }
      return '';
    },
  },

};

</script>
