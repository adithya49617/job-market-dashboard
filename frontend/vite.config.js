import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3002,
    proxy: {
      '/analytics': 'http://localhost:7861',
      '/health': 'http://localhost:7861',
    }
  }
})
