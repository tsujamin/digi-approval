# -*- encoding: utf-8 -*-
#
# Cookbook Name:: clamav
# Recipe:: default
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

case node['platform_family']
when 'rhel'
  include_recipe "#{cookbook_name}::install_rpm"
when 'debian'
  include_recipe "#{cookbook_name}::install_deb"
else
  fail(Chef::Exceptions::UnsupportedAction,
       "Cookbook does not support #{node["platform"]} platform")
end

include_recipe "#{cookbook_name}::users"
include_recipe "#{cookbook_name}::logging"
include_recipe "#{cookbook_name}::freshclam"
include_recipe "#{cookbook_name}::clamd"
include_recipe "#{cookbook_name}::services"
include_recipe "#{cookbook_name}::clamav_scan"

# vim: ai et ts=2 sts=2 sw=2 ft=ruby
