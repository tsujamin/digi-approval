# -*- encoding: utf-8 -*-
#
# Cookbook Name:: clamav
# Recipe:: services
#
# Copyright 2012-2014, Jonathan Hartman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

[
  node['clamav']['clamd']['pid_file'],
  node['clamav']['freshclam']['pid_file']
].map { |f| File.dirname(f) }.compact.uniq.each do |d|
  directory d do
    owner node['clamav']['user']
    group node['clamav']['group']
    recursive true
  end
end

c_service = node['clamav']['clamd']['service']
c_enabled = node['clamav']['clamd']['enabled']
service c_service do
  supports status: true, restart: true
  action :nothing
end

f_service = node['clamav']['freshclam']['service']
f_enabled = node['clamav']['freshclam']['enabled']
service f_service do
  supports status: true, restart: true
  action :nothing
end

ruby_block 'dummy service notification block' do
  block do
    Chef::Log.info('Dispatching service notifications...')
  end
  notifies(c_enabled ? :enable : :disable, "service[#{c_service}]")
  notifies(c_enabled ? :start : :stop, "service[#{c_service}]")
  notifies(f_enabled ? :enable : :disable, "service[#{f_service}]")
  notifies(f_enabled ? :start : :stop, "service[#{f_service}]")
end

# vim: ai et ts=2 sts=2 sw=2 ft=ruby
