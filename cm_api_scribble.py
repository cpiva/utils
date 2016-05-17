import socket
from cm_api.api_client import ApiResource
 
CM_HOST = "ec2-52-63-31-127.ap-southeast-2.compute.amazonaws"
 
api = ApiResource(CM_HOST, username="admin", password="admin")

print api

