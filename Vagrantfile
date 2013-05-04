Vagrant.configure("2") do |config|

  config.vm.define :djangovm do |django_config|
    # Every Vagrant virtual environment requires a box to build off of.
    django_config.vm.box = "precise32"

    # The url from where the 'config.vm.box' box will be fetched if it
    # doesn't already exist on the user's system.
    django_config.vm.box_url = "http://files.vagrantup.com/precise32.box"

    django_config.vm.synced_folder "C:/Users/tcvh/Documents/AptanaWorkspace/onpoint_django", "/src/appname"
    
    # Forward a port from the guest to the host, which allows for outside
    # computers to access the VM, whereas host only networking does not.
    django_config.vm.network :forwarded_port, guest: 80, host: 80
    django_config.vm.network :forwarded_port, guest: 8000, host: 7001

    # Enable provisioning with chef solo, specifying a cookbooks path (relative
    # to this Vagrantfile), and adding some recipes and/or roles.
    django_config.vm.provision :chef_solo do |chef|
      chef.cookbooks_path = "deploy/cookbooks"
      
      # Run recipes
      chef.add_recipe "apt"
      chef.add_recipe "appname::default" # does most of the work

      # Load custom attributes defined in node.json file
      chef.json = { "postgresql" => { 
                        "password" => { "postgres" => "iloverandompasswordsbutthiswilldo"}
                    },
                    :python => { :version => 2.7},
                    :server_name => "precise32",
                    :project_folder_name => "appname",
                    :dbname => "appname",
                    :django_settings => {
                        :project_name => "onpoint",
                        :pip_requirements_file => "requirements/production.txt",
                        :production_settings_file => "production_settings.py",
                        :south_apps => ["tastypie", "social_auth", "viewtracker", "contact", "apps.craigslist"],
                        :fixtures => [
                            {
                                :name => "user_session.json",
                                :description => "Load Superuser"
                            }, 
                            {
                                :name => "initial_data.json",
                                :description => "Sites"
                            }
                        ]
                    },
                    :wkhtmltopdf => {
                        :version => "0.11.0_rc1",
                        :arch => "i386",
                        :binary => "/usr/bin/wkhtmltopdf"
                    }
                  }
    end
  end
end

