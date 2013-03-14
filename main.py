if __name__ == "__main__":
    from cmd import CmdServer
    from hosts import Hosts
    from master_dns import MasterDns
    from proxy_dns import ProxyDnsServer
    from settings import HOST_DIR, MASTER_DNS, \
        MASTER_DNS_TIMEOUT, PROXY_DNS, CMD_SERVER
    import threading

    #master dns
    master = MasterDns(MASTER_DNS, MASTER_DNS_TIMEOUT)
    #hosts manager
    hosts = Hosts(HOST_DIR)
    #proxy dns
    proxy = ProxyDnsServer(PROXY_DNS, master, hosts)
    #cmd server
    cmd = CmdServer(CMD_SERVER, hosts, proxy)
    cmd.daemon_threads = True
    cmd_th = None
    try:
        #start cmd server
        cmd_th = threading.Thread(target=cmd.serve_forever, args=()).start()
        # start dns server
        proxy.serve_forever()
        print 'fff'
    except Exception:
        print 'kkk';
        import traceback
        import sys
        
        traceback.print_exc()
        sys.exit()
