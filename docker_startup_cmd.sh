#! /bin/bash
cd /fullFres/frontend && pm2 start "npx http-server dist/ -p 8080 --proxy http://localhost:8080?" --name frontend
cd /fullFres && python3 run_backend_server.py