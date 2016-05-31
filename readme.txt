#rsync -a /dfs/dn -e "ssh -i carlo-kp.pem" ec2-user@ip-172-31-14-78.ap-southeast-2.compute.internal:/dfs
#sudo rsync -rtvz /dfs/dn --rsh "ssh -i carlo-kp.pem" --rsync-path "rsync" ec2-user@ip-172-31-13-104.ap-southeast-2.compute.internal:/dfs
#sudo yum -y install cloudera-manager-agent
#fab -u ec2-user -i /Users/cpiva/Desktop/carlo-kp.pem disable_iptables disable_ipv6 disable_selinux disable_transparent_hugepage install_wget
