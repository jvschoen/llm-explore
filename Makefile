build:
	docker build -t llm-explore .

# Bind mounts local repo to allow fluid dev
attach-dev:
	docker build \
	--build-arg entry_workdir=/opt/dev-workspace \
	-t llm-explore . \
	&& docker run \
	-v $(shell pwd):/opt/dev-workspace \
	-p 8888:8888 \
	-it --rm \
	--name llm-explore llm-explore /bin/bash

jupyter-sever:
	jupyter lab \
	--ip=0.0.0.0 \
	--no-browser \
	--allow-root