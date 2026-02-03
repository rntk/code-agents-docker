FROM node:24-slim

# Pin Gemini CLI version for reproducibility
ARG GEMINI_VERSION=latest
RUN npm install -g "@google/gemini-cli@${GEMINI_VERSION}"

WORKDIR /app

# Switch to non-root user for security
USER node

CMD ["gemini"]
