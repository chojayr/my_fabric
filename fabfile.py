from __future__ import with_statement
from fabric.api import *
from fabric.api import task, run
from crypt import crypt
import fabric.contrib
import os.path
import time


@task
def hostname(*args):
  with settings(warn_only=True):
    hname=run('hostname')
    if hname.succeeded:
      puts("hostname suceeded: %s" % hname)
    else:
      puts("hostname is not allowed")


@task
def aptclean():
  with settings(warn_only=False):
    if sudo('apt-get autoclean -y',pty=True).succeeded:
      pass
    else:
      puts("apt-get clean failed")


@task
def aptupdate():
  with settings(warn_only=False):
    if sudo('apt-get update -y',pty=True).succeeded:
      pass
    else:
      puts("apt-get update failed")

@task
def update_kernel():
  with settings(warn_only=True):
    if sudo('apt-get -y install linux-image-generic-lts-raring linux-headers-generic-lts-raring',pty=True).succeeded:
        pass
    else:
        puts("kernel update failed")

@task
def add_docker_repo():
  with settings(warn_only=False):
    sudo('sh -c "echo deb https://get.docker.com/ubuntu docker main > /etc/apt/sources.list.d/docker.list"')
    sudo('apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9')
            

@task
def docker_package():
  with settings(warn_only=True):
    if sudo('apt-get -y install lxc-docker',pty=False).succeeded:
        pass
    else:
        puts("docker installation failed")

@task
def docker_startup():
    sudo('update-rc.d docker defaults')
 

@task
def install_docker():
    add_docker_repo()
    aptupdate()
    docker_package()
    docker_startup()
    aptclean()


@task
def dpkg_docker_stats():
    with settings(warn_only=False):
        dockerversion=sudo('dpkg -l | grep docker',pty=False)
        if dockerversion.succeeded:
            puts("version: %s" % dockerversion)
        else:
            puts("docker is not present here")


@task 
def docker_jenkins():
    with settings(warn_only=True):
        if sudo('docker pull llavina/jenkins:latest; docker run -d=true -p 8080:8080 llavina/jenkins:latest',pty=False).suceeded:
		pass
	else:
		puts("failes to run jenkins container")


@task 
def docker_openjdk7():
    with settings(warn_only=True):
	if sudo('docker run -d=true llavina/openjdk7:latest',pty=False).suceeded:
		pass
	else:
		puts("failes to run openjdk7 container")
