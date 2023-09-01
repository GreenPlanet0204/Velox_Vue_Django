import Vue from 'vue';
import Vuex from 'vuex';
import {BootstrapVue, IconsPlugin} from 'bootstrap-vue';

// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import "vue-select/dist/vue-select.css";

import UserLogin from "./components/UserLogin";
import MeasureForm from "./components/MeasureForm";
import VueRouter from "vue-router";
import vSelect from "vue-select";

import axios from "axios";
import MeasurePage from "./pages/MeasurePage";

Vue.config.productionTip = false;
Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.use(VueRouter);
Vue.use(Vuex);

Vue.component("v-select", vSelect);


axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

const store = new Vuex.Store({
  state: {
    isLoggedIn: localStorage.getItem('auth') || null,
  },
  mutations: {
    updateLocalStorage(state, isLoggedIn) {
      localStorage.setItem('auth', isLoggedIn);
      state.isLoggedIn = isLoggedIn;
    }
  },
  actions: {
    auth(context, flag) {
      context.commit('updateLocalStorage', flag);
    },
  }
});

const requireAuthenticated = (to, from, next) => {
  if (!store.state.isLoggedIn) {
    next('/login/');
  } else {
    next();
  }

};


const routes = [
  {path: '/measures/:id/', component: MeasurePage},
  {path: '/measures', component: MeasureForm},

];

const router = new VueRouter({
  mode: 'history',
  routes: routes
});

new Vue({
  router,
  store,
  template: `
    <div>
    <b-toaster name="message"></b-toaster>

    <router-view></router-view>
    </div>
  `,
  // components: {Menux},
}).$mount("#app");

