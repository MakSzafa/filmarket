import axios from "axios";

const state = {
  isAuthenticated: false,
  authError: false,
};

const getters = {};

const mutations = {
  login(state, payload) {
    localStorage.setItem("accessToken", payload.access);
    localStorage.setItem("refreshToken", payload.refresh);
    localStorage.setItem("id", payload.id);
    axios.defaults.headers.common["Authorization"] = "Bearer " + payload.access;
    state.isAuthenticated = true;
  },
  logout(state) {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("id");
    axios.defaults.headers.common["Authorization"] = "";
    state.isAuthenticated = false;
  },
  setIsAuthenticated(state, bool) {
    state.isAuthenticated = bool;
  },
  setAuthError(state, bool) {
    state.authError = bool;
  },
};

const actions = {
  async refreshAccessToken(context) {
    if (localStorage.getItem("refreshToken")) {
      try {
        const payload = {
          refresh: localStorage.getItem("refreshToken"),
        };
        const response = await axios.post("/api/token/refresh/", payload);
        localStorage.setItem("accessToken", response.data.access);
        axios.defaults.headers.common["Authorization"] =
          "Bearer " + response.data.access;
        context.commit("setIsAuthenticated", true);
        context.commit("setAuthError", false);
      } catch (e) {
        console.log(e);
        axios.defaults.headers.common["Authorization"] = "";
        context.commit("setIsAuthenticated", false);
        context.commit("setAuthError", true);
      }
    } else {
      axios.defaults.headers.common["Authorization"] = "";
      context.commit("setIsAuthenticated", false);
      context.commit("setAuthError", true);
    }
  },
};

export default {
  state,
  getters,
  mutations,
  actions,
};
