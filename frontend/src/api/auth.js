import { BACKEND_URL } from "../utils/constants.js";
import axios from "axios";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.withCredentials = true;

export function loginWithGoogle() {
  window.location.assign("/api/auth/google/login/");
}

export async function registerOrganizationName(name) {
  const { data } = await axios.post(`${BACKEND_URL}/auth/organization/register/`, {
    name,
  });
  return data;
}

export function registerOrgWithGoogle() {
  window.location.assign("/api/auth/organization/register/");
}

export function getErrorMessage(error) {
  const data = error?.response?.data;
  if (data?.name?.length) return data.name[0];
  if (data?.non_field_errors?.length) return data.non_field_errors[0];
  if (typeof data?.detail === "string") return data.detail;
  return "Something went wrong. Please try again.";
}

export function getNewCsrf() {
  return axios(`${BACKEND_URL}/auth/csrf`);
}

export async function getUserData() {
  try {
    const { data } = await axios(`${BACKEND_URL}/auth/me/`);
    return data;
  } catch (error) {
    if (error.response?.status === 403) {
      return null;
    }
    throw error;
  }
}
