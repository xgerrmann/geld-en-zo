

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

# Local testing

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