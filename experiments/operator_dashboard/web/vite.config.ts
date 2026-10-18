import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
// Build only. The Python entrypoint owns same-origin API/static serving.
export default defineConfig({ plugins: [react()] });
