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
include_recipie "wkhtmltopdf"

# Set up production requirements
execute "install python packages" do
    command "sudo pip install -r /vagrant/#{node[:project_folder_name]}/#{node[:django_settings][:pip_requirements_file]}"
end

execute "install build dependencies for mysqldb" do
    command "sudo apt-get -y build-dep python-mysqldb"
end

execute "create-database" do
    command "mysql -p\"#{node['mysql']['server_root_password']}\" -e 'CREATE DATABASE #{node[:dbname]}'"
    # show with:
    # command "mysql -p\"#{node['mysql']['server_root_password']}\" -e 'SHOW DATABASES;'"
end

# Creates new conf file in the mods-enabled folder; all conf files here are included
template "#{node['apache']['dir']}/mods-enabled/django_mod_wsgi.conf" do
  source "httpd.conf.erb"
  owner "root"
  group node['apache']['root_group']
  mode 00644
  variables({
    :server_name => node[:server_name]
  })
end

execute "Sync db" do
    command "python manage.py syncdb --noinput"
    cwd "/vagrant/#{node[:project_folder_name]}/#{node[:django_settings][:project_name]}"
    action :run
end

# Migrate applications using South
node[:django_settings][:south_apps].each do |app|
    execute "Migrate #{app}" do
        command "python manage.py migrate #{app}"
        cwd "/vagrant/#{node[:project_folder_name]}/#{node[:django_settings][:project_name]}"
        action :run
    end
end

# Install fixtures
node[:django_settings][:fixtures].each do |fixture|
    execute "#{fixture[:description]}" do
        command "python manage.py loaddata #{fixture[:name]}"
        cwd "/vagrant/#{node[:project_folder_name]}/#{node[:django_settings][:project_name]}"
        action :run
    end
end

# Load new site_media and setup to serve with apache
directory "/vagrant/#{node[:project_folder_name]}/#{node[:django_settings][:project_name]}/site_media" do
  recursive true
  action :delete
  not_if do ! File.directory?("/vagrant/#{node[:project_folder_name]}/#{node[:django_settings][:project_name]}/site_media") end
end
execute "Collect staticfiles" do
    command "python manage.py collectstatic --noinput"
    cwd "/vagrant/#{node[:project_folder_name]}/#{node[:django_settings][:project_name]}"
    action :run
end
link "/var/www/site_media" do
  to "/vagrant/#{node[:project_folder_name]}/#{node[:django_settings][:project_name]}/site_media/"
end

execute "Create local django settings" do
    command "cp #{node[:django_settings][:production_settings_file]} local_settings.py"
    cwd "/vagrant/#{node[:project_folder_name]}/#{node[:django_settings][:project_name]}"
    action :run
end

execute "restart mysql" do
    command "sudo service mysql restart"
end
execute "restart apache" do
    command "sudo service apache2 restart"
end


