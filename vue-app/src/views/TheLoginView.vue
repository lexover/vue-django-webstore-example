<template>
  <b-container class="pb-5">
    <b-row class="py-5">
      <b-col
        md="12"
        class=" mb-5 mb-md-0"
      >
        <h3 class="mb-3 text-black">
          Login form:
        </h3>
        <div class="p-3 p-lg-5 border">
          <b-row class="form-group">
            <b-col md="12">
              <label
                for="c_login"
                class="text-black"
              >Login:</label>
              <b-input
                id="c_login"
                v-model="form.username"
                type="text"
                class="form-control"
                placeholder="E-mail or user name."
              />
            </b-col>
          </b-row>
          <b-row class="form-group">
            <b-col md="12">
              <label
                for="c_password"
                class="text-black"
              >Password:</label>
              <b-input
                id="c_password"
                v-model="form.password"
                type="password"
                class="form-control"
                placeholder="Password"
              />
            </b-col>
          </b-row>
          <b-row>
            <b-col
              md="12"
              class="text-right"
            >
              <b-button
                type="submit"
                variant="primary"
                class="mx-3 px-5"
                @click="login"
              >
                Login
              </b-button>
              <b-button
                :to="{name: 'register'}"
                variant="outline-primary"
                class="px-5"
              >
                Register
              </b-button>
            </b-col>
          </b-row>
          <b-row v-if="errors">
            <ul>
              <li
                v-for="(v, k) in errors"
                :key="k"
                class="text-danger"
              >
                {{ v | error }}
              </li>
            </ul>
          </b-row>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import { USER } from '@/store/namespaces.types';
import { LOGIN } from '@/store/actions.types';
import { GET_ERRORS } from '@/store/getters.types';

export default {

  name: 'TheLoginView',

  data: () => ({
    form: {
      username: '',
      password: '',
    },
    modalShow: false,
  }),

  computed: {
    ...mapGetters({
      errors: `${GET_ERRORS}`,
    }),
  },

  methods: {
    login() {
      this.$store.dispatch(`${USER}${LOGIN}`, this.form).then((username) => {
        this.$bvModal.msgBoxOk(`Welcome ${username}!`)
          .then(() => {
            this.$router.go(-1);
          });
      });
    },
  },
};

</script>
