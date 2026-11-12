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
  const errors = error?.response?.data?.errors;
  if (errors?.name?.length) return errors.name[0];
  if (errors?.__all__?.length) return errors.__all__[0];
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
    if (error.response?.status === 401) {
      return null;
    }
    throw error;
  }
}
