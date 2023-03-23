#! /bin/bash
cd /fullFres/frontend && pm2 start "npx http-server dist/ --proxy http://localhost:8081?" --name frontend
cd /fullFres && python3 run_backend_server.py