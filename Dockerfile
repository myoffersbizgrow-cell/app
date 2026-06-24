FROM node:20-slim

# Java install karo
RUN apt-get update && apt-get install -y openjdk-17-jdk-headless

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

EXPOSE 10000
CMD ["node", "server.js"]
