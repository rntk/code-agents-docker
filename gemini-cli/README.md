# Gemini CLI (Dockerized)

This directory contains a Docker setup for running [Google's Gemini CLI](https://github.com/google-gemini/gemini-cli).

## Build

```bash
sudo docker build ./ -t gemini-cli -f Dockerfile --no-cache
```

## Run

```bash
# Set your API key
export GEMINI_API_KEY="YOUR_API_KEY"

# Run the container
sudo docker run --rm -it -v $(pwd):/app -e GEMINI_API_KEY=$GEMINI_API_KEY --name gemini-cli gemini-cli
```

## Prerequisites

- Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/)
