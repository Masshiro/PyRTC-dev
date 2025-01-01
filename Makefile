DOCKER_IMAGE = pyrtc_image
DOCKER_TAG = latest
DOCKERFILE = dockers/Dockerfile
CONTAINER_NAME = pyrtc_container
SHARE_DIR = $(shell pwd)/share


build:
	docker build -f $(DOCKERFILE) -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

build-no-cache:
	docker build -f $(DOCKERFILE) -t $(DOCKER_IMAGE):$(DOCKER_TAG) --no-cache .

run:
	docker run --rm --privileged -it \
	-v $(SHARE_DIR):/app/share \
	--name $(CONTAINER_NAME) \
	$(DOCKER_IMAGE):$(DOCKER_TAG)

clean:
	docker rmi $(DOCKER_IMAGE):$(DOCKER_TAG)

shell:
	docker exec -it $(CONTAINER_NAME) /bin/bash
