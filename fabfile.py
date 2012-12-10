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
env.hosts = ['127.0.0.1']
env.port = '2222'

appname = "HOMELAB_homesurvey"

def hello():
    print("Hello world!")
    
def list_project_dir():
    code_dir = "/vagrant/%s" %(appname)
    with cd(code_dir):
        run("ls -lah")

def test_and_commit():
    with settings(warn_only=True):
        result = local('./manage.py test homesurvey', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")
    else:
        local("git add -p && git commit")
 
def update_hdrive():
    code_dir = 'H:\django_vagrant_base\HOMELAB_homesurvey'
    with cd(code_dir):
        run("git pull")
        run("touch app.wsgi")
        
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