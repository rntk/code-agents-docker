.PHONY: build-all build clean

# Build all Docker images
build-all:
	@for dir in agents/*/; do \
		if [ -f "$$dir/Dockerfile" ]; then \
			image_name=$$(basename $$dir); \
			echo "Building $$image_name..."; \
			docker build --no-cache -t $$image_name $$dir; \
		fi; \
	done

# Build a specific agent image (usage: make build AGENT=claude-code)
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

# Clean up dangling images
clean:
	docker image prune -f
