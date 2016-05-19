from fabric.api import *
from fabric.contrib.console import confirm
from fabric.api import env

# host list 
env.roledefs = {
    'dn':  ['ec2-52-63-41-196.ap-southeast-2.compute.amazonaws.com'],
    'old_dn': ['ec2-52-62-164-31.ap-southeast-2.compute.amazonaws.com']    
}

env.warn_only = True

@parallel
@roles("dn")
def create_dfs_dir():
    sudo("mkdir /dfs")
    sudo("mkdir /dfs/dn"
    sudo("adduser hdfs")
    sudo("chmod -R 777 /dfs")
    sudo("chown -R hdfs:hdfs /dfs")

@parallel
@roles("dn")
def update():
    sudo("yum -y update", pty=True)

@roles("dn")
def sync_ntp():
    sudo("sudo service ntp stop")
    sudo("sudo service ntp start")
    sudo("chkconfig ntpd on")
    sudo("ntpdate time.apple.com")
    sudo("ntpd -q")

@roles("dn")
def disable_iptables():
    sudo("service iptables save")
    sudo("service iptables stop")
    sudo("chkconfig iptables off")

@roles("dn")
def install_mysql():
    sudo("yum -y install mysql")
    sudo("wget http://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.39.tar.gz")
    sudo("tar zxvf mysql-connector-java-5.1.39.tar.gz")
    sudo("mkdir -p /usr/share/java/")
    sudo("cp mysql-connector-java-5.1.39/mysql-connector-java-5.1.39-bin.jar /usr/share/java/mysql-connector-java.jar")

def install_openldap_krb_w():
    sudo("yum -y install openldap-clients", pty=True)
    sudo("yum -y install krb5*", pty=True)
    put("krb5.conf","/tmp/krb5.conf")
    sudo("mv /tmp/krb5.conf /etc/krb5.conf")

@roles("dn")
def install_wget():
    sudo("yum -y install wget", pty=True)

@roles("dn","old_dn")
def upload_private_key():
    put("/Users/cpiva/Desktop/carlo-kp.pem","/home/ec2-user/")

@roles("dn")
def disable_selinux():
    sudo("sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config")

@roles("dn")
def disable_ipv6():
    sudo("echo 'NETWORKING_IPV6=no' >> /etc/sysconfig/network")
    sudo("echo 'IPV6INIT=no' >> /etc/sysconfig/network")
    sudo("service network restart")

@roles("dn")
def install_wget():
    sudo("yum -y install wget")

@roles("dn")
def install_java_rpm():
    sudo('wget --no-check-certificate --no-cookies --header \
         "Cookie: oraclelicense=accept-securebackup-cookie" \
          http://download.oracle.com/otn-pub/java/jdk/7u79-b15/jdk-7u79-linux-x64.rpm')
    sudo("rpm -ivh jdk-7u79-linux-x64.rpm")

@roles("dn")
def install_java():
    sudo("sudo yum install oracle-j2sdk1.7")   

@roles("dn")
def set_swappiness():
    sudo("sysctl -w vm.swappiness=10")

@roles("dn")
def disable_transparent_hugepage():
    sudo("echo never > /sys/kernel/mm/transparent_hugepage/defrag")

