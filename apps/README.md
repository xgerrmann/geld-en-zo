

# Deployment

If gloud has not been setup yet follow the 'install gcloud' instructions in this document.

```
cd src
pipenv run pip freeze > requirements.txt
gcloud app deploy
```



View the app

```
gcloud app browse
```

Dont forget to append the app path to the url, e.g.

* ```
  /tax_credit
  ```

* ```
  /income_tax
  ```

  



# First time setting up

```
cd src
pipenv shell
pipenv install
```

Then in your browser go to one off

* `localhost:8080/tax_credit`
* `localhost:8080/income_taxes`



# Local testing

If this is the first time trying to run the apps locally, perform the steps described in 'first time setting up' (above)

```
cd tax_credit
pipenv shell
gunicorn -b 0.0.0.0:8080 main:server --reload
```

# Dash google cloud web app example
* https://datasciencecampus.github.io/deploy-dash-with-gcp/
* https://github.com/datasciencecampus/deploy-dash-with-gcp/tree/master/simple-dash-app-engine-app



# Include app in blog

* Find the url

  * One way to find the url is:

  ```
  cd tax_credit
  gcloud app browse
  ```

* Change **http://** to `https://`

* Put it in an iframe



# Installing gcloud

* Follow these instructions:

https://www.google.com/search?channel=fs&client=ubuntu&q=linux+install+gcloud

* Open a NEW terminal window (since the .zshrc has changed)

* Then perform authorization

  ```
  gcloud auth login
  ```

* Set the project (project ID can be found in the google console on cloud.google.com)

  ```
  gcloud config set project  personal-finance-app-300718
  ```

  