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

execute "create-database" do
    command "mysql -p\"#{node['mysql']['server_root_password']}\" -e 'CREATE DATABASE #{node[:dbname]}'"
    # show with:
    # command "mysql -p\"#{node['mysql']['server_root_password']}\" -e 'SHOW DATABASES;'"
end

execute "create log file directory" do
    command "sudo mkdir /etc/apache2/logs"
    action :run
end

execute "create error log file" do
    command "sudo touch /etc/apache2/logs/homelab-error.log"
    creates "/etc/apache2/logs/homelab-error.log"
    action :run
end

execute "create access log file" do
    command "sudo touch /etc/apache2/logs/homelab-access.log"
    creates "/etc/apache2/logs/homelab-error.log"
    action :run
end

# Should probably do this through apache node properties instead
execute "add line to config file" do
    command "echo 'Include /etc/apache2/httpd.conf' >> /etc/apache2/apache2.conf"
    action :run
end

# Should probably do this through apache node properties instead
# This overwrites file created by apache2 module
template "#{node['apache']['dir']}/httpd.conf" do
  source "httpd.conf.erb"
  owner "root"
  group node['apache']['root_group']
  mode 00644
end

execute "Sync db" do
    command "python manage.py syncdb --noinput"
    cwd "/vagrant/#{node[:project_name]}/#{node[:app_name]}"
    action :run
end

execute "Create superuser" do
    # This must have been created with a dump of the admin acct and the most recent admin session
    #> python manage.py dumpdata --indent=2 auth.user sessions.session
    command "python manage.py loaddata user_session.json"
    cwd "/vagrant/#{node[:project_name]}/#{node[:app_name]}"
    action :run
end

# Migrate applications using South
execute "Migrate app" do
    command "python manage.py migrate survey_browser"
    cwd "/vagrant/#{node[:project_name]}/#{node[:app_name]}"
    action :run
end
execute "Migrate tasypie" do
    command "python manage.py migrate tastypie"
    cwd "/vagrant/#{node[:project_name]}/#{node[:app_name]}"
    action :run
end

# Load new site_media and setup to serve with apache
execute "Remove existing site_media folder" do
    command "rm -r site_media/"
    cwd "/vagrant/#{node[:project_name]}/#{node[:app_name]}"
    action :run
end
execute "Collect staticfiles" do
    command "python manage.py collectstatic --noinput"
    cwd "/vagrant/#{node[:project_name]}/#{node[:app_name]}"
    action :run
end
execute "Create symlink between site_media and srv folder" do
    command "sudo ln -s /vagrant/appname/homesurvey/site_media/ /var/www/site_media"
    action :run
end

execute "Load database starter" do
    command "python manage.py loaddata loaded_options.json"
    cwd "/vagrant/#{node[:project_name]}/#{node[:app_name]}"
    action :run
end

execute "Create local django settings" do
    command "cp production_settings.py local_settings.py"
    cwd "/vagrant/#{node[:project_name]}/#{node[:app_name]}"
    action :run
end

execute "restart mysql" do
    command "sudo service mysql restart"
end
execute "restart apache" do
    command "sudo service apache2 restart"
end