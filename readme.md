# IS429 Cloud Computing Lab for AngularJS Development and CI with Nitrous.IO, GAE and Jenkins

This tutorial will cover the steps for using a virtual maching (VM) on [Nitrous.IO](https://www.nitrous.io) to develop and deploy AngularJS web apps running on a node.js server.

The tutorial is divided into the following 2 sections: 

1. Part 1 walks through the steps to use Git and Jenkins as a test and deploy tool to push updates to Google App Engine (PaaS).
2. Part 3 covers AngularJS and GAE web app development approaches


## Sign up for GitHub and Nitrous.IO

1. Sign up for [GitHub](https://github.com)
2. Sign up for [Nitrous.IO](https://www.nitrous.io). You can choose to use your GitHub account to do this, or your own email. If you are going to use Nitrous.IO to develop for both Python and node.js stacks, please sign up for two Nitrous.IO accounts.
3. Once your Nitrous.IO registration has been completed, create new node.js VM Box from [here](https://www.nitrous.io/app#/boxes/new)
4. Open the IDE of the VM Box, which should look like this:

![koding terminal](https://github.com/andrewbeng89/IS429AngularTest/raw/master/images/nitrous_ide.png)

## Part 1: Github, CloudBees and Jenkins

### Configuring Git and GitHub

Use the Nitrous.IO console located at the bottom section of the IDE to execute terminal commands. 

Generate a new ssh key pair on the VM to use to sync with GitHub and Jenkins.

1. `cd ~/.ssh`
2. `ssh-keygen -t rsa -C "<your_email@example.com>"`
3. When "Enter file in which to save the key (/home/action/.ssh/id_rsa):" is prompted, enter  `/home/action/.ssh/nitrous_id_rsa`
4. `Enter passphrase (empty for no passphrase): [Type a passphrase]`
5. `Enter same passphrase again: [Type passphrase again]`
6. Once the key pair has been generated, open the public key nitrous_id_rsa.pub using with vim `vim nitrous_id_rsa.pub`
7. Copy the public key (first line) and add it to your [GitHub keys](https://github.com/settings/ssh) with a new key name, e.g. nitrous_node
8. Close vim by entering `:q!`
5. Create a new config file in the .ssh folder and enter these lines below:
<pre>
  <code>
# Default GitHub user
 Host github.com
 HostName github.com
 PreferredAuthentications publickey
 IdentityFile ~/.ssh/nitrous_id_rsa
  </code>
</pre> 


### Clone and Configure Demo App

1. Set your git user email identity `git config --global user.email "<your_email@example.com>"`
2. Set your git user name identity `git config --global user.name "<Your Name>"`
3. Clone this repository `git clone https://github.com/andrewbeng89/IS429GAETest.git`
4. `cd IS429GAETest`
5. Reomve the .git directory `rm -rf .git`
6. Create a new GitHub repository with your account
7. Initialise the demo app as a git repo on the VM `git init`
8. Add the remote to the newly create GitHub repository `git remote add origin git@github.com:<your_username>/<your_new_repo>.git`


### Install and use the GAE Python SDK

After signing up for [Google App Engine](https://appengine.google.com), install the GAE SDK on your Nitrous.IO Box

1. `curl http://googleappengine.googlecode.com/files/google_appengine_1.8.8.zip > gae_python-1.8.8.zip`
2. `unzip gae_python-1.8.8.zip`
3. `rm gae_python-1.8.8.zip`


### Running the application on Nitrous.IO

You can use Nitrous.IO as a testing environment for development.

1. `cd app`
2. In the app/ directory, create a new file `credentials.js`
3. Add `module.exports = {MONGO_PASSWORD:"is429"};` and save
4. Install the dependencies `npm install`
5. Run the app `node main.js`
6. Under "Preview" from the IDE, select "Port 3000" to view the app which should look like this:

![koding terminal](https://github.com/andrewbeng89/IS429AngularTest/raw/master/images/webapp_preview.png)


### Continuous Integration with CloudBees and GitHub

CloudBees provides [Jenkins](https://wiki.jenkins-ci.org/display/JENKINS/Meet+Jenkins), a framework for building/testing software projects continuously, as a service. Developers can hook their GitHub project to this service, triggering automated test, build and deployment scripts whenever a push is made to the GitHub repository. Follow these steps to use Jenkins-as-a-Service with GitHub and CloudBees:

1. Go to `https://<your-username>.ci.cloudbees.com/pluginManager/available`
2. Select the GitHub plugin and click "Install without restart"
3. During the installation process, check "Restart Jenkens when installation is complete..."
4. Once Jenkins has restarted, go to `https://<your-username>.ci.cloudbees.com/configure` and scroll down to "GitHub Web Hook"
5. Check "Let Jenkins auto-manage..."
7. Enter GitHub credentials and test them
6. Check "Override Hook URL"
7. Copy the Hook URL
8. Go to `https://github.com/<your-username>/<your-repository>/settings/hooks`
9. Select "Jenkins (Github plugin)" and enter the URL
10. Check "Active" and click "Test Hook"
6. Click "Apply" at the bottom of the page.


Create and configure new CloudBees hosted node.js application

1. `bees app:create -a <your-app-name> -t nodejs -P MONGO_PASSWORD="is429" -R PLUGIN.SRC.nodejs=https://dl.dropboxusercontent.com/u/6484381/nodejs-clickstack.zip`
2. Go to `https://<your-username>.ci.cloudbees.com/view/All/newJob` to configure a new Jenkins build job
3. Check "Build a free-style software project" and click "Ok"
4. Uncheck "Restrict where this project can be run" under "CloudBees DEV@cloud Authorization" on the next page
5. Check "Git" under "Source Code Management" and enter `https://github.com/<your-username>/<your-repository>.git` as the "Repository URL"
6. Check "Build when a change is pushed to GitHub" under "Build Triggers"
7. Select "Execute shell" from "Add build step" dropdown
8. Add "Deploy applications" build step
9. Click "Add application" and enter the Application ID of the app you just created in the first step
10. Change "Application file" to `target/*.zip`
11. Add "Publish JUnit test result report" from "Add post-build action" and fill `test_out/unit.xml,test_out/e2e.xml` in "Test report XMLs"
12. Add the contents of `./build_script` to the shell commands under "Execute shell":
13. Finally... click "Apply" at the bottom of the page!


To test the CI testing and deployment:

1. `cd ~/IS429AngularTest`
2. Make some changes to app/index.html using the Nitrous.IO IDE
3. Commit the changes `git commit -m "test changes to app/index.html"`
4. Push the changes to GitHub `git push origin master`
5. Go to `https://<your-username>.ci.cloudbees.com/job/<your-build-id>/` where the build will start shortly


## Part 2: AngularJS Development in the Cloud

This section will cover simple front and back end techniques to get you up to speed with AngularJS application development in the Cloud

### AngularJS

[AngularJS](http://angularjs.org) provides a modularized approach to bind data structures, e.g. Arrays, Objects and other variables, to HTML views. This repository provides the code for a simple "todo list" application created in AngularJS.

AngularJS also provides an easy way to implment [single page applications](http://en.wikipedia.org/wiki/Single-page_application) with front end templating and routing. In this example application, routing to the various templates are in app/js/app.js while the HTML fragments are stored in the app/partials directory. Each template can then be associated to a unique AngularJS controller (app/js/controllers.js).

This repository also provides a classic "todo" application with two backend approaches:

1. A pure front-end AngularJS app that syncs with a [Firebase](https://firebase.com) real-time Database-as-a-Service
2. Integrated AngularJS app that communites with a Node.js back-end hosted on CloudBees


### AngularJS + Firebase + AngularFire

[Firebase](https://firebase.com) provides a real-time Object (JSON) database. [AngularFire](http://angularfire.com/) is a JavaScript library that allows developers to bind AngularJS scope objects with real-time data from Firebase. CRUD operations will be persisted and executed on the client-side without any need for any backend operations. 

Take a look at app/partials/todos.html and the "TodoFireController" in app/js/controllers.js. 

To create your own Firebase real-time database: 

1. Sign up for Firebase with your GitHub account
2. Create a new developer plan Firebase, and note the URL of the Firebase
3. Change this line in app/js/controllers.js: `var ref = new Firebase('https://<your-firebase-name>.firebaseio.com/todos');`
4. Push an update GitHub
5. View the app on your CloudBees app URL one the build is completed
6. Create some new todos and reload the page and observe
7. Open up different windows to the same URL and observe when you perform CRUD on the todos

This version of the "todo" app is enabled by default.


### Node.js with MongoDB (Mongolab Database-as-a-Service)

To enable the node.js with MongoDB version of the "todo" app, change `var firebase_backend` in app/js/app.js to `false`. This will enable the "TodoController" in AngularJS.

[Node.js](http://nodejs.org) is a JavaScript platform built on [Google's V8 engine](https://code.google.com/p/v8/), and is used to develop a wide variety of network applications, including web applications.

This demo application uses the [Express web app framework](http://expressjs.com/) as its backbone, with a app/ folder containing all of the front (js/, css/, partials/ etc.) and back-end (main.js, package.json etc.) code. 

The application database used here is [MongoDB](http://www.mongodb.org/), a document/object based database system. Unlike a traditional relational databse system (e.g. MySQL, Oracle DB), MongoDB is an example of a non-relational [NoSQL](http://en.wikipedia.org/wiki/NoSQL) database. Other examples of NoSQL database systems include CouchDB and Google's App Engine Datastore (NDB is covered in the [sister GAE tutorial](https://github.com/andrewbeng89/mitb_gae_demo)).

To uses MongoDB-as-a-Service hosted on [Mongolab](https://mongolab.com) with the "todo list" application, follow these steps:

1. Sign up for Mongolab [here](https://mongolab.com/signup/)
2. Once logged in, proceed to create a new mondolab development environment [here](https://mongolab.com/create). Remember to select "Development (single-node)" under "plans"
3. Choose a name for the database, e.g. "is429-todos"
4. When prompted, create the credentials for a new database user (username and password)
5. Make a note of the database name and the username and password of the new user you have just created 

To make use of the MongoDB database you have just created in the Node.js web application these credentials have to be used in a secure manner:

1. For developemnt on Nitrous.IO, app/credentials.js will be used
2. Using the CloudBees SDK, the MongoDB password will be set as CloudBees config variable

To use the password in the development environment, edit the contents of "credentials.js" (created in Part 1) accordingly:

<pre>
  <code>
module.exports = {
    MONGO_PASSWORD: '<MongoDB Password from Mongolab here>'
};
  </code>
</pre>

Using CloudBees SDK from the VM terminal:

1. `bees config:set MONGO_PASSWORD=<MongoDB Password from Mongolab here> -a <your-username>/<your-repo>`
2. Verify that the MONGO_PASSWORD variable has been set: `bees config:list -a <your-username>/<your-repo>`

Change the MongoDB URL endpoint in this line in app/main.js

`connection_string = 'mongodb://<your-db-username>:' + MONGO_PASSWORD + '@<your-mongolab-host>:39088/<your-database>';`


## View the demo app on [CloudBees](http://angular-awesome.andrewbeng89.cloudbees.net)