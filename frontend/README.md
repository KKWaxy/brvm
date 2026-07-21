SGI Frontend

A small React frontend scaffold for the BRVM SGI API.

Requirements
- Node.js 18+ and npm/yarn/pnpm OR Docker + Docker Compose

Quick start (local, Node installed)
1. cd frontend
2. npm install
3. VITE_API_URL=http://localhost:8000 npm run dev

Docker (no Node required locally)
- Development (hot reload):
  1. Ensure Docker is running
  2. VITE_API_URL=http://host.docker.internal:8000 docker compose up frontend_dev
  3. Open http://localhost:5173

- Production (build + nginx):
  1. docker compose build frontend
  2. docker compose up frontend
  3. Open http://localhost:8080

Notes
- The dev service maps the host backend to host.docker.internal. On Linux you may need to change VITE_API_URL to point to the host IP or the actual backend container name.
- The production image builds the static assets and serves them with Nginx.
- The frontend reads the backend base URL from VITE_API_URL at build/dev time.
