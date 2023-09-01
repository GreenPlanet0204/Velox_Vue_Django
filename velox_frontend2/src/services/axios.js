import axios from "axios";
import { apiUrl } from "../constants/config";

console.log("apiUrl", apiUrl);

const axiosInstance = axios.create({
  baseURL: apiUrl,
  headers: {
    "Content-Type": "application/json",
  },
});

export default axiosInstance;
