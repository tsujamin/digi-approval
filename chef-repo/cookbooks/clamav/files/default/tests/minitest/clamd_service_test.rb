#
# Cookbook Name:: clamav
# Spec:: clamd_service
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

require "minitest/spec"
require File.expand_path("../support/helpers.rb", __FILE__)

describe_recipe "clamav::clamd_service" do
  include Helpers::ClamAV

  it "should create the dir for the PID file" do
    d = File.dirname(node["clamav"]["clamd"]["pid_file"])
    u = node["clamav"]["user"]
    g = node["clamav"]["group"]
    directory(d).must_exist
    directory(d).must_have(:owner, u).and(:group, g)
  end

  it "should enable clamd if it's enabled" do
    if node["clamav"]["clamd"]["enabled"]
      # Minitest uses process names, not init script service names
      #service("clamd").must_be_running
      res = %x{/etc/init.d/#{node["clamav"]["clamd"]["service"]} status}
      $?.exitstatus.must_equal 0
      service(node["clamav"]["clamd"]["service"]).must_be_enabled
    end
  end

  it "should disable clamd if it's not enabled" do
    if !node["clamav"]["clamd"]["enabled"]
      #service("clamd").wont_be_running
      res = %x{/etc/init.d/#{node["clamav"]["clamd"]["service"]} status}
      $?.exitstatus.wont_equal 0
      service(node["clamav"]["clamd"]["service"]).wont_be_enabled
    end
  end
end

# vim: ai et ts=2 sts=2 sw=2 ft=ruby fdm=marker
