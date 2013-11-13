#!/bin/bash
#Generate missing locales
sudo locale-gen en_AU.UTF-8

#Bring the system and its package lists up to date (excluding grub due to manual intervention)
sudo apt-get -y update
sudo apt-mark hold grub-pc
sudo apt-get -y upgrade

#Get packages available on apt and cleanup
sudo apt-get -y install python3 python3-pip postgresql-9.1 nginx rabbitmq-server swift postgresql-server-dev-9.1 python3-dev
sudo apt-get -y autoremove

#Setup python3 aliases and load them for use in rest of script
echo "alias python=\"python3\"
alias pip=\"pip3\"" >> ~/.bashrc
source ~/.bashrc

#Install python packages
sudo pip3 install Django Django-Celery psycopg2 Pillow

#Configure postgres (add user for vagrant and user/database for django)
sudo -u postgres bash -c "createuser -s vagrant
psql -c \"CREATE USER django WITH PASSWORD 'django';\" postgres
psql -c \"CREATE DATABASE django;\" postgres
psql -c \"GRANT ALL ON DATABASE django TO django;\" postgres"
