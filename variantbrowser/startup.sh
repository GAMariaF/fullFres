#! /bin/bash
# Script the docker container uses to start the variantbrowser processes.

cd /vb/frontend && pm2 start "npx http-server dist/ -p ${PORTFRONTEND} --proxy http://0.0.0.0:${PORTFRONTEND}?" --name frontend

cd /vb/ && vb-runbackend
