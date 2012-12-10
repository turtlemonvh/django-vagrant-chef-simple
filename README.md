django-vagrant-chef-simple
==========================

This project provides a template for a simple configuration for setting up a development environment for django with vagrant and chef.  [Honza's django-chef][0] provided much of the code for starting this project.  Cookbooks are cloned directly from [opscode][cookbooks]. 

Dependencies
---------------

  - [VirtualBox] [1]
  - [Vagrant] [2]
  - [Fabric] [fabric] - see below for installation instructions on Windows


Chef cookbooks included
---------------
These are directly cloned into the project instead of included as sub-modules.  That may change later.

  - [apache2] [apache2]
  - [apt] [apt]
  - [build-essential] [build-essential]
  - [git] [git]
  - [vim] [vim]
  - [python] [python]
  - [mysql] [mysql]
  - [openssl] [openssl]


Basic Use
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
    
        python manage.py runserver [::]:8000
    * You should see your site [here] [3] and a blank apache page [here] [4]

1. When finished, destroy box (Windows command console)

        vagrant destroy

Setting up Fabric
---------------

[Fabric] [fabric] is a python module that allows you to execute commands remotely on multiple remote locations simultaneously, simplifying server administration.

Using Fabric requires installation of the pycrypto modules.  These are compiled C modules, so the easiest way to get them working for Windows is to download the exe directly and install this into your virtual\_env using easy\_install.

1. Download the latest exe of pycrypto [here] [pycrypto]

 * make sure to use the 32 bit version if using 32 bit python, even if you're running 64 bit Windows

1. Install (make sure you activated the correct virtual\_env)

        easy_install pycrypto-2.6.win32-py3.3.exe    
    
1. Install fabric with pip

        pip install fabric 

1. Test your installation by trying [the tutorial] [fabric_tutorial]

        
Tips
---------------
* Additional cookbooks can be found [here] [5]
    
  [0]: https://github.com/honza/django-chef
  [cookbooks]: https://github.com/opscode-cookbooks/
  [pycrypto]: http://www.voidspace.org.uk/python/modules.shtml#pycrypto
  [fabric]: http://docs.fabfile.org/en/1.5/index.html
  [fabric_tutorial]: http://docs.fabfile.org/en/1.5/tutorial.html

  [apache2]: [https://github.com/opscode-cookbooks/apache2.git]
  [apt]: [https://github.com/opscode-cookbooks/apt.git]
  [build-essential]: [https://github.com/opscode-cookbooks/build-essential.git]
  [git]: [https://github.com/opscode-cookbooks/git.git]
  [vim]: [https://github.com/opscode-cookbooks/vim.git]
  [python]: [https://github.com/opscode-cookbooks/python.git]
  [mysql]: [https://github.com/opscode-cookbooks/mysql.git]
  [openssl]: [https://github.com/opscode-cookbooks/openssl.git]

  [1]: https://www.virtualbox.org/wiki/Downloads
  [2]: http://vagrantup.com/
  [3]: http://localhost:7001/
  [4]: http://localhost:8070/
  [5]: https://github.com/opscode-cookbooks/