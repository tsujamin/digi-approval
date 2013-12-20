#
# Cookbook Name:: broker
# Recipe:: default
#
# Copyright 2013, DigiACTive Pty Ltd
#
# All rights reserved - Do Not Redistribute
#

include_recipe "rabbitmq::default"

if node.chef_environment == "development"
  include_recipe "rabbitmq::mgmt_console"
  
  # mgmt console:
  include_recipe "simple_iptables"
  simple_iptables_rule "rabbitmq-mgmt" do
    rule [ "--proto tcp --dport 15672"]
    jump "ACCEPT"
  end
end
