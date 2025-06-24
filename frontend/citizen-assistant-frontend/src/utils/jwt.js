// src/utils/jwt.js
export function decodeJwt(token) {
  if (!token) return {};
  const payload = token.split('.')[1];
  return JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')));
}