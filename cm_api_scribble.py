import time
import uuid
import socket
from datetime import datetime, timedelta
from cm_api.api_client import ApiResource
from cm_api.endpoints.cms import ClouderaManager

CM_HOST = "ec2-52-64-235-74.ap-southeast-2.compute.amazonaws.com"
 
api = ApiResource(CM_HOST, username="admin", password="cr1pt0n1t3")
cm = ClouderaManager(api)
cluster = api.get_cluster('cluster')

def list_hosts():
  for host in api.get_all_hosts('full'):
    print host.hostname

def list_roles():
  hdfs = get_service("HDFS")
  for role in hdfs.get_all_roles():
    print role

def inspect_hdfs():
  hdfs = get_service("HDFS")
  print hdfs.name, hdfs.serviceState, hdfs.healthSummary
  print hdfs.serviceUrl
  for chk in hdfs.healthChecks:
    print "%s --- %s" % (chk['name'], chk['summary'])

def print_metrics():
  from_time = datetime.fromtimestamp(time.time() - 1800*2*24) # 24 hrs.
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

def print_yarn_apps():
  now = datetime.today()
  lastHr = datetime.today() - timedelta(hours = 1)   
  for app in get_service("YARN").get_yarn_applications(lastHr, now, filter_str = "state=RUNNING").applications:
    print app

def add_new_host():
  name = 'ip-172-31-1-41.ap-southeast-2.compute.internal'
  host = api.create_host(name, name, "172.31.1.41", "/default")
  xid = str(uuid.uuid4()).replace('-','')
  hdfs.create_role("hdfs-DATANODE-" + xid, "DATANODE", name)

def delete_host():
  api.delete_host()

def add_datanode_role():
  name = 'ip-172-31-9-17.ap-southeast-2.compute.internal'
  xid = str(uuid.uuid4()).replace('-','')
  #get_service("HDFS").create_role("hdfs-DATANODE-" + xid, "DATANODE", name)
  get_service("HDFS").create_role("hdfs-DATANODE-ac05b2e3cafc01531b61c12e304b2c04", "DATANODE", name)

def inspect_hosts():
  print "Inspecting hosts. This might take a few minutes."
  cmd = cm.inspect_hosts()
  while cmd.success == None:
      cmd = cmd.fetch()
  if cmd.success != True:
      print "Host inpsection failed!"
      exit(0)
  print "Hosts successfully inspected: \n" + cmd.resultMessage

def get_service(type):
  for service in cluster.get_all_services():
    if service.type == type:
      return service

def restart_hdfs():
  cmd = get_service("HDFS").restart()
  print cmd.active
  cmd = cmd.wait()
  print "Active: %s. Success: %s" % (cmd.active, cmd.success)

def main():
  #restart_hdfs()  
  #inspect_hosts()
  #print_yarn_apps()
  #inspect_hdfs()
  #list_roles()
  list_hosts()
  #add_datanode_role()
  delete_host()
  
if __name__ == "__main__": main()
