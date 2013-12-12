#
# Cookbook Name:: app
# Recipe:: default
#
# Copyright 2013, DigiACTive Pty Ltd
#
# All rights reserved - Do Not Redistribute
#

# Install Python3
# this messily hopes the attributes are correctly set elsewhere
# for now in the role.
if not ::File.exists?("#{node["python_build"]["install_prefix"]}/bin/python3")
  import_recipe "python-build"
end

# Verify that we're a messy dev env only
if node.chef_environment != "development" 
  abort "No production environment defined yet, only 'development'"
end

# do a simple dodgy deployment
# heavily based on https://github.com/poise/application_python/blob/master/providers/django.rb

# create a virtualenv
python_virtualenv "/vagrant/env" do
  interpreter "python3"
  owner "vagrant"
  group "vagrant"
  action :create
end

# it is enough to use the right pip to get a correctly located install
Chef::Log.info("Installing packages from requirements.txt")
execute "/vagrant/env/bin/pip install -r requirements.txt" do
      cwd "/vagrant/src"
      user "vagrant"
      group "vagrant"
end

# permit port 8000 for dev traffic
simple_iptables_rule "http-dev" do
  rule [ "--proto tcp --dport 8000"]
  jump "ACCEPT"
end
