#!/bin/bash
#Bring the system and its package lists up to date (excluding grub due to manual intervention)
sudo apt-get -y update
sudo apt-mark hold grub-pc
sudo apt-get -y upgrade

#Get packages available on apt and cleanup
sudo apt-get -y install python python-pip postgresql nginx rabbitmq-server swift
sudo apt-get -y autoremove

#Install python packages
sudo pip install Django Carrot
