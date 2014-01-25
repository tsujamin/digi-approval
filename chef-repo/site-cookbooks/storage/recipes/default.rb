# -*- coding: utf-8 -*-
#
# Cookbook Name:: storage
# Recipe:: default
#
# Copyright 2013, DigiACTive Pty Ltd
#
# All rights reserved - Do Not Redistribute
#

include_recipe "git"
include_recipe "build-essential"

# hack. don't know why this is necessary but whatever
if node['platform_family'] == "rhel"
  package "MySQL-python" do
    action :install
  end
end

git "/home/" + node['digiactive']['user'] + "/devstack" do
  repository "https://github.com/openstack-dev/devstack.git"
  user node['digiactive']['user']
  group node['digiactive']['user']
  action :sync
end

# fixme: ignores environment
template "/home/" + node['digiactive']['user'] + "/devstack/localrc" do
  source "localrc.erb"
  owner node['digiactive']['user']
  group node['digiactive']['user']
end

# check if there is an existing one running - stolen from stack.sh
Chef::Log.info("Installing OpenStack devstack")
execute 'type -p screen >/dev/null && screen -ls | egrep -q "[0-9].stack" || /home/' + node['digiactive']['user'] + '/devstack/stack.sh' do
  cwd "/home/" + node['digiactive']['user'] + "/devstack"
  user node['digiactive']['user']
  group node['digiactive']['user']
end

# Set the Temp URL key
# fixme: ignores environment
execute "set temp url key" do
  command "swift --os-username admin --os-tenant-name demo " + 
          "--os-password password --os-auth-url http://127.0.0.1:5000/v2.0 " +
          "post -m 'Temp-URL-Key:" + node['digiactive']['swift_temp_url_key'] +
          "'"
  cwd "/home/" + node['digiactive']['user'] + "/devstack"
  user node['digiactive']['user']
  group node['digiactive']['user']
end

# open fw for web interface on 8080
simple_iptables_rule "swift-frontend" do
  rule [ "--proto tcp --dport 8080"]
  jump "ACCEPT"
end
