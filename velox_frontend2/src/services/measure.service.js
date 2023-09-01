import api from "@/services/axios";
import moment from "moment";

const MeasureService = {
  async fetchHorseMeasures(payload) {
    let response = await api.get(`/horses/${payload.id}/`);

    return response.data.measures;
  },
  async fetchHorseImageMeasures(payload) {
    let response = await api.get(`/horses/${payload.id}/`);

    return response.data.image_measurements;
  },
  async fetchMeasures(payload) {
    return api.get("/measures/");
  },
  async createMeasure(payload) {
    payload.date_of_measure = moment
      .utc(payload.date_of_measure)
      .format("YYYY-MM-DD");
    console.log("createMeasure", payload);

    return api.post("/measures/", payload);
  },
  async updateMeasure(payload) {
    if (payload.date_of_measure) {
      payload.date_of_measure = moment
        .utc(payload.date_of_measure)
        .format("YYYY-MM-DD");
    }
    console.log("updateMeasure", payload);

    return api.patch(`/measures/${payload.id}/`, payload);
  },
  async deleteMeasure(payload) {
    return api.delete(`/measures/${payload.id}/`);
  },
  async deleteImageMeasure(payload) {
    return api.delete(`/image-measurements/${payload.id}/`);
  },
  async createImageMeasure(payload) {
    payload.date_of_measure = moment
      .utc(payload.date_of_measure)
      .format("YYYY-MM-DD");

    console.log("createImageMeasure.payload:", payload);

    return api.post("/image-measurements/", payload);
  },
  async updateImageMeasure(payload) {
    payload.date_of_measure = moment
      .utc(payload.date_of_measure)
      .format("YYYY-MM-DD");

    console.log("updateImageMeasure", payload);

    return api.patch(`/image-measurements/${payload.id}/`, payload);
  },

  async measureScore(payload)
  {
    return api.post(`/measures/${payload}/score/`, payload)
  }
};

export default MeasureService;
