import { BACKEND_URL } from "../utils/constants.js";
import axios from "axios";

export function loginWithGoogle(nextPath = "/") {
  const params = new URLSearchParams({ next: nextPath });
  window.location.assign(`/api/auth/google/login/?${params}`);
}

export function getNewCsrf() {
  return axios(`${BACKEND_URL}/auth/csrf`);
}
