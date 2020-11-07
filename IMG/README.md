# How to deploy a production ready machine learning model?
Deploying a machine learning model for  clustering unstructured text using kmeans, docker container and flask API
***

In this article, I will illustrate a step by step guide on how to deploy a flask API to clustered unstructured text  using kmeans and docker container. We will use waitress package to serve the flask API for a production ready application.

Here is the URL of the model we will build and deploy on heroku with details step by step guide.
[Click here to explore the deployed API](wwww.xyz.com)

Project link on github : `https://github.com/toraaglobal/tutorial/tree/machine_learning/NLP`

### Why docker container?
* its easy to reproduce in different environment
* isolation portability
* Scalibility

### Step 1 : Build a machine machine learning model



### Step 2 : Create a flask Application



### Step 3: Put all the application in a docker countainer



### Step 4: deploy the application on heroku
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

