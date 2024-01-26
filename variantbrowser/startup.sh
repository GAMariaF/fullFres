#! /bin/bash
# Script the docker container uses to start the variantbrowser processes.

cd /vb/variantbrowser/frontend && pm2 start "npx http-server dist/ -p ${PORTFRONTEND} --proxy http://localhost:${PORTFRONTEND}?" --name frontend
cd /vb/variantbrowser && python3 run_backend_server.py
