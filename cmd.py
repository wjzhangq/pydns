from SocketServer import BaseRequestHandler, ThreadingUDPServer
from settings import SYS_PASSWORD
from settings import DEBUG
import time

#------------------------#
# Message Struct (type, event, body)
# Cmd Result     (result, body)
#------------------------#

class CmdHandler(BaseRequestHandler):
    
    def handle(self):
        hosts = self.server.hosts
        data, sock = self.request
        
        msg = data.split()
        if(len(msg) != 2):
            sock.sendto('UNKNOWN', self.client_address)
        else:
            event , body = msg
            self.log('%s -- [%s] %s' % (self.client_address[0], time.ctime(), data))
            if event == 'load':
                if body == '*':
                    hosts.load_all_hosts(body)
                    sock.sendto('load all data', self.client_address)
                    return
                else:
                    ret = hosts.load_hosts(body)
                    reply = body + ' Not Exist'
                    if ret > 0:
                        reply = body + ' reload ok'
                    else:
                        if ret < 0:
                            reply = body + ' delete ok'
                    sock.sendto(reply, self.client_address)
                    return
            if event == 'shutdown':
                if body == SYS_PASSWORD:
                    sock.sendto('shutdown now', self.client_address)
                    self.server.proxy_dns.shutdown()
                    self.server.shutdown()
                    return
                else:
                    sock.sendto('Password need', self.client_address)
                    return

            sock.sendto('UNKNOWN ' + event , self.client_address)
            
    def log(self, message):
        if DEBUG:
            print message

class CmdServer(ThreadingUDPServer):
    def __init__(self, server, hosts, proxy_dns):
        self.hosts = hosts
        self.proxy_dns = proxy_dns
        ThreadingUDPServer.__init__(self, server, CmdHandler)
