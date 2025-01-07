DOCKER_IMAGE = pyrtc_image
DOCKER_TAG = latest
DOCKERFILE = dockers/Dockerfile
CONTAINER_NAME = pyrtc_container
SHARE_DIR = $(shell pwd)/share
NETWORK_NAME ?= rtcnet
NETWORK_SUBNET ?= 192.168.2.0/24
NO_CACHE ?= false


network:
	@if [ -z `docker network ls --filter name=$(NETWORK_NAME) --format '{{.Name}}'` ]; then \
		echo "=> Creating network $(NETWORK_NAME): $(NETWORK_SUBNET)"; \
		docker network create --subnet $(NETWORK_SUBNET) $(NETWORK_NAME); \
	else \
		echo "=> Network $(NETWORK_NAME) $(NETWORK_SUBNET) already exists."; \
	fi

build:
	@if [ "$(NO_CACHE)" = "true" ]; then \
		echo "=> Building without cache"; \
		docker build -f $(DOCKERFILE) -t $(DOCKER_IMAGE):$(DOCKER_TAG) --no-cache .; \
	else \
		echo "=> Building with cache"; \
		docker build -f $(DOCKERFILE) -t $(DOCKER_IMAGE):$(DOCKER_TAG) .; \
	fi

setup: build network

run:
	docker run --rm --privileged -it \
	-v $(SHARE_DIR):/app/share \
	--name $(CONTAINER_NAME) \
	$(DOCKER_IMAGE):$(DOCKER_TAG)

clean:
	docker rmi $(DOCKER_IMAGE):$(DOCKER_TAG)
	docker network rm $(NETWORK_NAME)

shell:
	docker exec -it $(CONTAINER_NAME) /bin/bash
