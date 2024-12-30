DOCKER_IMAGE = pyrtc_image
DOCKER_TAG = latest
DOCKERFILE = dockers/Dockerfile
CONTAINER_NAME = pyrtc_container
SHARE_DIR = $(shell pwd)/share

# Build Docker image
build:
	docker build -f $(DOCKERFILE) -t $(DOCKER_IMAGE):$(DOCKER_TAG) .
# docker run --rm \
# -v $(SHARE_DIR):/app/share \
# --name $(CONTAINER_NAME) \
# $(DOCKER_IMAGE):$(DOCKER_TAG) bash -c "cd ./build.sh"
build-no-cache:
	docker build -f $(DOCKERFILE) -t $(DOCKER_IMAGE):$(DOCKER_TAG) --no-cache .

# Run container and mount folder
run:
	docker run --rm --privileged -it \
	-v $(SHARE_DIR):/app/share \
	--name $(CONTAINER_NAME) \
	$(DOCKER_IMAGE):$(DOCKER_TAG)

# Clean Docker image
clean:
	docker rmi $(DOCKER_IMAGE):$(DOCKER_TAG)

# Enter running container
shell:
	docker exec -it $(CONTAINER_NAME) /bin/bash
