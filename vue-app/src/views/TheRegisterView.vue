<template>
  <b-container class="pb-5">
    <b-row class="py-5">
      <b-col
        md="12"
        class=" mb-5 mb-md-0"
      >
        <h3 class="mb-3 text-black">
          Register:
        </h3>
        <b-form
          class="p-3 p-lg-5 border"
          @submit.prevent="onSubmit"
        >
          <b-row class="form-group">
            <b-col md="12">
              <label
                for="c_login"
                class="text-black"
              >User name(login):</label>
              <b-input
                id="c_username"
                v-model="form.username"
                type="text"
                class="form-control"
                name="c_username"
                placeholder="Login"
                debounce="500"
                autocomplete="username"
                :formatter="formatter"
                :state="loginState"
                @update="checkUnique"
              />
              <b-form-invalid-feedback id="input-live-feedback">
                User with such name already registered, please choose another
              </b-form-invalid-feedback>
            </b-col>
          </b-row>
          <b-row class="form-group">
            <b-col md="12">
              <label
                for="c_email"
                class="text-black"
              >E-mail:</label>
              <b-input
                id="c_email"
                v-model="form.email"
                type="text"
                class="form-control"
                name="c_email"
                placeholder="E-mail"
                autocomplete="email"
                :state="emailState"
              />
              <b-form-invalid-feedback id="input-live-feedback">
                Invalid email format
              </b-form-invalid-feedback>
            </b-col>
          </b-row>
          <b-row class="form-group">
            <b-col md="6">
              <label
                for="c_password"
                class="text-black"
              >Password:</label>
              <b-input
                id="c_password"
                v-model="form.password"
                type="password"
                class="form-control"
                name="c_password"
                placeholder="Password"
                autocomplete="new-password"
                :state="passwordState"
              />
              <b-form-invalid-feedback id="input-live-feedback">
                Enter at least 6 symbols
              </b-form-invalid-feedback>
            </b-col>
            <b-col md="6">
              <label
                for="c_repeatpassword"
                class="text-black"
              >Repeat the password:</label>
              <b-input
                id="c_repeatpassword"
                v-model="password_repeat"
                type="password"
                placeholder="Password"
                autocomplete="current-password"
                :state="repeatPasswordState"
              />
              <b-form-invalid-feedback id="input-live-feedback">
                The entered password does not match the previous
              </b-form-invalid-feedback>
            </b-col>
          </b-row>
          <b-row>
            <b-col
              md="8"
              class="text-left"
              style="color: red;"
            >
              <span v-if="errors.length > 0">{{ errors | error }}</span>
            </b-col>
            <b-col
              md="4"
              class="text-right"
            >
              <b-button
                type="submit"
                variant="primary"
                class="px-5"
                :disabled="buttonState"
                @click="onSubmit"
              >
                Register
              </b-button>
            </b-col>
          </b-row>
        </b-form>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>

import { mapGetters } from 'vuex';
import { USER } from '@/store/namespaces.types';
import { REGISTER, CHECK_UNIQUE } from '@/store/actions.types';
import { GET_ERRORS, IS_UNIQUE } from '@/store/getters.types';

export default {

  name: 'TheRegisterView',

  data() {
    return {
      form: {
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
    async onSubmit() {
      this.$store.dispatch(`${USER}${REGISTER}`, this.form).then((username) => {
        this.$bvModal.msgBoxOk(`${username} successful registered!`)
          .then(() => {
            this.$router.push({ name: 'profile' });
          });
      });
    },
    checkUnique() {
      this.$store.dispatch(`${USER}${CHECK_UNIQUE}`, this.form.username);
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
