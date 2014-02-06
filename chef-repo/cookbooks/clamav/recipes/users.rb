# -*- encoding: utf-8 -*-
#
# Cookbook Name:: clamav
# Recipe:: users
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

# These should be created by the package install but, just in case...
user node['clamav']['user'] do
  comment 'Clam Anti Virus Checker'
  system true
  shell '/sbin/nologin'
end

group node['clamav']['group'] do
  members [node['clamav']['user']]
  system true
  only_if { node['clamav']['user'] != node['clamav']['group'] }
end

# vim: ai et ts=2 sts=2 sw=2 ft=ruby
