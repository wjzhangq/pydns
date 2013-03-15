# -*- coding:utf-8 -*-
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from cgi import parse_header, parse_multipart
from urlparse import parse_qs
import socket


class myHTTPHandle(BaseHTTPRequestHandler):
    host_dir = '../data'
    cmd_server = ("127.0.0.1", 5454)
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        path_array = [i for i in self.path.split('/') if not i==""]
        
        cur_path = ""
        content = "";
        if len(path_array) > 0:
            cur_path = path_array[0]
            if os.path.exists(self.host_dir + '/' + path_array[0]):
                fc = open(self.host_dir + '/' + path_array[0], 'r')
                content = fc.read()
                fc.close()
        
        f = open('./template/index.html','r');
        buffer = f.read()
        f.close()
        
        opt = []
        flist = self.list_host()
        opt.append('<option value="">创建新文件</option>')
        for i in flist:
            opt.append('<option value="'+ i +'">'+ i +'</option>')
            
        self.wfile.write(buffer % (cur_path,"".join(opt), content))
    
    def do_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                self.rfile.read(length), 
                keep_blank_values=1)
        else:
            postvars = {}
        
        rpath = "/"
        if not (postvars.has_key('content') and postvars.has_key('cnode')):
            print "less key";
            pass
        elif len(postvars['cnode'][0]) == 0:
            print "less key cnode";
            pass
        else:
            content = postvars['content'][0]
            cnode = postvars['cnode'][0]
            
            if len(content) > 0 :
                fc = open(self.host_dir + '/' +  cnode, 'w');
                fc.write(content)
                fc.close()
                rpath = "/" +  cnode
            else:
                if os.path.exists(self.host_dir + '/' +  cnode):
                    os.remove(self.host_dir + '/' +  cnode)
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(self.cmd_server)
            sock.settimeout(20)
            sock.sendall("load " +  cnode)
        self.send_response(301)
        self.send_header("Location", rpath)

    
    def list_host(self):
        files = [f for f in os.listdir(self.host_dir) if not f.startswith(".")]
        return files


if __name__ == "__main__":
    import os,sys
    root_path = os.path.realpath('../')
    sys.path.append(root_path)
    from settings import DEBUG, HTTP_SERVER,HOST_DIR, CMD_SERVER
    
    myHTTPHandle.host_dir = os.path.realpath(root_path + '/' + HOST_DIR)
    myHTTPHandle.cmd_server = CMD_SERVER

    
    http_server = HTTPServer(HTTP_SERVER, myHTTPHandle)
    try:
        http_server.serve_forever()
    except:
        pass
    
    http_server.server_close()