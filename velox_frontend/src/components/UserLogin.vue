<!--<template>-->
<!--  <div>-->
<!--    <b-card title="Login">-->
<!--      <b-card-body>-->
<!--        <b-form-group label="Email" label-for="username">-->
<!--          <b-form-input id="username" v-model="username" required></b-form-input>-->
<!--        </b-form-group>-->
<!--        <b-form-group label="Password" label-for="password">-->
<!--          <b-form-input id="password" type="password" v-model="password" required></b-form-input>-->
<!--        </b-form-group>-->
<!--        <b-button @click="login" variant="outline-primary">Login</b-button>-->
<!--      </b-card-body>-->
<!--    </b-card>-->
<!--  </div>-->
<!--</template>-->

<!--<script>-->
<!--import axios from "axios";-->

<!--import {usersAPIUrl} from "../utils/apis";-->

<!--export default {-->
<!--  name: "UserLogin",-->
<!--  data() {-->
<!--    return {-->
<!--      username: "",-->
<!--      password: ""-->
<!--    }-->
<!--  },-->
<!--  methods: {-->
<!--    login() {-->
<!--      const fullUrl = `${usersAPIUrl}login/`-->
<!--      axios.post(fullUrl, {'username': this.username, password: this.password}).then(resp => {-->
<!--        this.$store.dispatch('auth', true);-->
<!--        this.password = "";-->
<!--        this.username = "";-->
<!--        this.$router.replace('/');-->
<!--      })-->
<!--        .catch(error => {-->
<!--          console.log(error);-->
<!--          this.$store.dispatch('auth', false);-->
<!--        })-->
<!--    }-->
<!--  }-->
<!--}-->
<!--</script>-->

<!--<style scoped>-->

<!--</style>-->
