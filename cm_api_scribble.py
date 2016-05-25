import time
import socket
from datetime import datetime, timedelta
from cm_api.api_client import ApiResource
from cm_api.endpoints.cms import ClouderaManager

CM_HOST = "ec2-52-64-91-202.ap-southeast-2.compute.amazonaws.com"
 
api = ApiResource(CM_HOST, username="admin", password="cr1pt0n1t3")
cm = ClouderaManager(api)

cluster = api.get_cluster('cluster')

for host in api.get_all_hosts('full'):
  print host.hostname

print  
for service in cluster.get_all_services():
  print service
  if service.type == "HDFS":
    hdfs = service

print hdfs.name, hdfs.serviceState, hdfs.healthSummary
print hdfs.serviceUrl
for chk in hdfs.healthChecks:
  print "%s --- %s" % (chk['name'], chk['summary'])

# Reading a metric. Suppose we are interested in:
# the files_total, dfs_capacity and dfs_capacity_used metrics, over the last 24 hrs.
from_time = datetime.fromtimestamp(time.time() - 1800*2*24)
to_time = datetime.fromtimestamp(time.time())
query = "select files_total, dfs_capacity, dfs_capacity_used " \
        "where serviceName = HDFS " \
        "  and category = SERVICE"

result = api.query_timeseries(query, from_time, to_time)
ts_list = result[0]
for ts in ts_list.timeSeries:
  print "--- %s: %s ---" % (ts.metadata.entityName, ts.metadata.metricName)
  for point in ts.data:
    print "%s:\t%s" % (point.timestamp.isoformat(), point.value)

now = datetime.today()
lastHour = datetime.today() - timedelta(hours = 1)
for service in cluster.get_all_services():
  print service
  if service.type == "YARN":
    yarn = service

for app in yarn.get_yarn_applications(lastHour, now, filter_str = "state=RUNNING").applications:
  print app


for host in api.get_all_hosts('full'):
  print host

for role in hdfs.get_all_roles():
    print role

name = 'ip-172-31-1-41.ap-southeast-2.compute.internal'
'''
host = api.create_host(
      name,                             # Host id
      name,                             # Host name (FQDN)
      '172.31.1.41',                  # IP address
      "/default")                       # Rack
'''
hdfs.create_role("hdfs-DATANODE-d9e6f8fa1cc8955d1fa5d2f17088e4e7", "DATANODE", name)


'''
print "Decommissioning hosts. This might take a few minutes."
hosts = ['host1','host2','host3']

for h in hosts:
  cm.hosts_decommission(h)
'''


'''
print "Inspecting hosts. This might take a few minutes."

cmd = cm.inspect_hosts()
while cmd.success == None:
    cmd = cmd.fetch()

if cmd.success != True:
    print "Host inpsection failed!"
    exit(0)

print "Hosts successfully inspected: \n" + cmd.resultMessage

#cmd = hdfs.restart()
#print cmd.active

#cmd = cmd.wait()
#print "Active: %s. Success: %s" % (cmd.active, cmd.success)
'''

#rsync -a /dfs/dn -e "ssh -i carlo-kp.pem" ec2-user@ip-172-31-14-78.ap-southeast-2.compute.internal:/dfs
#sudo rsync -rtvz /dfs/dn --rsh "ssh -i carlo-kp.pem" --rsync-path "rsync" ec2-user@ip-172-31-13-104.ap-southeast-2.compute.internal:/dfs
#sudo yum -y install cloudera-manager-agent
#fab -u ec2-user -i /Users/cpiva/Desktop/carlo-kp.pem disable_iptables disable_ipv6 disable_selinux disable_transparent_hugepage install_wget
