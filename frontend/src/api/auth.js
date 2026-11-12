import { BACKEND_URL } from "../utils/constants.js";
import axios from "axios";

export function loginWithGoogle(nextPath = "/") {
  const params = new URLSearchParams({ next: nextPath });
  window.location.assign(`/api/auth/google/login/?${params}`);
}

export function registerOrgWithGoogle(orgName, nextPath = "/") {
  const params = new URLSearchParams({ next: nextPath, org_name: orgName });
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
