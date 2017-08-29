# TheDeployer
Python 2.7 app that uses Fabric to deploy apps to Ubuntu boxes via SSH.

The Deployer is a tool I use to deploy applications and their dependencies to linux boxes via SSH. It's configurable. You create a configuration for the app, a JSON file that defines the app files, dependencies, and where they go. 

So far, I've built in support for:
Python
Flask
Supervisor
Nginx
Postgres
React

The Deployer usually requires small modifications or feature additions based on the environment its deploying to. 
