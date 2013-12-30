#
# Cookbook Name:: app
# Recipe:: default
#
# Copyright 2013, DigiACTive Pty Ltd
#
# All rights reserved - Do Not Redistribute
#

# Verify that we're a messy dev env only
if node.chef_environment != "development" 
  abort "No production environment defined yet, only 'development'"
end

# Install Python
# install the software collections, then install the python 2.7
# package
yum_package "centos-release-SCL"
yum_package "python27"
# Allow it to find postgres
ENV["PATH"] = ENV["PATH"] + ":/usr/pgsql-9.3/bin"

# do a simple dodgy deployment
# heavily based on https://github.com/poise/application_python/blob/master/providers/django.rb

# create a virtualenv
#give up entirely on python_virtualenv for now - it doesn't support environment vars
execute "scl enable python27 'virtualenv /vagrant/env'" do
  user "vagrant"
  group "vagrant"
  not_if do ::File.exists?('/vagrant/env/bin/python') end
end

# install packages
# (make sure git is around for our own versions of packages)
include_recipe 'git'

Chef::Log.info("Installing packages from requirements.txt")
# interestingly using the absolute path to virtualenv pip will make
# sure things are installed to the virtualenv
execute "scl enable python27 '/vagrant/env/bin/pip install -r requirements.txt'" do
  cwd "/vagrant/src"
  user "vagrant"
  group "vagrant"
  # so pip can write log files, build directories, etc.
  environment 'HOME' => '/home/vagrant/'
end


# create local_settings.py
template "/vagrant/src/digiapproval_project/digiapproval_project/local_settings.py" do
  source "local_settings.py.erb"
  owner "vagrant"
  group "vagrant"
  mode "644"
  variables node['digiactive']
end

# Do all the django setup
# This has to be done w/i the venv, so we create and run a script for it.
template "/tmp/init_django.bash" do
  source "init_django.bash.erb"
  owner "vagrant"
  group "vagrant"
  mode "755"
  variables node['digiactive']
end

execute "scl enable python27 '/tmp/init_django.bash'" do
  cwd "/vagrant/src/digiapproval_project"
  user "vagrant"
  group "vagrant"
end

file "/tmp/init_django.bash" do
  action :delete
end

# permit port 8000 for dev traffic
simple_iptables_rule "http-dev" do
  rule [ "--proto tcp --dport 8000"]
  jump "ACCEPT"
end

# to debug lamson, install mutt
yum_package "mutt"
