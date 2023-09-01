<template>
  <div>
    <h1>Users</h1>
    <b-button v-b-modal.user-creation-modal>Create User</b-button>
    <b-table :items="users" :fields="fields"></b-table>

    <b-modal id="user-creation-modal" @ok="createUser">
      <template #modal-ok>
        Add user
      </template>
      <b-form-group label="First Name" label-for="first-name">
        <b-form-input id="first-name" v-model="c.first_name" trim></b-form-input>
      </b-form-group>
      <b-form-group label="Last name" label-for="last-name">
        <b-form-input id="last-name" v-model="c.last_name" trim></b-form-input>
      </b-form-group>
      <b-form-group label="Email" label-for="email">
        <b-form-input v-model="c.email" trim></b-form-input>
      </b-form-group>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";

const usersApiUrl = '/cmmc/api/users/'
export default {
  name: "Users",
  data() {
    return {
      users: [],
      c: {
        first_name: "",
        last_name: "",
        email: ""
      },
      fields: [
        {key: 'first_name'},
        {key: 'last_name'},
        {key: 'email'}
      ]
    }
  },
  methods: {
    getUsers() {
      axios.get(usersApiUrl).then(resp => {
        this.users = resp.data;
      }).catch(error => {
        if (error.response) {
          this.$bvToast.toast(`${error.response.data.detail}`, {
            title: 'Error',
            variant: 'danger'
          })
        }
      })
    },
    createUser() {
      axios.post(usersApiUrl, this.c).then(resp => {
        this.c = {
          first_name: "",
          last_name: "",
          email: ""
        }
        this.$bvToast.toast(`Created successfully`, {
          title: 'User'
        })
      }).catch(error => {
        if (error.response) {
          this.$bvToast.toast(`${error.response.data.detail}`, {
            title: 'Error',
            variant: 'danger'
          })
        }
      })
      this.getUsers();
    }
  },
  mounted() {
    this.getUsers();
  }
}
</script>

<style scoped>

</style>
