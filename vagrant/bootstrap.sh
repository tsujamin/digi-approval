#!/bin/bash
#Generate missing locales
locale-gen en_AU.UTF-8

#Bring the system and its package lists up to date (excluding grub due to manual intervention)
apt-get -y update
apt-mark hold grub-pc
apt-get -y upgrade

#Get packages available on apt
apt-get -y install python3 python3-pip postgresql-9.1 nginx rabbitmq-server  postgresql-server-dev-9.1 python3-dev

#Setup python3 aliases for all users
echo "alias python=\"python3\"
alias pip=\"pip3\"" >> /etc/profile
. /etc/profile

#Install python packages
easy_install3 Pillow Django Django-Celery psycopg2

#Configure postgres (add user for vagrant and user/database for django)
sudo -u postgres bash -c "createuser -s vagrant
psql -c \"CREATE USER django WITH PASSWORD 'django';\" postgres
psql -c \"CREATE DATABASE django;\" postgres
psql -c \"GRANT ALL ON DATABASE django TO django;\" postgres"

#Workaround for upstart apparently not calling our rc*.d scripts
echo "start on runlevel [2345]
stop on runlevel [016]
script
  exec /etc/init.d/rc 2
  /usr/bin/startmain
  /usr/bin/startrest
end script" > /etc/init/runlevel2.conf

#Configure swift
bash /vagrant/vagrant/swiftstrap.sh

#Configure RabbitMQ
rabbitmqctl add_user django django
rabbitmqctl add_vhost djangoMQ
rabbitmqctl set_permissions -p djangoMQ django ".*" ".*" ".*"

#Cleanup
apt-get -y autoremove

