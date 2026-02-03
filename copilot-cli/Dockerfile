FROM node:24-slim

# Pin Copilot CLI version for reproducibility
ARG COPILOT_VERSION=latest
RUN npm install -g "@github/copilot@${COPILOT_VERSION}"

WORKDIR /app

# Change ownership of app directory to node user
RUN chown -R node:node /app
RUN mkdir -p /home/node/.copilot && \
  chown -R node:node /home/node/.copilot

# Switch to node user
USER node

ENTRYPOINT ["copilot"]