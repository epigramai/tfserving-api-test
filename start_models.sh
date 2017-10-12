#!/usr/bin/env bash

docker pull epigramai/model-server:light &&
#docker run --name iv4 -p 9000:9000 -d -v $(pwd)/models/:/models/ epigramai/model-server:light --port=9000 --model_name=incv4 --model_base_path=/models/incv4_1536/ &&
docker run --name iv3 -p 9000:9000 -d -v $(pwd)/models/:/models/ epigramai/model-server:light --port=9000 --model_name=incv3 --model_base_path=/models/incv3_bottleneck &&
docker run --name fash -p 9001:9000 -d -v $(pwd)/models/:/models/ epigramai/model-server:light --port=9000 --model_name=fashion --model_base_path=/models/final_layers