FROM node:18-alpine

WORKDIR /app

# Copiamos protos para que el gateway los cargue desde /app/protos
COPY ./protos /app/protos

# Dependencias
COPY ./gateway/package.json /app/package.json
RUN npm install --omit=dev

# Código
COPY ./gateway/index.js /app/index.js
COPY ./gateway/protoload.js /app/protoload.js

EXPOSE 3000
CMD ["node", "/app/index.js"]
