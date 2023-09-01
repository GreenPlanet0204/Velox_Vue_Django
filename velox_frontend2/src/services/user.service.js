import api from "@/services/axios";
import moment from "moment";

const UserService = {
  async fetchUser(id) {
    return api.get(`/users/${id}/`);
  },

  async addUser(payload) {
    return api.post("/users/", JSON.stringify(payload));
  },

  async updateUser(payload) {
    return api.put(`/users/${payload.id}/`, JSON.stringify(payload));
  },
  async deleteUser(payload) {
    return api.delete(`/users/${payload.id}/`);
  },

  async fetchUsers(payload) {
    let url = "/users/";

    let params = [];

    for (const property in payload) {
      params.push(`${property}=${payload[property]}`);
    }

    if (params.length) url = url + "?" + params.join("&");

    console.log("fetchUsers.url", url);

    return api.get(url);
  },
  login(payload) {
    return api.post(`/users/login/`, payload);
  },
  logout(payload) {
    return api.post(`/users/logout/`, payload);
  },

  async addCountry(payload) {
    return api.post("/country-weights/", JSON.stringify(payload));
  },

  async fetchcountyweights(payload) {

    let url = "/country-weights/";
    
    if(payload.start_country) url = url + payload.start_country + '/';
    console.log("fetchcountryweight.url", url);
    return api.get(url);
  },

  async updateCountry(payload) {
    return api.put(`/country-weights/${payload.starts_country}/`, JSON.stringify(payload));
  },

  async fetchstartcountry(payload) {
    let url = "/country-weights/";

    console.log("fetchcountryweight.url", url);

    return api.get(url);
  },
};

export default UserService;
