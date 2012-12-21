Vagrant::Config.run do |config|
  config.vm.define :djangovm do |django_config|
    # Every Vagrant virtual environment requires a box to build off of.
    django_config.vm.box = "precise32"

    # The url from where the 'config.vm.box' box will be fetched if it
    # doesn't already exist on the user's system.
    django_config.vm.box_url = "http://files.vagrantup.com/precise32.box"

    # Forward a port from the guest to the host, which allows for outside
    # computers to access the VM, whereas host only networking does not.
    django_config.vm.forward_port 80, 8070
    django_config.vm.forward_port 8000, 7001

    # Enable provisioning with chef solo, specifying a cookbooks path (relative
    # to this Vagrantfile), and adding some recipes and/or roles.
    django_config.vm.provision :chef_solo do |chef|
      chef.cookbooks_path = "deploy/cookbooks"
      
      # Run recipes
      chef.add_recipe "apt"
      chef.add_recipe "appname::default" # does most of the work

      # Load custom attributes defined in node.json file
      chef.json = { "mysql" => { 
                        "bind_address" => "127.0.0.1",
                        "server_root_password" => "iloverandompasswordsbutthiswilldo",
                        "server_repl_password" => "iloverandompasswordsbutthiswilldo",
                        "server_debian_password" => "iloverandompasswordsbutthiswilldo",
                        "tunable" => { "innodb_adaptive_flushing" => "on"}
                    },
                    :python => { :version => 2.7},
                    :project_name => "appname",
                    :dbname => "appname",
                    :app_name => "homesurvey",
                    :error_log => "homelab-error",
                    :access_log => "homelab-access"
                  }
    end
  end
end

