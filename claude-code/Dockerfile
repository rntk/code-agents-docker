FROM node:24-slim

WORKDIR /app

RUN npm install -g @anthropic-ai/claude-code

# Change ownership of app directory to node user
RUN chown -R node:node /app
RUN mkdir -p /home/node/.claude && \
  chown -R node:node /home/node/.claude

# Switch to node user
USER node

ENTRYPOINT ["claude"]
