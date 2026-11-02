export function isEmail(email) {
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email.match(pattern)) return "Please provide a valid email";
}

export function passwordStrongEnough(password) {
  const uppercase = /[A-Z]/.test(password);
  const lowercase = /[a-z]/.test(password);
  const special = /[@$!%*#?&]/.test(password);
  const digit = /\d/.test(password);
  const long = password.length >= 8;
  if (!long) return "Password must be at least 8 characters long";
  if (!uppercase) return "Password must contain at least one uppercase letter";
  if (!lowercase) return "Password must contain at least one lowercase letter";
  if (!special)
    return "Password must contain at least one speccial letter (@,$,!...)";
  if (!digit) return "Password must contain at least one number";
}

export function passwordMatch(passwordrepeated, { password }) {
  if (passwordrepeated != password) {
    return "Passwords must match";
  }
}
