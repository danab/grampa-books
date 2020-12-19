import Vue from "vue";
import axios from "axios";

axios.defaults.baseURL = process.env.DEV ? "http://localhost:8000" : "/api";

Vue.prototype.$axios = axios;
