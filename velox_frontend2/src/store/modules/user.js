import { currentUser, isAuthGuardActive } from "../../constants/config";
import userServices from "../../services/user.service";
import { setCurrentUser, getCurrentUser } from "../../utils";

export default {
  state: {
    currentUser: isAuthGuardActive ? getCurrentUser() : currentUser,
    loginError: null,
    processing: false,
    forgotMailSuccess: null,
    resetPasswordSuccess: null
  },
  getters: {
    currentUser: state => state.currentUser,
    processing: state => state.processing,
    loginError: state => state.loginError,
    forgotMailSuccess: state => state.forgotMailSuccess,
    resetPasswordSuccess: state => state.resetPasswordSuccess
  },
  mutations: {
    setUser(state, payload) {
      state.currentUser = payload;
      state.processing = false;
      state.loginError = null;
    },
    setLogout(state) {
      state.currentUser = null;
      state.processing = false;
      state.loginError = null;
    },
    setProcessing(state, payload) {
      state.processing = payload;
      state.loginError = null;
    },
    setError(state, payload) {
      let message = "Undefined error";
      let errorObject = JSON.parse(payload);

      if (Object.keys(errorObject).length) {
        message = errorObject[Object.keys(errorObject)[0]];
      }

      state.loginError = message;
      state.currentUser = null;
      state.processing = false;
    },
    setForgotMailSuccess(state) {
      state.loginError = null;
      state.currentUser = null;
      state.processing = false;
      state.forgotMailSuccess = true;
    },
    setResetPasswordSuccess(state) {
      state.loginError = null;
      state.currentUser = null;
      state.processing = false;
      state.resetPasswordSuccess = true;
    },
    clearError(state) {
      state.loginError = null;
    }
  },
  actions: {
    async login({ commit }, payload) {
      try {
        commit("clearError");
        commit("setProcessing", true);

        console.log("store.user.login", payload);
        let res = await userServices.login(payload);
        console.log("store.user.login.response", res);

        let user = res.data;
        user.title = user.email;
        user.id = user.user_id;
        //const item = { uid: "111-222-333-444", ...currentUser };
        setCurrentUser(user);
        commit("setUser", user);
      } catch (err) {
        console.error("login.error:", err.response);
        setCurrentUser(null);

        commit("setError", err.response.request.responseText);
        // throw err.response.request.responseText;
      }
    },
    async logout({ commit }, payload) {
      console.log("store.user.logout", payload);
      try {
        let res = await userServices.logout(payload);

        setCurrentUser(null);
        commit("setLogout");
      } catch (err) {
        setCurrentUser(null);

        commit("setError", err.response.request.responseText);
        throw err.response.request.responseText;
      }
    },
    async refreshToken() {
      console.log("store.user.refreshToken");
    }
  }
};
