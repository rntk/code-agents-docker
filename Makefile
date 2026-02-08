.PHONY: build-all run clean

# Build all Docker images
build-all:
	@for dir in */; do \
		if [ -f "$$dir/Dockerfile" ]; then \
			image_name=$$(basename $$dir); \
			echo "Building $$image_name..."; \
			docker build --no-cache -t $$image_name $$dir; \
		fi; \
	done

# Run a specific CLI (usage: make run CLI=claude-code)
run:
	@if [ -z "$(CLI)" ]; then \
		echo "Usage: make run CLI=<cli-name>"; \
		exit 1; \
	fi; \
	if [ ! -d "$(CLI)" ]; then \
		echo "CLI $(CLI) not found"; \
		exit 1; \
	fi; \
	docker run --rm -it -v $$(pwd):/app $(CLI)

# Clean up dangling images
clean:
	docker image prune -f
