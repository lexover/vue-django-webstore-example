<template>
  <b-container>
    <b-row>
      <b-col md=12 class="pt-5">
        <h3 class="text-center">Pharmative simple webstore project</h3>
      </b-col>
    </b-row>
    <b-row class='p-5'>
      <b-col md=12>
        <article>
          <h4>What is it?</h4>
          <p> 
            This is a fully working study project of an online store, including both the frontend and backend. 
            In addition, everything is packed in a Docker container.
          </p>
          <h4>How is it built?</h4>
          <p>
            The design of the <a href="https://colorlib.com">Colorlib</a> was used as the appearance of the online store. 
            <a href="https://vuejs.org/">Vue.js 2</a> and <a href="https://bootstrap-vue.org">Bootstrap Vue</a> was chosen 
            for building the frontend. <a href="https://www.django-rest-framework.org/">Django REST Framework</a>
            used for backend. 
            Authorization is implemented using JSON Web Tokens for which used 
            <a href="https://github.com/SimpleJWT/django-rest-framework-simplejwt">Simple JWT</a> library. 
            A <a href="https://github.com/axios/axios">Axios</a> is used for interaction between the frontend and the backend.
            All this is collected into <a href="https://www.docker.com/">Docker</a> container using 
            <a href="https://github.com/unbit/uwsgi">uWSGI</a>.
          </p>
          <h4>Where can I download source code?</h4>
          <p>
            Source code is available on <a href="#">Git Hub</a>. Code licensed MIT.
          </p>
        </article>
      </b-col>
    </b-row>
  </b-container>
</template>

<style scoped>
  article {
    font-size: 1.2em;
  }
</style>