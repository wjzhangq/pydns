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
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print 'usage: client event[load,shutdown] body'
        sys.exit(0)
    cmd('%s %s' % (sys.argv[1], sys.argv[2]))