# Linux Server Configuration
Part of Full Stack Nanodegree on Udacity.com

Link to Nanodegree - https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004

In this project, we take a baseline installation of a Linux distribution on a virtual machine and prepare it to host your web applications, to include installing updates, securing it from a number of attack vectors and installing/configuring web and database servers.

##IP, SSH and URL

The IP address is 52.36.39.199 and SSH port is 2200.

The Catalog project is put on link - http://52.36.39.199/ or http://ec2-52-36-39-199.us-west-2.compute.amazonaws.com/

To login to linux server use the command
ssh -p 2200 -i [RSA file] grader@52.36.39.199

Replace [RSA file] with rsa file provided to the grader

##Summary of softwares (I used mongodb instead of Postgresql, so didn't install postgresql packages)
- Flask
- Mongodb
- Mongoengine

##List of third-party resources used to complete the project
- https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
- https://www.digitalocean.com/community/tutorials/how-to-create-a-ssl-certificate-on-apache-for-ubuntu-14-04
- https://www.digicert.com/ssl-certificate-installation-ubuntu-server-with-apache2.htm