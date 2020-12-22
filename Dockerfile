FROM femtopixel/eleventy
RUN apk add bash

COPY ./site /app

RUN yarn install
