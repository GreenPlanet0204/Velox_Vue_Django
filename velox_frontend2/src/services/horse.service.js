import api from "@/services/axios";
import moment from "moment";

const HorseService = {
  async fetchHorse(id) {
    return api.get(`/horses/${id}/`);
  },

  async addHorse(payload) {
    payload.date_of_birth = moment
      .utc(payload.date_of_birth)
      .format("YYYY-MM-DD");
    console.log(JSON.stringify(payload));

    return api.post("/horses/", JSON.stringify(payload));
  },
  async updateHorse(payload) {
    if (payload.date_of_birth) {
      payload.date_of_birth = moment
        .utc(payload.date_of_birth)
        .format("YYYY-MM-DD");
    }
    if (payload.date_last_start) {
      payload.date_last_start = moment
        .utc(payload.date_last_start)
        .format("YYYY-MM-DD");
    }

    return api.patch(`/horses/${payload.id}/`, JSON.stringify(payload));
  },
  async deleteHorse(payload) {
    return api.delete(`/horses/${payload.id}/`);
  },

  async addDNAMarkers(payload) {
    return api.patch(`/horses/${payload.id}/`, JSON.stringify(payload));
  },
  async addBiomechanicsVideo(payload) {
    return true;
  },
  async fetchHorses(payload) {
    let url = "/horses/";

    let params = [];

    for (const property in payload) {
      if (property !== "name") params.push(`${property}=${payload[property]}`);
      else params.push("search=" + payload.name);
    }

    if (params.length) url = url + "?" + params.join("&");

    console.log("fetchHorses.url", url);
    return api.get(url);
  },

  async fetchHorsesCounts() {
    return api.get(`/horses/counts/`);
  },
  async fetchHorsesStates() {
    return api.get(`/horses/stats/`);
  }
};

export default HorseService;
