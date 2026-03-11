.PHONY: build-all build run clean

# Build all Docker images
build-all:
	@for dir in agents/*/; do \
		if [ -f "$$dir/Dockerfile" ]; then \
			image_name=$$(basename $$dir); \
			echo "Building $$image_name..."; \
			docker build --no-cache -t $$image_name $$dir; \
		fi; \
	done

# Build a specific agent image (usage: make build AGENT=junie-cli)
build:
	@if [ -z "$(AGENT)" ]; then \
		echo "Usage: make build AGENT=<agent-name>"; \
		exit 1; \
	fi; \
	if [ ! -d "agents/$(AGENT)" ]; then \
		echo "Agent $(AGENT) not found in agents/"; \
		exit 1; \
	fi; \
	if [ ! -f "agents/$(AGENT)/Dockerfile" ]; then \
		echo "Dockerfile not found in agents/$(AGENT)/"; \
		exit 1; \
	fi; \
	docker build --no-cache -t $(AGENT) agents/$(AGENT)

# Run a specific agent image (usage: make run AGENT=junie-cli)
run:
	@if [ "$(AGENT)" = "junie-cli" ]; then \
		sudo docker run --rm -it -v "$(shell pwd):/app" -v "$(HOME)/.junie:/home/ubuntu/.junie" -e JUNIE_API_KEY junie-cli:latest --brave; \
	else \
		./agent.sh run; \
	fi

# Clean up dangling images
clean:
	docker image prune -f
