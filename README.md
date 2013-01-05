django-vagrant-chef-simple
==========================

This project provides a template for a simple configuration for setting up a development environment for django with vagrant and chef.  [Honza's django-chef][0] provided much of the code for starting this project.  Cookbooks are cloned directly from [opscode][cookbooks]. 

After following the instructions below, you will have a simple bare-bones configuration for your project running.  This project uses [apache2 with mod_wsgi][django_apache_modwsgi] and mysql as the database.  Static files are served directly with apache.  This configuration may not be perfect for performance, but it is easy to understand and fairly easy to set up.

Right now this project is only tested with the precise32 box provided on vagrant's website.  I plan to expand the project to work with other flavors of Ubuntu as well as CentOS and RedHat soon.

Dependencies
---------------

  - [VirtualBox] [1]
  - [Vagrant] [2]
  - [Fabric] [fabric] - see below for installation instructions on Windows


Chef cookbooks included
---------------
These are directly cloned into the project instead of included as sub-modules, mostly because of [this suggestion] [9] for chef-solo users.

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
  
1. Start by cloning your django project a folder named "appname" in the main project directory ([how to][7]).

        cd django-vagrant-chef-simple
        git clone /path/to/your/project appname

   This project expects manage.py to live one directory __below__ `appname`.  Thus, the location from the top directory would be `django-vagrant-chef-simple/appname/myprojectname/manage.py`.

1. Create a deployment specific requirements file.  This will be called via pip to install any python packages required for your project.  Mine looks like this:

        Django==1.3.1
        Pinax==0.9a2
        South==0.7.6
        django-appconf==0.5
        django-compressor==1.0.1
        django-debug-toolbar==0.8.5
        django-extensions==0.9
        django-staticfiles==1.1.2
        django-tastypie==0.9.11
        ipython==0.13
        mimeparse==0.1.3
        mysql-python==1.2.3
        pinax-theme-bootstrap==0.1.2

  Don't forget `mysql-python`!
        
1. Edit the main VagrantFile under the "django_settings" variable to change: 
  * `project_name` from `onpoint` to the name of your project, e.g. `myprojectname`
  * `pip_requirements_file` to the location of your requirements file, relative to the directory `project_folder_name`
  * `south_apps` to a list of the apps that you want to migrate using [South][south].
  * `fixtures` to a list of the fixtures you want to be installed in your new database.  The `description` field is only used by vagrant to to display information about what data is being loaded.  

1. We suggest you create a fixture called `user_session.json` to load initial superuser data.  You can place this in any fixture directory in your project.  You can dump this out of your current installation by running the command:

        python manage.py dumpdata --indent=2 auth.user

  Delete all but the first entry from this file, which should be the superuser account you created when first running `manage.py syncdb`

1. Create a file called `production_settings.py` at the same level as `manage.py`; use this to over-ride anythin in `settings.py` that you want changed in production.  For example, mine has the following:

        DEBUG = False
        TEMPLATE_DEBUG = DEBUG
        
        SERVE_MEDIA = DEBUG
        
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.mysql", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
                "NAME": "appname",                       # Or path to database file if using sqlite3.
                "USER": "root",                             # Not used with sqlite3.
                "PASSWORD": "iloverandompasswordsbutthiswilldo",                         # Not used with sqlite3.
                "HOST": "",                             # Set to empty string for localhost. Not used with sqlite3.
                "PORT": "3306",                             # Set to empty string for default. Not used with sqlite3.
            }
        }

1. Start vagrant box (Windows command console).  

        vagrant up

  After executing this command you should see your site [here] [4]

1. When finished, destroy box (Windows command console)

        vagrant destroy

More commands specific to dealing with Vagrant boxes can be in [the Vagrant tutorial] [8].

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
* To ssh into the box, use this command with cygwin on Windows.  Your project files will be found in the `/vagrant/appname` directory.

        ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no vagrant@127.0.0.1 -p 2222

* Try using a different distro if you experience problems when adding a recipe to this project
 * For me, the mysql recipe would not install correctly with lucid64, but worked fine with precise32
 * More boxes can be found [here][6]
    
  [cookbooks]: https://github.com/opscode-cookbooks/
  [pycrypto]: http://www.voidspace.org.uk/python/modules.shtml#pycrypto
  [fabric]: http://docs.fabfile.org/en/1.5/index.html
  [fabric_tutorial]: http://docs.fabfile.org/en/1.5/tutorial.html

  [apache2]: https://github.com/opscode-cookbooks/apache2.git
  [apt]: https://github.com/opscode-cookbooks/apt.git
  [south]: http://south.readthedocs.org/en/latest/index.html
  [build-essential]: https://github.com/opscode-cookbooks/build-essential.git
  [git]: https://github.com/opscode-cookbooks/git.git
  [vim]: https://github.com/opscode-cookbooks/vim.git
  [python]: https://github.com/opscode-cookbooks/python.git
  [mysql]: https://github.com/opscode-cookbooks/mysql.git
  [openssl]: https://github.com/opscode-cookbooks/openssl.git
  [django_apache_modwsgi]: https://docs.djangoproject.com/en/1.4/howto/deployment/wsgi/modwsgi/
  
  [0]: https://github.com/honza/django-chef
  [1]: https://www.virtualbox.org/wiki/Downloads
  [2]: http://vagrantup.com/
  [4]: http://localhost:8070/
  [5]: https://github.com/opscode-cookbooks/
  [6]: https://github.com/mitchellh/vagrant/wiki/Available-Vagrant-Boxes
  [7]: http://stackoverflow.com/questions/651038/how-do-you-clone-a-git-repository-into-a-specific-folder
  [8]: http://vagrantup.com/v1/docs/getting-started/teardown.html
  [9]: http://stackoverflow.com/questions/8941034/provisioning-vagrant-w-chef