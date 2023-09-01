import api from "@/services/axios";

const CommonService = {
  async getSignedUrl(payload) {
    return api.post("/upload/get_signed_url/", payload);
  }
};

export default CommonService;
