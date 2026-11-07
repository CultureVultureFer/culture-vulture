import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      // This will need to be setup using something like Caddy in prod...
      "/api": {
        target: "http://localhost:8000",
        // Needed for CSRF
        changeOrigin: false,
      },
    },
  },
});
