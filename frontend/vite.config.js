import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// reroutes React's API calls for /api and /static to fetch data from the Flask backend running on port 5000
// allowing the frontend to interact with the backend without CORS issues during development
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/static': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
})
