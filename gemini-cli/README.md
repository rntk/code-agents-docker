# Gemini CLI (Dockerized)

This directory contains a Docker setup for running [Google's Gemini CLI](https://github.com/google-gemini/gemini-cli).

## Prerequisites

- Docker installed on your system
- Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/)

## Build

```bash
docker build -t gemini-cli .
```

## Run

```bash
# Set your API key as an environment variable
export GEMINI_API_KEY="YOUR_API_KEY"

# Run the container with volume mount for working directory
docker run --rm -it -v $(pwd):/app -e GEMINI_API_KEY=$GEMINI_API_KEY gemini-cli

docker run --rm -it -v $(pwd):/app -v $HOME/.gemini:/home/node/.gemini gemini-cli
```

## Configuration

- The container runs as a non-root user for security.
- Mount your current directory to `/app` to work with local files.
- Pass API keys via environment variables to avoid storing them in the image.

## Troubleshooting

- **Permission errors**: Ensure the mounted volume allows write access.
- **API key issues**: Verify your key is valid and exported correctly.
- **Build failures**: Check Docker is running and you have internet access for npm installs.
