FROM femtopixel/eleventy
RUN apk add bash vim
#RUN apk add --no-cache autoconf libtool automake
#RUN apk --update add gcc make g++ zlib-dev

COPY ./site /app

RUN yarn install
