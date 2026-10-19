# Lernplattform (quint-games.de/hefte): Node + Chromium fuer den PDF-Export
FROM node:22-bookworm-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends chromium fonts-dejavu-core ca-certificates \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev --no-audit --no-fund || npm install --omit=dev --no-audit --no-fund
COPY server.mjs ./
COPY public ./public
# Archivo auch systemweit (falls Chromium sie ausserhalb der Seite braucht)
RUN mkdir -p /usr/share/fonts/truetype/archivo && cp public/assets/fonts/*.woff2 /usr/share/fonts/truetype/archivo/ && fc-cache -f >/dev/null 2>&1 || true
RUN mkdir -p /app/data && chown node:node /app/data
ENV NODE_ENV=production PORT=8080 BASE=/hefte CHROMIUM=/usr/bin/chromium
USER node
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD node -e "fetch('http://127.0.0.1:8080/hefte/healthz').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"
CMD ["node", "server.mjs"]
