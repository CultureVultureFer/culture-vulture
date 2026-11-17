import { BACKEND_URL } from "../utils/constants.js";
import axios from "axios";
import "./auth.js";

export function getCategories() {
    return axios.get(`${BACKEND_URL}/categories/`).then((res) => res.data);
}

export function getEvent(id) {
    return axios.get(`${BACKEND_URL}/events/${id}/`).then((res) => res.data);
}

export function createEvent(payload) {
    return axios.post(`${BACKEND_URL}/events/`, payload).then((res) => res.data);
}

export function updateEvent(id, payload) {
    return axios.patch(`${BACKEND_URL}/events/${id}/`, payload).then((res) => res.data);
}

export function deleteEvent(id) {
    return axios.delete(`${BACKEND_URL}/events/${id}/`);
}

