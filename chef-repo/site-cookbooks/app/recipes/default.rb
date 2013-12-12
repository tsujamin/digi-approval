#
# Cookbook Name:: app
# Recipe:: default
#
# Copyright 2013, DigiACTive Pty Ltd
#
# All rights reserved - Do Not Redistribute
#

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
      # seems that if we don't set the HOME env var pip tries to log to /root/.pip, which fails due to permissions
      # setting HOME also enables us to control pip behavior on per-project basis by dropping off a pip.conf file there
      # GIT_SSH allow us to reuse the deployment key used to clone the main
      # repository to clone any private requirements
      #if new_resource.deploy_key
      #  environment 'HOME' => ::File.join(new_resource.path,'shared'), 'GIT_SSH' => "#{new_resource.path}/deploy-ssh-wrapper"
      #else
      #  environment 'HOME' => ::File.join(new_resource.path,'shared')
      #end
      user "vagrant"
      group "vagrant"
end

