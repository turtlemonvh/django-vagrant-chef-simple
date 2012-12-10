# From: http://honza.ca/2011/04/virtual-machines-for-django-developers
# 

execute "Update apt repos" do
    command "apt-get update"
end

include_recipe  "openssl"
include_recipe  "mysql::server"
include_recipe  "apache2"
include_recipe  "apache2::mod_wsgi"
include_recipe  "build-essential"
include_recipe  "git"
include_recipe  "vim"
include_recipe  "python"

# Set up production requirements
execute "install python packages" do
    command "sudo pip install -r /vagrant/#{node[:project_name]}/prod_requirements.txt"
end

execute "install build dependencies for mysqldb" do
    command "sudo apt-get -y build-dep python-mysqldb"
end

execute "restart mysql" do
    command "sudo service mysql restart"
end

execute "create-database" do
    command "mysql -p\"#{node['mysql']['server_root_password']}\" -e 'CREATE DATABASE #{node[:dbname]}'"
    # show with:
    # command "mysql -p\"#{node['mysql']['server_root_password']}\" -e 'SHOW DATABASES;'"
end