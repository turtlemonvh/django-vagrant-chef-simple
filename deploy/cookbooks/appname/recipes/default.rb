# From: http://honza.ca/2011/04/virtual-machines-for-django-developers
# 

execute "Update apt repos" do
    command "apt-get update"
end

include_recipe  "openssl"
include_recipe  "postgresql::server"
include_recipe  "apache2"
include_recipe  "apache2::mod_wsgi"
include_recipe  "build-essential"
include_recipe  "git"
include_recipe  "vim"
include_recipe  "python"
include_recipe  "mongodb::10gen_repo"
include_recipe  "mongodb::default"

# Install extra packages for PIL
apt_package "libjpeg62" do
  action :install
end
apt_package "libjpeg-dev" do
  action :install
end
apt_package "libfreetype6" do
  action :install
end
apt_package "libfreetype6-dev" do
  action :install
end
apt_package "zlib1g-dev" do
  action :install
end

# Install packages for wkhtmltopdf
apt_package "libxrender1" do
  action :install
end
apt_package "libfontconfig1" do
  action :install
end

# Create links to packages
execute "Add symbolic link to libjpeg" do
    command "sudo ln -s /usr/lib/i386-linux-gnu/libjpeg.so /usr/lib/"
end
execute "Add symbolic link to libfreetype" do
    command "sudo ln -s /usr/lib/i386-linux-gnu/libfreetype.so /usr/lib/"
end
execute "Add symbolic link to libz" do
    command "sudo ln -s /usr/lib/i386-linux-gnu/libz.so /usr/lib/"
end

# Set up production requirements
execute "install python packages" do
    command "sudo pip install -r /src/#{node[:project_folder_name]}/#{node[:django_settings][:pip_requirements_file]}"
end

execute "create-database" do
    command "PGPASSWORD=#{node['postgresql']['password']['postgres']} createdb #{node[:dbname]} --username=postgres -h localhost"
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

execute "Create local django settings" do
    command "cp #{node[:django_settings][:production_settings_file]} local_settings.py"
    cwd "/src/#{node[:project_folder_name]}/#{node[:django_settings][:project_name]}"
    action :run
end

execute "Sync db" do
    command "python manage.py syncdb --noinput"
    cwd "/src/#{node[:project_folder_name]}/#{node[:django_settings][:project_name]}"
    action :run
end

# Migrate applications using South
node[:django_settings][:south_apps].each do |app|
    execute "Migrate #{app}" do
        command "python manage.py migrate #{app}"
        cwd "/src/#{node[:project_folder_name]}/#{node[:django_settings][:project_name]}"
        action :run
    end
end

# Install fixtures
node[:django_settings][:fixtures].each do |fixture|
    execute "#{fixture[:description]}" do
        command "python manage.py loaddata #{fixture[:name]}"
        cwd "/src/#{node[:project_folder_name]}/#{node[:django_settings][:project_name]}"
        action :run
    end
end

# Load new site_media and setup to serve with apache
directory "/src/#{node[:project_folder_name]}/#{node[:django_settings][:project_name]}/site_media" do
  recursive true
  action :delete
  not_if do ! File.directory?("/src/#{node[:project_folder_name]}/#{node[:django_settings][:project_name]}/site_media") end
end
execute "Collect staticfiles" do
    command "python manage.py collectstatic --noinput"
    cwd "/src/#{node[:project_folder_name]}/#{node[:django_settings][:project_name]}"
    action :run
end
link "/var/www/site_media" do
  to "/src/#{node[:project_folder_name]}/#{node[:django_settings][:project_name]}/site_media/"
end

execute "restart postgres" do
    command "sudo service postgresql restart"
end
execute "restart apache" do
    command "sudo service apache2 restart"
end


# Setup wkhtml
# From https://github.com/scalarium/example-cookbooks/blob/master/wkhtmltopdf/recipes/install.rb
wkhtmltopdf_file = "wkhtmltopdf-#{node[:wkhtmltopdf][:version]}-static-#{node[:wkhtmltopdf][:arch]}.tar.bz2"

remote_file "/tmp/#{wkhtmltopdf_file}" do
  source "http://wkhtmltopdf.googlecode.com/files/#{wkhtmltopdf_file}"
  owner 'root'
  group 'root'
  not_if do
    File.exist?(node[:wkhtmltopdf][:binary])
  end
end

execute "tar xfvj /tmp/#{wkhtmltopdf_file}" do
  cwd "/tmp"
  not_if do
    File.exist?(node[:wkhtmltopdf][:binary])
  end
end

execute "sudo mv /tmp/wkhtmltopdf-#{node[:wkhtmltopdf][:arch]} #{node[:wkhtmltopdf][:binary]}" do
  creates node[:wkhtmltopdf][:binary]
end

# For using "find" and "locate" commands
execute "Update file database" do
  command "sudo updatedb"
end
