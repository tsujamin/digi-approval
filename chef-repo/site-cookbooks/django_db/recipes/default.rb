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
postgresql_database node['digiactive']['django_db_name'] do
  connection postgresql_connection_info
  action :create
end

# create user django, password django
postgresql_database_user node['digiactive']['django_db_user'] do
  connection    postgresql_connection_info
  password      node['digiactive']['django_db_password']
  action        :create

end

# grant rights to do everything
# not just the main db - so as to enable testing
# TODO: lock this down.
postgresql_database node['digiactive']['django_db_name'] do
  connection    postgresql_connection_info
  sql           "ALTER ROLE #{node['digiactive']['django_db_user']} CREATEDB;"
  action        :query
end
