# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Database Connectivity
The TODO app use a MongoDB database

You can run a local mongoDB for dev purposes by running:
```docker-compose up -d todoapp-local-mongodb```
It will spin a local mongoDB from a cloud image. You can connect at the default 27017 port. Any records added will persist in local volume created in ```./localmongodb``` so you can find them later even if you bring the container down

Change if needed the ```.env``` you created and add the following information (if not already there):
* ```DB_CONNECTION_STRING=mongodb://localhost:27017```


## Integration with GitHub authentication using the OAuth flow
* Register the app with Github
    * Follow the Github [documentation](https://docs.github.com/en/developers/apps/building-oauth-apps/creating-an-oauth-app) to create your oauth app.
    * For the homepage URL field enter the address for accessing the website locally.
    * For the callback add a particular path to this URL for example /login/
callback.
* You will need both a client-id (```GITHUB_CLIENT_ID```) and client-secret (```GITHUB_CLIENT_SECRET```) for your ```.env``` file. The client-secret once generated will only be shown once, so take a note of it to avoid needing to regenerate one later.

Note: For integration with Heroku (see firther down) create an additional oauth app and add separate ```GITHUB_CLIENT_ID``` and ```GITHUB_CLIENT_SECRET```

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the Tests

To run the Selenium tests, you will need to download the Gecko driver:
https://github.com/mozilla/geckodriver/releases

Place the driver at the root of the project

Before running the tests, install with pip the following:
```bash
pip install -U pytest
pip install -U mock
pip install -U requests_mock
pip install -U selenium
pip install -U selenium-requests
poetry add pytest selenium selenium-requests mock --dev
```
To run the tests:
* go to the root of the project 
* run the below - it will launch all tests:
```
poetry run pytest
```

Troubleshooting!
Getting the driver to work can be a bit of a pain! If it isn’t working, try these things
* you’ll need the browser (FireFox in this case) installed as well as the driver.
* the browser and the driver will need to be the same version
* the driver must be on the $PATH
* on Mac, you may get a permissions error. If you do, try the steps explained here:
https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-errorchromedriver-cannot-be-opened-because-the-de


## Using Vagrant
You can create a new Hypervisor installed with your app and in running mode.
* Download and install VirtualBox on your host https://www.virtualbox.org/wiki/Downloads
* Download and install Vagrant: https://www.vagrantup.com/downloads 
* Open a shell 
* Go to the root of your TODO app
* Run the following on your command line to create the virtual machine with the TODO app installed and running:
```bash
vagrant up --provision
```
* Once complete login to the hypervisor created (username & password: vagrant/vagrant)
```bash
vagrant ssh
```
* Then tail the gunicorn access logs:
```bash
cd /vagrant
tail -f ./gunicorn-access.log
```
* Open a browser on your host and go to: http://localhost
* You should see the TODO app and in the logs a new entry

NOTE: if there is already a binding on port 80 in your host you can change the port on Vargantfile (replace xxxx with your desired port):
config.vm.network "forwarded_port", guest: 5000, host: xxxx


## Using Docker
To run with Docker you need the Docker Desktop (Windows and Mac). 
* Docker Desktop overview: https://www.docker.com/products/docker-desktop
* Installation intructions: https://docs.docker.com/docker-for-windows/install/

Once installed you can create the prod, dev and testing containers:

Production:

``` docker build --target production --tag todo-app:prod . ```

To create and run the container use:

``` docker run  -p 80:5000 --env-file .env  -d todo-app:prod ```
On your browser go to http://localhost to view the app (in case port 80 is already bound, replace 80 in the above command with another port)


Development & Testing

``` docker-compose up -d ```
you can pass the ``` --build ``` flag if you want to re-build.

On your browser go to http://localhost:5100 to view the app

To see the logs of the test containers do the following:
* List all containers with ```docker ps -a```
* From the list, look at the last column "NAMES" and copy the name of the containers which have "test" 
* Type ```docker logs <container name>``` to see the logs e.g.:
``` docker logs devops-course-starter_todoapp-test-offline_1``` (non-selenium tests)
``` docker logs devops-course-starter_todoapp-test-online_1``` (selenium tests)


## C4 
The C4 Architecture diagrams are maintained in C4-Architecture-diagram file which is in Draw IO (Diagrams.NET) format [https://www.diagrams.net/](https://www.diagrams.net/) 

You can view them online through their online service or dowloading their app. They also have a VSCode plugin

Note - the "Code Diagram" UML classes and packages diagrams are generated from the code using pylint's pyreverse. You will need to install [GraphViz](https://graphviz.org/download/)

Then run:

``` poetry run pyreverse -o png -p -p todo_app .```

This will generate 2 files:
```classes_-p.png``` and ```packages_-p.png``` which then can be added as images to the C4 "Code diagram" tab.

## Azure setup
The app runs on the Azure Cloud. Azure hosts the production application, in a docker container, as an Azure
App Service, and using Azure's CosmosDB, which has an API compatible with MongoDB.

Ensure you have an Azure account created at the [Azure portal](https://portal.azure.com)

* Setup 
    * Step 1: Follow the instructions to [Install azure CLI](https://docs.microsoft.com/en-us/cli/azure/) on your machine if you haven't already.
    * Step 2: Add resource group: ```az group create -l uksouth -n <resource_group_name>```
    * Step 3: Setup the Cosmos Database with Mongo API: 
        * Create a new CosmosDB: ```az cosmosdb create --name <cosmos_account_name> --resourcegroup <resource_group_name> --kind MongoDB```
        * Create new MongoDB database under that account: ```az cosmosdb mongodb database create --account-name <cosmos_account_name> --name <database_name> --resourcegroup <resource_group_name>```
    * Step 4: Connect the app to the CosmosDB: ```az cosmosdb keys list -n <cosmos_account_name> -g <resource_group_name> --type connection-strings```. This will give us a connection string. Alter the given connection string to tell pymongo to use the default database: Add ```/DefaultDatabase``` after the port number in the given connection string, eg: ```mongodb://<database_name>:<primarymasterkey>@<database_name>.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&<config>```. Keep this connection string as we will encrypt in the next section in Travis CI
    * Step 5: Create a web app: 
        * First create an App Service Plan: ```az appservice plan create --resource-group <resource_group_name> -n <appservice_plan_name> --sku Free --is-linux```
        * Then create the Web App: ```az webapp create --resource-group <resource_group_name> --plan <appservice_plan_name> --name <webapp_name> --deployment-container-image-name <dockerhub_username>/todoapp:latest```
    * Step 6: Setup the environment variables from your ```.env``` file: e.g ```az webapp config appsettings set -g <resource_group_name> -n <webapp_name> --settings FLASK_APP=todo_app/app```. Or you can pass in a JSON file containing all variables by using ```--settings @foo.json```, see [here](https://docs.microsoft.com/en-us/cli/azure/webapp/config/appsettings?view=azure-cli-latest#az_webapp_config_appsettings_set).
    


## Continuous Integration using Travis CI
Travis CI is set up to work well with GitHub but for it to work you need to enable it for any repository you want to use it for. Instructions are here: https://docs.travisci.com/user/tutorial/#to-get-started-with-travis-ci-using-github. 
Follow the first three steps for signing up with GitHub, making sure you activate Travis CI for the TODO app repository.

To run the e2e tests with selenium you will need the env variables. The .travis.yml already has those but if you want to replace follow these steps:
* Install Ruby ```sudo apt install ruby```
* Install Travis ```sudo gem install travis```
* Login to Travis ```travis login --pro --github-token <gitbub token>```. The token can be obtained from here: https://github.com/settings/tokens/

* Encrypt the CosmoDB database connection string from the previous section: ```travis encrypt --pro "DB_CONNECTION_STRING=<Cosmo DB connection string>" --add```. NOTE: ensure you escape the special characters & with \\& and the $ sign with \\\$

You can goto [Travis Dashboard](https://travis-ci.com/dashboard) and then select the repository to see the build progress
 
## Continuous Deployment using Dockerhub and Azure
Everytime there is a commit, there will also be an automatic deployment to Azure server, provided CI completed successfully. Also the docker images are published to DockerHub

You will first need to add the Docker username and password to the travis configuration
```
travis encrypt --pro DOCKER_USER=<docker username> --add
travis encrypt --pro DOCKER_PWD=<docker password> --add
```

We need to enable the CD in Azure and use the webhook to trigger the CD once a new image is available on HitHub
* Enable CD: ```az webapp deployment container config --enable-cd true --resource-group <resource_group_name> --name <webapp_name>```. This will return a web hook url
* Add this to Travis: ```travis encrypt --pro "AZURE_WEBHOOK_URL=<web hook url from previous step>" --add```. NOTE: ensure you escape the special characters & with \\& and the $ sign with \\\$




