export function loginWithGoogle(nextPath = "/") {
  const params = new URLSearchParams({ next: nextPath });
  window.location.assign(`/api/auth/google/login/?${params}`);
}
