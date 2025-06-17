// utils/api.js
import axios from 'axios';

const API_BASE = '/agent';

export function fetchIntent(query) {
  return axios.post(`${API_BASE}/intent`, { query }).then(res => res.data);
}

export function fetchService(service_id) {
  return axios.post(`${API_BASE}/scrape`, { service_id }).then(res => res.data);
}

export function fetchAutoFill(form_url, user_profile) {
  return axios.post(`${API_BASE}/auto_fill`, { form_url, user_profile }).then(res => res.data);
}
