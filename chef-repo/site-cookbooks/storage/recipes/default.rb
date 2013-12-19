#
# Cookbook Name:: storage
# Recipe:: default
#
# Copyright 2013, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#

# Verify that we're a messy dev env only
if node.chef_environment != "development" 
  abort "No production environment defined yet, only 'development'"
end

include_recipe "git"

# hack. don't know why this is necessary but whatever
if node['platform_family'] == "rhel"
  package "MySQL-python" do
    action :install
  end
end

git "/home/vagrant/devstack" do
  repository "https://github.com/openstack-dev/devstack.git"
  user "vagrant"
  group "vagrant"
  action :sync
end

template "/home/vagrant/devstack/localrc" do
  source "localrc.erb"
  user "vagrant"
  group "vagrant"
end

# check if there is an existing one running
execute "/home/vagrant/devstack/unstack.sh" do
cwd "/home/vagrant/devstack"
  user "vagrant"
  group "vagrant"
end

Chef::Log.info("Installing OpenStack devstack")
execute "/home/vagrant/devstack/stack.sh" do
  cwd "/home/vagrant/devstack"
  user "vagrant"
  group "vagrant"
end

# open fw for web interface on 8080
simple_iptables_rule "swift-frontend" do
  rule [ "--proto tcp --dport 8080"]
  jump "ACCEPT"
end
