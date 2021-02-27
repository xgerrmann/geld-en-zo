# Run locally

In the terminal, do:

```
yarn serve
```

Then click on one of the links shown at the end of the output.

If yarn is not installed perform the installation steps below.

### Installation of dependencies

* Install npm and node.js

  * Source: https://github.com/nodejs/snap
    The 'channel' argument below indicates the node.js version

    ```
    sudo snap install node --classic --channel=15
    ```

* Install yarn

  ```
  npm install yarn
  ```

* Install dependencies (defined in `package.json`)

  ```
  yarn install
  ```

  

### Errors

* > Please verify that the package.json has a valid "main" entry

  Do not use `npm install`, use `yarn install`

  





# Theme

https://jamstackthemes.dev/theme/11ty-starter-boilerplate/

```bash
cd personal_finance_blog
git clone --depth=1 https://github.com/ixartz/Eleventy-Starter-Boilerplate.git site
```





# Other

##### Open website

```bash
http://localhost:8080
```



##### About the JAM stack

https://snipcart.com/blog/jamstack

##### Latex for Eleventy

https://benborgers.com/posts/eleventy-katex/







# Docker -> Not used anymore

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




