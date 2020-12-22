

### Theme

https://jamstackthemes.dev/theme/11ty-starter-boilerplate/

```bash
cd personal_finance_blog
git clone --depth=1 https://github.com/ixartz/Eleventy-Starter-Boilerplate.git site
```

## Docker 

Source of base image:

> https://hub.docker.com/r/femtopixel/eleventy?ref=login

Base os: Alpine linux



##### Build container

```bash
cd personal_finance_blog
docker build . -t eleventy
```

##### Run container

```bash
cd personal_finance_blog
docker run --rm -v /home/xander/Google\ Drive/Hobby/personal_finance_blog/site/:/app --name eleventy: -p 8080:8080 eleventy:latest --serve 
```

##### Enter container

```
docker exec -it eleventy bash
yarn build
```



##### Open website

```bash
http://localhost:8080
```



### About the JAM stack

https://snipcart.com/blog/jamstack



