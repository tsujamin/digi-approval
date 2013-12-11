#
# Cookbook Name:: django_db
# Recipe:: default
#
# Copyright 2013, DigiACTive Pty Ltd
#
# All rights reserved - Do Not Redistribute
#

include_recipe 'database::postgresql'

# connection info
postgresql_connection_info = {
  :host     => 'localhost',
  :port     => node['postgresql']['config']['port'],
  :username => 'postgres',
  :password => node['postgresql']['password']['postgres']
}

# create database django
postgresql_database 'django' do
  connection postgresql_connection_info
  action :create
end

# create user django, password django
postgresql_database_user 'django_user' do
  connection    postgresql_connection_info
  password      'django_password'
  action        :create
end

# grant rights to db django
postgresql_database_user 'django_user' do
  connection    postgresql_connection_info
  database_name 'django'
  privileges    [:all]
  action        :grant
end
