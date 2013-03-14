import os
from settings import DEBUG

class Hosts(object):

    def __init__(self, host_dir):
        self.host_dir = host_dir
        
        self.repository_hosts = {} #{hosts_name:[(domain,ip)]}

        self.load_all_hosts()
    
    def get_ip(self,domain):
        ret = None
        for i in self.repository_hosts:
            ret = self._get_ip(domain, self.repository_hosts.get(i)) # load from special hosts
            if not ret == None:
                self.log('%s -- hit in %s' % (domain, i)) 
                break
                  
        return ret

    def _get_ip(self, domain, hosts_list):
        if not hosts_list:
            return None
        for host in hosts_list:
            if host[0].startswith('*'):
                    if domain.endswith(host[0][2:]):
                        return host[1]
            else:
                if host[0] == domain:
                    return host[1]
        return None
    
    def load_all_hosts(self):
        files = [f for f in os.listdir(self.host_dir) if not f.startswith(".")]
        for i in files:
            self.load_hosts(i)
    
    def load_hosts(self, hosts_name):
        ret = 0
        if os.path.exists(self.host_dir + hosts_name):
            self.repository_hosts[hosts_name] = self._load_hosts(self.host_dir + hosts_name)
            ret = 1
        else:
            if self.repository_hosts.has_key(hosts_name):
                del self.repository_hosts[hosts_name]
                ret = -1
        
        return ret

    def _load_hosts(self, file):
        # get hosts line
        lines = [line.strip() for line in open(file) if line.strip() != '' and not line.strip().startswith('#')]
        # get domain and ip 
        domains = []
        for line in lines:
            info = line.split()
            domains.extend([(h.strip(), info[0].strip()) for h in info[1:] if not h.strip().startswith("#") ])
        return domains
        
    def log(self, message):
        if DEBUG:
            print message

if __name__ == "__main__":
    #test
    from settings import HOST_DIR
    hosts = Hosts(HOST_DIR)
    print hosts.get_ip('www.baidu.com')
    print hosts.get_ip('a.youku.com')