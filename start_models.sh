#!/usr/bin/env bash

docker pull epigramai/model-server:light &&
docker run --name iv4 -p 9000:9000 -d -v $(pwd)/models/:/models/ epigramai/model-server:light --port=9000 --model_name=incv4 --model_base_path=/models/incv4_1536/