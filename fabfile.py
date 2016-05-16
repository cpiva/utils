from fabric.api import *
from fabric.contrib.console import confirm
from fabric.api import env

# host list 
env.roledefs = {
    'cm': ['ec2-52-63-17-219.ap-southeast-2.compute.amazonaws.com'],
    'nn1': ['ec2-52-63-192-102.ap-southeast-2.compute.amazonaws.com'],
    'nn2': ['ec2-52-62-35-187.ap-southeast-2.compute.amazonaws.com'],
    'dn':  ['ec2-52-63-163-14.ap-southeast-2.compute.amazonaws.com', 
            'ec2-52-63-126-80.ap-southeast-2.compute.amazonaws.com',
            'ec2-52-62-214-118.ap-southeast-2.compute.amazonaws.com']
}

env.warn_only = True

@parallel
@roles("cm","nn1","nn2","dn")
def test():
    sudo("time")

@parallel
@roles("cm","nn1","nn2","dn")
def update():
    sudo("yum -y update", pty=True)

@roles("cm","nn1","nn2","dn")
def sync_ntp():
    sudo("sudo service ntp stop")
    sudo("sudo service ntp start")
    sudo("chkconfig ntpd on")
    sudo("ntpdate time.apple.com")
    sudo("ntpd -q")

@roles("cm","nn1","nn2","dn")
def disable_iptables():
    sudo("service iptables save")
    sudo("service iptables stop")
    sudo("chkconfig iptables off")

@roles("cm","nn1","nn2","dn")
def install_mysql():
    sudo("yum -y install mysql")
    sudo("wget http://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.39.tar.gz")
    sudo("tar zxvf mysql-connector-java-5.1.39.tar.gz")
    sudo("mkdir -p /usr/share/java/")
    sudo("cp mysql-connector-java-5.1.39/mysql-connector-java-5.1.39-bin.jar /usr/share/java/mysql-connector-java.jar")

@roles("cm","nn1","nn2","dn")
def install_openldap_krb_w():
    sudo("yum -y install openldap-clients", pty=True)
    sudo("yum -y install krb5*", pty=True)
    put("krb5.conf","/tmp/krb5.conf")
    sudo("mv /tmp/krb5.conf /etc/krb5.conf")

@roles("cm","nn1","nn2","dn")
def install_wget():
    sudo("yum -y install wget", pty=True)

@roles("cm","nn1","nn2","dn")
def upload_private_key():
    put("/Users/cpiva/Desktop/carlo-kp.pem","/home/ec2-user/")

@roles("cm","nn1","nn2","dn")
def disable_selinux():
    sudo("sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config")

@roles("cm","nn1","nn2","dn")
def disable_ipv6():
    sudo("echo 'NETWORKING_IPV6=no' >> /etc/sysconfig/network")
    sudo("echo 'IPV6INIT=no' >> /etc/sysconfig/network")
    sudo("service network restart")

@roles("cm","nn1","nn2","dn")
def install_wget():
    sudo("yum -y install wget")

@roles("cm","nn1","nn2","dn")
def install_java_rpm():
    sudo('wget --no-check-certificate --no-cookies --header \
         "Cookie: oraclelicense=accept-securebackup-cookie" \
          http://download.oracle.com/otn-pub/java/jdk/7u79-b15/jdk-7u79-linux-x64.rpm')
    sudo("rpm -ivh jdk-7u79-linux-x64.rpm")

@roles("cm","nn1","nn2","dn")
def install_java():
    sudo("sudo yum install oracle-j2sdk1.7")   

@roles("cm","nn1","nn2","dn")
def set_swappiness():
    sudo("sysctl -w vm.swappiness=10")

@roles("cm","nn1","nn2","dn")
def disable_transparent_hugepage():
    sudo("echo never > /sys/kernel/mm/transparent_hugepage/defrag")

@roles("cm","nn1","nn2","dn")
def add_admin_user():
    sudo("useradd admin")

@roles('cm','nn2')
def install_mysql_server():
    sudo("wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm")
    sudo("rpm -ivh mysql-community-release-el7-5.noarch.rpm")
    sudo("yum -y install mysql-server")
    sudo("systemctl start mysqld")

@roles('cm','nn2')
def restart_mysql_server():
    sudo("systemctl restart mysqld")

@roles("cm")
def get_cloudera_repo():
    sudo('wget https://archive.cloudera.com/cm5/redhat/7/x86_64/cm/cloudera-manager.repo')
    sudo("mv cloudera-manager.repo /etc/yum.repos.d/cloudera-manager.repo")

@roles("cm")
def install_cm():
    sudo("sudo yum install cloudera-manager-daemons cloudera-manager-server")
    sudo("sudo service cloudera-scm-server start")    

@roles("cm")
def create_external_dbs():
    sudo("mysql -uroot -pabc123 -e 'create database amon;'")
    sudo("mysql -uroot -pabc123 -e 'create database rman;'")
    sudo("mysql -uroot -pabc123 -e 'create database metastore;'")
    sudo("mysql -uroot -pabc123 -e 'create database sentry;'")
    sudo("mysql -uroot -pabc123 -e 'create database nav;'")
    sudo("mysql -uroot -pabc123 -e 'create database navms;'")
    sudo("mysql -uroot -pabc123 -e 'create database oozie;'")

@roles("cm")
def create_scm_db():
    sudo("sh /usr/share/cmf/schema/scm_prepare_database.sh mysql -h ip-172-31-12-78.ap-southeast-2.compute.internal -uroot -pabc123 --scm-host ip-172-31-12-78.ap-southeast-2.compute.internal scm scm scm;")

@roles("cm")
def get_parcels():
    sudo("mkdir -p /opt/parcel-downloads")
    sudo("wget -P /opt/parcel-downloads -r --no-parent https://archive.cloudera.com/cdh5/parcels/latest/")

@roles("nn1")
def start_rpcbind():
    sudo("sudo service rpcbind start")

@roles("kdc")
def enable_kerberos_client():
    sudo("yum -y install krb5-libs krb5-auth-dialog krb5-workstation", pty=True)
    put("krb5.conf","/etc/krb5.conf")



