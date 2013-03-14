# -*- coding:utf-8 -*-
# 远程代理查询代码
import socket

class MasterDns(object):

    def __init__(self, servers=[], timeout=1):
        '''
            servers: tuple of (host,port) tuple e.g. (('1.1.1.1',53),('2.2.2.2',53))
            timeout: the special timeout, in seconds
        '''
        self.servers = servers
        self.timeout = timeout
        self._pointer = 0
    
    def query(self, data):
        try_count = 0
        while(try_count < 2):
            try:
                return self._query(self._poll(), data)
            except Exception as e:
                print e
                try_count = try_count + 1
        return ''
    
    def _poll(self):
        pointer = self._pointer % len(self.servers)
        self._pointer = pointer + 1
        return self.servers[pointer]

    def _query(self, server, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(server)
        sock.settimeout(self.timeout)
        sock.sendall(data)
        resp = sock.recv(65535)
        return resp