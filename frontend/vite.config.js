import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    // material-tailwind tries to deduplicate react libraries
    // this prevents it from happening
    dedupe: ["react", "react-dom"],
  },
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
