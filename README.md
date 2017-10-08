# tfserving-api-test

### main.py
This is the api with endpoints. When receiving a request, it sends the image to the correct model.
The models are hosted in separate docker containers.

### start_models.sh
Add tfserving models in models/ and add a new line to the startup script.

### Dockerfile
This file has instructions on how to build the api image. Move files into the docker image, install the requirements etc.

### docker-compose.yml
Use `docker stack deploy api -c docker-compose.yml` to deploy the stack. This will deploy the api
image and the models in separate docker services. The services are on the same virtual network and
can communicate with each other. 