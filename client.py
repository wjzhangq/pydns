from settings import CMD_SERVER
import socket
import sys

def cmd(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(CMD_SERVER)
    sock.settimeout(20)
    sock.sendall(data)
    print sock.recv(65535)
    sock.close()
    
if len(sys.argv) != 4:
    print 'usage: client type event body'
    sys.exit(0)
cmd('%s %s %s' % (sys.argv[1], sys.argv[2], sys.argv[3]))