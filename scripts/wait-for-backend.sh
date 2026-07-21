#!/usr/bin/env sh

# Wait for backend health endpoint to be available
BACKEND_URL=${BACKEND_URL:-http://backend:8000/health}

echo "Waiting for backend at $BACKEND_URL"
until curl -sf "$BACKEND_URL" > /dev/null; do
  printf '.'
  sleep 1
done

echo "\nBackend is up"
exit 0
