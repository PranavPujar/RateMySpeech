FROM --platform=linux/arm64 node:18.18.0

WORKDIR /frontend
COPY package*.json ./

RUN npm install --save-dev serve
RUN npm install
    
COPY public/ ./public
COPY src/ ./src

RUN npm run build

EXPOSE 3000

CMD ["npx", "serve", "-s", "build"] 
