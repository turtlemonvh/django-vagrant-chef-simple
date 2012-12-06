# From: http://honza.ca/2011/04/virtual-machines-for-django-developers
# 

execute "Update apt repos" do
    command "apt-get update"
end

include_recipe  "apache2::mod_wsgi"
include_recipe  "build-essential"
include_recipe  "git"
include_recipe  "vim"
include_recipe  "python"
include_recipe  "mysql"

#execute "restart postgres" do
#    command "sudo /etc/init.d/postgresql-8.4 restart"
#end

#execute "create-database" do
#    command "createdb -U postgres -O postgres #{node[:dbname]}"
#end

execute "install python packages" do
    command "sudo pip install -r /vagrant/#{node[:projectname]}/requirements.txt"
end

execute "install build dependencies for mysqldb" do
    command "sudo apt-get build-dep python-mysqldb"
end

execute "install mysql python" do
    command "sudo pip install MySQL-python"
end
