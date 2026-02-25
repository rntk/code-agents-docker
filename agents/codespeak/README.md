# CodeSpeak Docker

This repository provides a Dockerized version of [CodeSpeak](https://codespeak.io), an AI-powered coding tool. Running CodeSpeak in Docker ensures a consistent environment and avoids the need to install dependencies like `uv` directly on your host machine.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your machine.
- An **Anthropic API Key**. You can get one [here](https://platform.claude.com/settings/keys).

## Building the Image

Build the Docker image locally:

```bash
docker build -t codespeak .
```

## Running CodeSpeak

Since CodeSpeak works on your project files, you need to mount your current directory into the container and provide your API key.

### Initialize a New Project

To run `codespeak init` in a new directory:

```bash
docker run -it --rm \
  -v "$(pwd):/app" \
  codespeak init
```

### Build a Project

To build the project specified in your `spec/` directory:

```bash
docker run -it --rm \
  -v "$(pwd):/app" \
  -e ANTHROPIC_API_KEY=your_api_key_here \
  codespeak build
```

### Making Changes

To request changes:

```bash
docker run -it --rm \
  -v "$(pwd):/app" \
  -e ANTHROPIC_API_KEY=your_api_key_here \
  codespeak change -m "Your change request here"
```

## Authentication Flow (Login)

If you need to use `codespeak login`, the tool will start a local callback server listening on `localhost:8080`. Since this is inside a container, it won't be directly accessible from your host browser.

We've included a proxy script `auth_proxy.py` that listens on `0.0.0.0:8081` and forwards requests to the local server.

### How to use the login flow:

1.  **Run the container with port 8081 exposed** and override the entrypoint to a shell:
    ```bash
    docker run -it --rm \
      -v "$(pwd):/app" \
      -p 8081:8081 \
      --entrypoint /bin/bash \
      codespeak
    ```

2.  **Inside the container**, start the proxy in the background:
    ```bash
    auth_proxy &
    ```

3.  **Run the login command**:
    ```bash
    codespeak login
    ```

4.  The tool will provide a URL to open in your browser. Open it, and once it redirects to `http://localhost:8080/callback...`, **change the port in your browser's address bar from 8080 to 8081**. The proxy will then forward the request to the tool inside the container.

---

## Tips

- **Alias**: For convenience, you can add an alias to your `.bashrc` or `.zshrc`:
  ```bash
  alias codespeak='docker run -it --rm -v "$(pwd):/app" -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY codespeak'
  ```
  Then you can just run `codespeak build`.
- **Git**: Since the container has `git` installed, it can handle the repository initialization performed by `codespeak init`.
- **Persisting Config**: If you use `codespeak login`, the credentials will be stored inside the container's `/home/codespeak` directory. To persist them, you might want to mount a volume to `/home/codespeak/.codespeak`. However, using `ANTHROPIC_API_KEY` is generally easier for Docker usage.
