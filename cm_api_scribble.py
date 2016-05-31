import time
import uuid
import socket
from datetime import datetime, timedelta
from cm_api.api_client import ApiResource
from cm_api.endpoints.cms import ClouderaManager

CM_HOST = "ec2-52-64-91-202.ap-southeast-2.compute.amazonaws.com"
 
api = ApiResource(CM_HOST, username="admin", password="abc123")
cm = ClouderaManager(api)
cluster = api.get_cluster('cluster')

def list_hosts(self):
  for host in api.get_all_hosts('full'):
    print host.hostname

def list_roles(self):
  for role in hdfs.get_all_roles():
    print role

def list_services(self):
  for service in cluster.get_all_services():
    print service
    if service.type == "HDFS":
      hdfs = service
  print hdfs.name, hdfs.serviceState, hdfs.healthSummary
  print hdfs.serviceUrl
  for chk in hdfs.healthChecks:
    print "%s --- %s" % (chk['name'], chk['summary'])

def print_metrics(self):
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

def print_yarn_apps(self):
  now = datetime.today()
  lastHour = datetime.today() - timedelta(hours = 1)
  for service in cluster.get_all_services():
    print service
    if service.type == "YARN":
      yarn = service
  for app in yarn.get_yarn_applications(lastHour, now, filter_str = "state=RUNNING").applications:
    print app

def add_host(self):
  name = 'ip-172-31-1-41.ap-southeast-2.compute.internal'
  host = api.create_host(name, name, "172.31.1.41", "/default")
  xid = str(uuid.uuid4()).replace('-','')
  hdfs.create_role("hdfs-DATANODE-" + xid, "DATANODE", name)

def inspect_hosts(self):
  print "Inspecting hosts. This might take a few minutes."
  cmd = cm.inspect_hosts()
  while cmd.success == None:
      cmd = cmd.fetch()
  if cmd.success != True:
      print "Host inpsection failed!"
      exit(0)
  print "Hosts successfully inspected: \n" + cmd.resultMessage

def restart_hdfs(self):
  cmd = hdfs.restart()
  print cmd.active
  cmd = cmd.wait()
  print "Active: %s. Success: %s" % (cmd.active, cmd.success)
