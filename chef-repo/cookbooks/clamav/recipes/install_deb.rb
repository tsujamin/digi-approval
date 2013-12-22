#
# Cookbook Name:: clamav
# Recipe:: install_deb
#
# Copyright 2012-2013, Jonathan Hartman
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

include_recipe "apt"

service node["clamav"]["clamd"]["service"]
service node["clamav"]["freshclam"]["service"]

apt_repository "clamav-repo" do
  uri "http://ppa.launchpad.net/ubuntu-clamav/ppa/ubuntu"
  distribution node['lsb']['codename']
  components ["main"]
  keyserver "keyserver.ubuntu.com"
  key "5ADC2037"
  only_if { node["platform"] == "ubuntu" }
  notifies :run, "execute[apt-get update]", :immediately
end

package "clamav" do
  action :install
  version node["clamav"]["version"] if node["clamav"]["version"]
  if node["clamav"]["clamd"]["enabled"]
    notifies :restart,
      "service[#{node["clamav"]["clamd"]["service"]}]"
  end
  if node["clamav"]["freshclam"]["enabled"]
    notifies :restart,
      "service[#{node["clamav"]["freshclam"]["service"]}]"
  end
end

package "clamav-daemon" do
  action :install
  version node["clamav"]["version"] if node["clamav"]["version"]
  if node["clamav"]["clamd"]["enabled"]
    notifies :restart,
      "service[#{node["clamav"]["clamd"]["service"]}]"
  end
end

package "libclamav-dev" do
  action :install
  version node["clamav"]["version"] if node["clamav"]["version"]
  only_if { node["clamav"]["dev_package"] }
end

files = %w{/etc/logrotate.d/clamav-daemon /etc/logrotate.d/clamav-freshclam}
files.each do |f|
  file f do
    action :delete
  end
end

# vim: ai et ts=2 sts=2 sw=2 ft=ruby fdm=marker
