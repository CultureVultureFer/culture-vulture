// F-001: prijava i registracija (backend: backend/accounts/).
//
// Svi (korisnici i organizatori) se registriraju i prijavljuju SAMO preko
// Googlea. Nema obrasca s emailom i lozinkom.
//
//   Korisnik:     gumb "Prijava s Googleom" -> loginWithGoogle("/")
//                 Prva prijava automatski stvara račun.
//   Organizator:  1. loginWithGoogle("/register/organizer")
//                 2. na toj stranici obrazac s nazivom organizacije
//                    -> registerOrganizer({ name })
//
// Prijava se pamti u kolačiću sesije koji postavlja Django. React ne sprema
// nikakav token i ne treba ga slati: preglednik šalje kolačić sam.
//
// Primjer s react-query (kao u OrgRegister.jsx):
//
//   const mutation = useMutation({
//     mutationFn: registerOrganizer,          // prima {name}
//     onSuccess: (user) => navigate("/hello"),
//     onError: (err) => {                      // err je ApiError
//       for (const [field, messages] of Object.entries(err.errors)) {
//         setError(field, { message: messages[0] });   // react-hook-form
//       }
//     },
//   });

/** Greška s backenda. `errors` je {polje: [poruke]}, `__all__` za opće greške. */
export class ApiError extends Error {
  constructor(status, errors) {
    const first = Object.values(errors ?? {})[0]?.[0];
    super(first || `Request failed (${status})`);
    this.status = status;
    this.errors = errors ?? {};
  }
}

function getCookie(name) {
  const row = document.cookie.split("; ").find((r) => r.startsWith(`${name}=`));
  return row ? decodeURIComponent(row.split("=")[1]) : null;
}

/** Django za svaki POST traži CSRF token; dobije se jednom s ovog endpointa. */
async function ensureCsrf() {
  if (!getCookie("csrftoken")) {
    await fetch("/api/auth/csrf/");
  }
  return getCookie("csrftoken");
}

/**
 * Opći poziv API-ja. Koristite ga i za ostale dijelove aplikacije (događaji,
 * komentari...), jer sam dodaje CSRF token za POST/PUT/PATCH/DELETE.
 * Bez tog tokena Django vraća 403.
 */
export async function apiFetch(url, { method = "GET", body, headers = {} } = {}) {
  const init = { method, headers: { ...headers } };

  if (!["GET", "HEAD"].includes(method)) {
    init.headers["X-CSRFToken"] = await ensureCsrf();
  }
  if (body !== undefined) {
    init.headers["Content-Type"] = "application/json";
    init.body = JSON.stringify(body);
  }

  const response = await fetch(url, init);
  if (response.status === 204) return null;

  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new ApiError(response.status, data.errors);
  return data;
}

// --- Prijava i registracija ---------------------------------------------------

/**
 * Prijava (i registracija) Googleom, za sve korisnike.
 *
 * MORA biti puna navigacija, ne fetch(): korisnik treba vidjeti Googleovu
 * stranicu. Nakon prijave backend ga vraća na `nextPath`, a u slučaju
 * greške na /login?auth_error=<kod> (vidi GOOGLE_ERRORS).
 */
export function loginWithGoogle(nextPath = "/") {
  const params = new URLSearchParams({ next: nextPath });
  window.location.assign(`/api/auth/google/login/?${params}`);
}

/**
 * {name} -> organizator. Korisnik mora već biti prijavljen Googleom
 * (inače ApiError 401). Email i lozinka se ne šalju: email je s Googlea.
 */
export const registerOrganizer = ({ name }) =>
  apiFetch("/api/auth/register/organizer/", { method: "POST", body: { name } });

export const logout = () => apiFetch("/api/auth/logout/", { method: "POST" });

/** Trenutno prijavljeni korisnik ({id, username, email, role}) ili null. */
export async function getCurrentUser() {
  try {
    return await apiFetch("/api/auth/me/");
  } catch (err) {
    if (err instanceof ApiError && err.status === 401) return null;
    throw err;
  }
}

/** Poruke za ?auth_error= nakon Google prijave. */
export const GOOGLE_ERRORS = {
  cancelled: "Google sign-in was cancelled.",
  email_exists: "An account with this email already exists. Please contact an administrator.",
  email_not_verified: "Your Google email address is not verified.",
  account_disabled: "This account has been deactivated.",
  google_linked_to_other_account: "This Google account is already connected to another user.",
  other_google_already_linked: "Your account is already connected to a different Google account.",
  invalid_token: "Sign-in failed. Please try again.",
  oidc_error: "Sign-in failed. Please try again.",
};
