<template>
  <b-container class="pb-5">
    <b-row class="py-5">
      <b-col md="12" class=" mb-5 mb-md-0">
        <h3 class="mb-3 text-black">Login form:</h3>
        <div class="p-3 p-lg-5 border">
          <b-row class="form-group">
            <b-col md="12">
              <label for="c_login" class="text-black">Login:</label>
              <b-input type="text"
                       id="c_login"
                       class="form-control"
                       v-model="form.username"
                       placeholder="E-mail or user name."/>
            </b-col>
          </b-row>
          <b-row class="form-group">
            <b-col md="12">
              <label for="c_password" class="text-black">Password:</label>
              <b-input type="password"
                       id="c_password"
                       class="form-control"
                       v-model="form.password"
                       placeholder="Password"/>
            </b-col>
          </b-row>
          <b-row>
            <b-col md="12" class="text-right">
              <b-button type="submit" variant="primary" class="mx-3 px-5" @click="login">
                Login
              </b-button>
              <b-button :to="{name: 'register'}" variant="outline-primary" class="px-5">
                Register
              </b-button>
            </b-col>
          </b-row>
          <b-row v-if="errors">
            <ul>
              <li v-for="(v, k) in errors" :key="k" class="text-danger">{{ v | error }} </li>
            </ul>
          </b-row>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { USER, LOGIN, GET_ERRORS } from '@/store/types';
import { mapGetters } from 'vuex';

export default {

  data: () => ({
    form: {
      username: '',
      password: '',
    },
    modalShow: false,
  }),

  methods: {
    login() {
      this.$store.dispatch(`${USER}${LOGIN}`, this.form).then(username => {
        this.$bvModal.msgBoxOk(`Welcome ${username}!`)
          .then(() => {
             this.$router.go(-1);
          })
      });
    },
  },

  computed: {
    ...mapGetters({
      errors: `${GET_ERRORS}`,
    }),
  },

};

</script>
