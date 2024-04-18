FROM node:latest

WORKDIR /usr/src/app

COPY . .

RUN yarn install

RUN mv src/config.js.example src/config.js
RUN sed -i "s/'CLIENT_ID'/process.env.CLIENT_ID/g" src/config.js \
    && sed -i "s/'CLIENT_SECRET'/process.env.CLIENT_SECRET/g" src/config.js

EXPOSE 3000

CMD ["yarn", "start"]
