import Toastify from "./Toastify.js";



axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';

const apiClient = axios.create({
  withCredentials: true, // This is the default
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(config => {
  return config;
});
apiClient.interceptors.response.use(
  response => response.data,
  error => {
    const { reason } = error.response.data;
    if (reason) {
      Toastify(reason).showToast();
    }
  },
);

export default apiClient;
