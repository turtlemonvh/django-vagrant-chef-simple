#
# Cookbook Name:: apache2
# Recipe:: dav_svn
#
# Copyright 2008-2009, Opscode, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

include_recipe "apache2::dav"

package "libapache2-svn" do
  case node['platform_family']
  when "rhel", "fedora", "suse"
    package_name "mod_dav_svn"
  else
    package_name "libapache2-svn"
  end
end

case node['platform_family']
when "rhel", "fedora", "suse"

  file "#{node['apache']['conf']}/conf.d/subversion.conf" do
    action :delete
    backup false
  end

end

apache_module "dav_svn"