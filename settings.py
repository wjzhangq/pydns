# -*- coding:utf-8 -*-
# is debug
DEBUG = True

#sys cmd password
SYS_PASSWORD = 'hello'

# master dns server
MASTER_DNS = (
    ('10.103.10.1', 53),
    ('10.103.10.2', 53),
)

# proxy dns server
PROXY_DNS = ('0.0.0.0', 1053)
#message entrance
CMD_SERVER = ('0.0.0.0', 5454)
#http server
HTTP_SERVER = ('0.0.0.0', 8000)

# master dns time out, in seconds
MASTER_DNS_TIMEOUT = 2

# # base hosts file
# BASE_HOSTS = '../db/hosts.base'
# # special hosts directory
HOST_DIR = './data/'
# # ip directory
#IP_DIR = './data/' 

