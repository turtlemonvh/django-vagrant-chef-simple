"""
Based off:
https://github.com/honza/django-chef/blob/master/fabfile.py

Timothy Van Heest
12/06/2012
"""

from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

# User and ssh key
env.user = 'vagrant'
env.password = 'vagrant'
env.key_filename = ['H:\.ssh\id_rsa'] # doesn't seem to make a difference right now

# Hosts and default port
# Get with command "vagrant ssh-config"
env.hosts = ['127.0.0.1']
env.port = '2222'

"""
Configuation variables; change for your project
"""
code_dir = 'H:\django_vagrant_base\appname' # location of code on your computer
vm_code_dir = "/vagrant/appname" # location of code in created vm
projectname = "homesurvey" # name of your project, both folder and django name

    
def list_project_dir():
    with cd(vm_code_dir):
        run("ls -lah")

def update_repo():
    code_dir = code_dir
    with cd(code_dir):
        run("git pull")
        run("touch app.wsgi")

def restart_apache():
    sudo("service apache2 restart", pty=False)
        
# Call post pull
# http://stackoverflow.com/questions/6379484/fabric-appears-to-start-apache2-but-doesnt
def refresh_code():
    with cd(vm_code_dir):
        with cd(projectname):
            run("rm -r site_media/")
            run("python manage.py collectstatic --noinput")
            sudo("service apache2 restart", pty=False)
        
def test_and_commit():
    with settings(warn_only=True):
        result = local('./manage.py test %s' %(projectname), capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")
    else:
        local("git add -p && git commit")
 
        
# Local tasks
def clean():
    """
    Remove all .pyc files
    """
    local('find . -name "*.pyc" -exec rm {} \;')

def debug():
    """
    Find files with debug symbols
    """
    clean()
    local('grep -ir "print" *')
    local('grep -ir "console.log" *')

def todo():
    """
    Find all TODO and XXX
    """
    clean()
    local('grep -ir "TODO" *')
    local('grep -ir "XXX" *')