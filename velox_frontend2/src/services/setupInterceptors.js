import axiosInstance from "./axios";
import { setCurrentUser, getCurrentUser } from "@/utils";

const setup = ({ store, router }) => {
  //axiosInstance.interceptors.response.use(response => response.data);

  axiosInstance.interceptors.request.use(
    config => {
      const currentUser = getCurrentUser();
      const token = currentUser ? currentUser.token : null;

      if (token) {
        config.headers.common.Authorization = `Token ${token}`;
      }

      return config;
    },
    error => Promise.reject(error)
  );

  const createAxiosResponseInterceptor = () => {
    const interceptor = axiosInstance.interceptors.response.use(
      response => response,
      async error => {
        // Reject promise if usual error
        if (error.response && error.response.status !== 401) {
          return Promise.reject(error);
        }
        let originalConfig = error.config;

        originalConfig = error.config;

        if (originalConfig.url !== "/auth/login" && error.response) {
          if (error.response.status === 401) {
            console.log("401.logout");
            await store.dispatch("user/logout");
            router.push({ name: "Login" });
            Promise.reject(err);

            /*            
            // Access Token has expired
            axiosInstance.interceptors.response.eject(interceptor);

            return store
              .dispatch("user/refreshToken")
              .then(response => {
                const newToken = response;

                originalConfig.headers.Authorization = `Bearer ${newToken}`;

                return axiosInstance(originalConfig);
              })
              .catch(async err => {
                await store.dispatch("user/logout");

                router.push({ name: "Login" });

                Promise.reject(err);
              })
              .finally(createAxiosResponseInterceptor);
              */
          }
        }

        return Promise.reject(error);
      }
    );
  };

  createAxiosResponseInterceptor();
};

export default setup;
