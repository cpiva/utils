from fabric.api import *
from fabric.contrib.console import confirm

# host list 
env.hosts = ['']


env.warn_only = True

@parallel
def update():
    if run("yum check-update").return_code != 0:
        sudo("yum -y update", pty=True)

def upload_private_key():
    put("/home/carlo/Downloads/carlo-kp.pem","/home/ec2-user/")

def disable_selinux():
    sudo("sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config")

def disable_ipv6():
    sudo("sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config")

def enable_kerberos_client():
    #do not run this on the local kdk host (the cm host)
    kdc_host = 'CHANGE_THIS_TO_KDC_HOST'
    if not env.host == kdc_host:
        sudo("yum -y install krb5-libs krb5-auth-dialog krb5-workstation", pty=True)
        sudo("scp -i /home/ec2-user/carlo-kp.pem ec2-user@" + kdc_host + ":/etc/krb5.conf /etc/krb5.conf", pty=True)

def add_admin_user():
    sudo("useradd admin")
