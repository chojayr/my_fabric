from __future__ import with_statement
from fabric.api import *
from fabric.api import task, run
from crypt import crypt
import fabric.contrib
import os.path
import time

env.reject_unknown_hosts=False
env.disable_known_hosts=True

@task
def hostname():
  with settings(warn_only=True):
    hname=run('hostname')
    if hname.succeeded:
      puts("hostname suceeded: %s" % hname)
    else:
      puts("hostname is not allowed")


@task
def yumclean():
  with settings(warn_only=True):
    if sudo('yum clean all',pty=False).succeeded:
      pass
    else:
      puts("yum clean failed")


@task
def yumstatusinotify():
  with settings(warn_only=True):
    inotifyversion=sudo('rpm -qa | grep inotify-tools',pty=False)
    if inotifyversion.succeeded:
      puts("version: %s" % inotifyversion)
    else:
      puts("inotify-tools not present")


@task
def kill_tty():
  with settings(warn_only=True):
    if sudo('a=`w | awk \'{print $1, $2, $5}\' | grep root | grep days | awk \'{print $2}\'; for usertty in $a; do skill -KILL -v $usertty; done;').succeeded:
      pass
    else:
      puts("No tty sessions idle for more than 24 hours")


@task
def check_vim():
  with settings(warn_only=True):
    vim_version=sudo('/usr/bin/vim --version | grep "Vi IMproved" | awk \'{print $5}\' | sed -e "s/\.//g"',pty=False)
  if vim_version.succeeded:
      puts("version: %s" % vim_version)
  else:
      puts("vim not present")

