import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    // F-001: sve što ide na /api/... Vite prosljeđuje Djangu (port 8000).
    // Preglednik tako misli da su frontend i backend na istoj adresi
    // (localhost:5173), pa se kolačić sesije šalje sam od sebe: nema CORS-a
    // ni credentials: "include".
    // U fetch() zato UVIJEK pišite relativni URL ("/api/events/"), nikad
    // "http://localhost:8000/api/...", jer onda kolačići ne rade.
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        // false: Django vidi isti Host kao preglednik (localhost:5173), pa
        // CSRF provjera prolazi.
        changeOrigin: false,
      },
    },
  },
});
