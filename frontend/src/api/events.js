import axios from "axios";
export async function getEvents() {
  return axios.get("/api/events/");
}
