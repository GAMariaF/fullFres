#! /bin/bash

cd /fullFres/frontend && pm2 start "npx http-server dist/ -p ${PORTFRONTEND} --proxy http://localhost:${PORTFRONTEND}?" --name frontend
cd /fullFres && python3 run_backend_server.py