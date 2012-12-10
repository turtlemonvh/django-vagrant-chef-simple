django-vagrant-chef-simple
==========================

This project provides a template for a simple configuration for setting up a development environment for django with vagrant and chef.

Dependencies
---------------

  - [VirtualBox] [1]
  - [Vagrant] [2]

Using
---------------
  
1. Start by cloning your django project into the "appname" folder:

        cd django-vagrant-chef-simple
        git clone /path/to/your/project appname

1. Start vagrant box (Windows command console)

        vagrant up
        
1. ssh into the box; command below for cygwin on windows (password = vagrant)

        ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no vagrant@127.0.0.1 -p 2222

1. Change into project directory:

        cd /vagrant/appname
        
1. Start django test server:
    * You should see your site [here] [3] and a blank apache page [here] [4]
    
            python manage.py runserver [::]:8000

1. When finished, destroy box (Windows command console)

        vagrant destroy
        
Tips
---------------
* Additional cookbooks can be found [here] [5]
    
  [1]: https://www.virtualbox.org/wiki/Downloads
  [2]: http://vagrantup.com/
  [3]: http://localhost:7001/
  [4]: http://localhost:8070/
  [5]: https://github.com/opscode-cookbooks/