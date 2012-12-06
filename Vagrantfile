Vagrant::Config.run do |config|
  config.vm.define :djangovm do |django_config|
    # Every Vagrant virtual environment requires a box to build off of.
    django_config.vm.box = "lucid64"

    # The url from where the 'config.vm.box' box will be fetched if it
    # doesn't already exist on the user's system.
    django_config.vm.box_url = "http://files.vagrantup.com/lucid64.box"

    # Forward a port from the guest to the host, which allows for outside
    # computers to access the VM, whereas host only networking does not.
    django_config.vm.forward_port 80, 8070
    django_config.vm.forward_port 8000, 7001

    # Enable provisioning with chef solo, specifying a cookbooks path (relative
    # to this Vagrantfile), and adding some recipes and/or roles.
    django_config.vm.provision :chef_solo do |chef|
      chef.cookbooks_path = "cookbooks"
      chef.provisioning_path = "/tmp/vagrant-chef"
      
      chef.add_recipe "apt"
      chef.add_recipe "webapp" # does most of the work

      # You may also specify custom JSON attributes:
      chef.json = { :mysql_password => "foo",
                    :python => { :version => 2.7},
                    :projectname => "HOMELAB_homesurvey" # set this
                  }
    end
  end
end

