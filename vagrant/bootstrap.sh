#!/bin/bash
#Generate missing locales
locale-gen en_AU.UTF-8

#Bring the system and its package lists up to date (excluding grub due to manual intervention)
apt-get -y update
apt-mark hold grub-pc
apt-get -y upgrade

#Get packages available on apt
apt-get -y install python3 python3-pip postgresql-9.1 nginx rabbitmq-server swift postgresql-server-dev-9.1 python3-dev
apt-get -y autoremove

#Install python packages
pip3 install Django Django-Celery psycopg2 Pillow

#Setup python3 aliases for vagrant user
echo "alias python=\"python3\"
alias pip=\"pip3\"" >> /home/vagrant/.bashrc

#Configure postgres (add user for vagrant and user/database for django)
sudo -u postgres bash -c "createuser -s vagrant
psql -c \"CREATE USER django WITH PASSWORD 'django';\" postgres
psql -c \"CREATE DATABASE django;\" postgres
psql -c \"GRANT ALL ON DATABASE django TO django;\" postgres"