

# Deployment


### tax_credit

```
cd tax_credit
pipenv run pip freeze > requirements.txt
gcloud app deploy
```



View the app

```
gcloud app browse
```



# First time setting up

```
cd tax_credit
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