build:
	docker build -t llm-explore .

# Bind mounts local repo to allow fluid dev
attach-dev:
	docker build \
	--build-arg entry_workdir=/opt/dev-workspace \
	-t llm-explore . \
	&& docker run \
	-v $(shell pwd):/opt/dev-workspace \
	-it --rm \
	--name llm-explore llm-explore /bin/bash