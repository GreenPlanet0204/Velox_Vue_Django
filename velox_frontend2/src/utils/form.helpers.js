import Vue from "vue";

import BootstrapVue from "bootstrap-vue";
Vue.use(BootstrapVue);

let vm = new Vue();

export default {
  showConfirmation(message) {
    return vm.$bvModal.msgBoxConfirm(
      [vm.$createElement("div", { domProps: { innerHTML: message } })],
      {
        title: "Confirm action",
        size: "md",
        buttonSize: "md",
        okVariant: "danger",
        okTitle: "YES",
        cancelTitle: "NO",
        footerClass: "p-2",
        hideHeaderClose: false,
        centered: true
      }
    );
  },

  showInfo(message) {
    vm.$notify("info", "Info", message, {
      duration: 3000,
      permanent: false
    });
  },

  showError(message) {
    vm.$notify("error", "Error", message, {
      duration: 3000,
      permanent: false
    });
  },
  makeToastError(message) {
    return vm.$bvToast.toast(message, {
      title: "Error",
      variant: "danger",
      toaster: "b-toaster-bottom-right",
      autoHideDelay: 5000,
      solid: true
    });
  },
  resetObject(obj) {
    let resultObject = Object.assign({}, obj);
    for (let prop in resultObject) {
      resultObject[prop] = "";
    }

    return resultObject;
  }
};
