# Deploy a machine learning model using docker container
Model deployment is one of the key component in data science. You build a model, in other to make use of it in the production environment, you need to deploy it.
This tutorial will illustrate a step by step guide on how to deploy a production ready model deployment using docker container.

### Why docker container?
* its easy to reproduce in different environment
* isolation portability
* Scalibility

### The overall achitecture of the application/ api deployment


### Step 1 : Build and train the machine learning model

### Step 2: Build an api usinmg flask to serve the model


### Step 3: Dockerize the application 
Flast <====> Apache [WSGI]

Using the WSGI( web server gateway interface) for production ready application that will manage user concurrency as flask can not handle production application.


## Step 4: Deploy the application 
Create `heroku.yml` file in the root directory:
```
build:
  docker:
    web: Dockerfile
```

commit the file to the repo
```
git add heroku.yml

git commit -m "Add heroku.yml"
```

set stack of the container
```
heroku stack:set container
```
push your application to master

```
git push heroku master
```