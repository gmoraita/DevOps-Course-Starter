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
The TODO app use a MongoDB database cluster hosted on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas). There is a free tier, which is suitable for the purposes of this app. If you choose the "I'm learning MongoDB" option at sign-up then the set-up instructions are very intuitive. Start the sign-up process [here](https://www.mongodb.com/try) and refer to the below for guidance:
* Cloud & Region: Select any nearer your region
* Security: Select username/password authentication and select the IP from where your app is hosted
Note that once created, the cluster might take a bit of time to spin up

Change the ```.env``` you created to add the connection string on ```DB_CONNECTION_STRING```. Replace the placeholders for username, passowrd and cluster as follows:
* USER_NAME: Created when you signed up to MongoDB Atalas. A list is visible in the "Database Access" menu under the "Security" heading
* PASSWORD: Created druing sign up as well. If lost you'll have to to change the password in the "Database Access" menu.
* CLUSTER: Get from the mongo URL which is visible in the "Connect" menu of your cluster. Look for a URL that ends .mongodb.net

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
The C4 Architecture diagrams are maintained in C4-Architecture-diagram file which is in Draw IO (Digrams.NET) format https://www.diagrams.net/ 

You can view them online through their online service or dowloading their app. They also have a VSCode plugin

Note - the "Code Diagram" UML classes and packages diagrams are generated from the code using pylint's pyreverse. You will need to install GraphViz (https://graphviz.org/download/)

Then run:

``` poetry run pyreverse -o png -p -p todo_app .```

This will generate 2 files:
```classes_-p.png``` and ```packages_-p.png``` which then can be added as images to the C4 "Code diagram" tab.

## Continuous Integration using Travis CI
Travis CI is set up to work well with GitHub but for it to work you need to enable it for any repository you want to use it for. Instructions are here: https://docs.travisci.com/user/tutorial/#to-get-started-with-travis-ci-using-github. 
Follow the first three steps for signing up with GitHub, making sure you activate Travis CI for the TODO app repository.

To run the e2e tests with selenium you will need the env variables. The .travis.yml already has those but if you want to replace follow these steps:
* Install Ruby ```sudo apt install ruby```
* Install Travis ```sudo gem install travis```
* Login to Travis ```travis login --pro --github-token <gitbub token>```. The token can be obtained from here: https://github.com/settings/tokens/
* Encrypt the environment variable TRELLO_API_KEY using: ```travis encrypt --pro TRELLO_API_KEY=<the API Key> --add```
* Encrypt the environment variable TRELLO_API_SECRET using: ```travis encrypt --pro TRELLO_API_SECRET=<the API Secret> --add```
 
## Continuous Deployment using Heroku
Everytime there is a commit, there will also be an automatic deployment to Heroku server, provided CI completed successfully. Also the docker images are published to DockerHub

You will need to set on Heroku the env variables:
``` 
heroku config:set `cat .env | grep TRELLO_API_KEY` -a <heroku_app_name> 
heroku config:set `cat .env | grep TRELLO_API_SECRET` -a <heroku_app_name> 
heroku config:set `cat .env | grep TRELLO_USER` -a <heroku_app_name> 
heroku config:set `cat .env | grep TRELLO_BOARD_NAME` -a <heroku_app_name> 
```

NOTE: If not done yet, please encrypt the environment variable HEROKU_API_KEY using: ```travis encrypt --pro HEROKU_API_KEY=<the API Secret> --add```

Then make a change and commit to github

You can goto https://travis-com/dashboard and then select the repository to see the build progress

Once complete you can open the application on your browser:
``` heroku open -a <heroku_app_name> 


