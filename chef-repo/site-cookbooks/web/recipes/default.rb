#
# Cookbook Name:: web
# Recipe:: default
#
# Copyright 2013, DigiACTive Pty Ltd
#
# All rights reserved - Do Not Redistribute
#

# drop in a more useful http config file
execute "nxdissite default"

file "/etc/nginx/conf.d/default.conf" do
  action :delete
end

cookbook_file "uwsgi.conf" do
  path "/etc/nginx/sites-available/uwsgi"
  action :create
end

execute "nxensite uwsgi" do
  notifies :reload, resources(:service => "nginx")
end

# Allow HTTP, HTTPS
simple_iptables_rule "http" do
  rule [ "--proto tcp --dport 80",
         "--proto tcp --dport 443" ]
  jump "ACCEPT"
end
