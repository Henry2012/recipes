#!/usr/bin/python
# -*- coding: utf-8 -*-

class SnsStat(object):
    def getTime(self):
        '''
            取当前的ms时间
        '''
        import time
        return time.time()

    def statReport(self, stat_url, start_time, params):
        '''
            上报数据
        '''
        try:
            import json
            import socket
        except ImportError:
            import simplejson as json

        endTime = self.getTime()
        params['time'] = round(endTime - start_time)
        params['timestamp'] = int(self.getTime())
        params['collect_point'] = "sdk-python-v3"
        stat_str = json.dumps(params)
        host_ip = socket.gethostbyname(stat_url),80

        if host_ip != stat_url:
            sock = socket.socket(type=socket.SOCK_DGRAM)
            if sock is None:
                return
            sock.sendto(stat_str, host_ip)
            sock.close()

def main():
    params={}
    params['appid']="222222"
    params['rc']="0"
    params['svr_name']="10.2.3.4"
    params['protocol']="http"
    params['interface']="user/get_app_friends"
    params['method']="get"
    params['pf']="qqconnect"

    stat = SnsStat()

    start_time = stat.getTime()

    stat.statReport("apistat.tencentyun.com", start_time, params)


if __name__ == "__main__":
    main()
