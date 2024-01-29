#!/bin/bash
# Script for starting the variantbrowser docker.
docker run \
	-it \
	-v "./db:/vb/db" \
	-v "./import:/vb/import" \
	--network host \
    -e PORTFRONTEND=8082 \
	variantbrowser:test-version-upgrade \
    /bin/bash
 
 # To enter docker:
 # docker container ls -> get id
 # Run: docker exec -it [id] bash
