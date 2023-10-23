#!/bin/bash

docker run \
	-it \
	-v "/illumina/analysis/dev/2023/sigvla/fullFres_dev/db:/db" \
	-v "/illumina/analysis/dev/2023/sigvla/fullFres_dev/variantbrowser:/illumina/analysis/dev/2023/sigvla/fullFres_dev/variantbrowser" \
	--network host \
    --rm \
    -e PORTFRONTEND=8082 \
	vbtest:test1 \
    /bin/bash
 
