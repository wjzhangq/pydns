# -*- coding:utf-8 -*-

from SocketServer import BaseRequestHandler, ThreadingUDPServer
from cStringIO import StringIO
from protocol import DnsRequest, Answer, DnsResponse
from settings import DEBUG
import time

class ProxyDnsHandler(BaseRequestHandler):
   
    def handle(self):
        hosts = self.server.hosts
        master = self.server.master 
        
        data, sock = self.request
        
        req = DnsRequest.parse(StringIO(data))
        domain = req.queries[0].name
        
        ip = hosts.get_ip(domain) 
        if ip:
            self.log('%s -- [%s] %s %s %s' % (self.client_address[0], time.ctime(), domain, 'Found', ip))
            header = req.header
            header.answer_rrs = 1
            query = req.queries[0]
            answer = Answer(domain, Answer.TYPE_A, Answer.CLASS_IN, 60, ip)
            resp = DnsResponse(header, [query], [answer]).serialize()
        else:
            self.log('%s -- [%s] %s %s' % (self.client_address[0], time.ctime(), domain, 'Not Found'))
            resp = master.query(data)
        sock.sendto(resp, self.client_address)
    
    def log(self, message):
        if DEBUG:
            print message

    
class ProxyDnsServer(ThreadingUDPServer):
    def __init__(self, local, master, hosts):
        self.local = local
        self.master = master
        self.hosts = hosts
        ThreadingUDPServer.__init__(self, local, ProxyDnsHandler)
