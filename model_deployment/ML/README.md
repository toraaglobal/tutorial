# Deploy a machine learning model using docker container
Model deployment is one of the key component in data science. You build a model, in other to make use of it in the production environment, you need to deploy it.
This tutorial will illustrate a step by step guide on how to deploy a production ready model deployment using docker container.

### Why docker container?
* its easy to reproduce in different environment
* isolation portability
* Scalibility

### The overall achitecture of the application/ api deployment


### Step 1 : Build and train the machine learning model
 Train the machine learning model.
 Use `model.py` to create a sample model mimicking the production environment,retrieving data from database.

### Step 2: Build an api using flask to serve the model

Build a flask api using python and flasgger to manage the api documentation.


### Step 3: Dockerize the application 
put evrything into a docker container ready for production using WSGI to manage the usage concurrency.
Flast <====> Apache [WSGI]

Using the WSGI( web server gateway interface) for production ready application that will manage user concurrency as flask can not handle production application.


## Step 4: Deploy the application 
Install the Heroku CLI

`https://devcenter.heroku.com/articles/heroku-cli#download-and-install`

Download and install the Heroku CLI.

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


### Using docker registry for deployment

Install the Heroku CLI

Download and install the Heroku CLI.

If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.

```
heroku login
```

Log in to Container Registry

You must have Docker set up locally to continue. You should see output when you run this command.

```
docker ps
```

Now you can sign into Container Registry.

```
heroku container:login
```

Push your Docker-based app

Build the Dockerfile in the current directory and push the Docker image.

```
heroku container:push web
```

Deploy the changes

Release the newly pushed images to deploy your app.

```
heroku container:release web
```


## References
https://www.udemy.com/course/deploy-data-science-nlp-models-with-docker-containers/

