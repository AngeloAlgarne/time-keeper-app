FROM node:21-alpine

WORKDIR /frontend

COPY package.json /frontend/
COPY src /frontend/

RUN npm install

EXPOSE 3000

CMD ["npm", "start"]