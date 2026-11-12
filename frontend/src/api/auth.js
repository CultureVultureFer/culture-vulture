import { BACKEND_URL } from "../utils/constants.js";
import axios from "axios";

export function loginWithGoogle() {
  window.location.assign("/api/auth/google/login/");
}

export function registerOrgWithGoogle(orgName) {
  const params = new URLSearchParams({ org_name: orgName });
  window.location.assign(`/api/auth/google/login/?${params}`);
}

export function getNewCsrf() {
  return axios(`${BACKEND_URL}/auth/csrf`);
}

export async function getUserData() {
  try {
    const { data } = await axios(`${BACKEND_URL}/auth/me/`);
    return data;
  } catch (error) {
    if (error.response?.status === 401) {
      return null;
    }
    throw error;
  }
}
