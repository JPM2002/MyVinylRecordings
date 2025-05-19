import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": "http://localhost:5000",
      "/cover": "http://localhost:5000",
      "/audio": "http://localhost:5000",
    },
  },
});
