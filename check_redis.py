#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenmingle'

import sys
import subprocess
import json

try:
    import redis
except Exception, e:
    print 'pip install redis'
    sys.exit(1)


class Redis(object):
    def __init__(self, host, port, password=None):
        self.host = host
        self.port = port
        self.password = password
        if self.password:
            self.rds = redis.StrictRedis(host=host, port=port, password=self.password)
        else:
            self.rds = redis.StrictRedis(host=host, port=port)
        try:
            self.info = self.rds.info()
        except Exception, e:
            self.info = None

    def redis_connections(self):
        try:
            return self.info['connected_clients']
        except Exception, e:
            return 0

    def redis_connections_usage(self):
        try:
            curr_connections = self.redis_connections()
            max_clients = self.parse_config('maxclients')
            rate = float(curr_connections) / float(max_clients)
            return "%.2f" % (rate * 100)
        except Exception, e:
            return 0

    def redis_used_memory(self):
        try:
            return self.info['used_memory']
        except Exception, e:
            return 0

    def redis_memory_usage(self):
        try:
            used_memory = self.info['used_memory']
            max_memory = self.info['maxmemory']
            system_memory = self.info['total_system_memory']
            if max_memory:
                rate = float(used_memory) / float(max_memory)
            else:
                rate = float(used_memory) / float(system_memory)
            return "%.2f" % (rate * 100)
        except Exception, e:
            return 0

    def redis_ping(self):
        try:
            return self.rds.ping()
        except Exception, e:
            return False

    def rejected_connections(self):
        try:
            return self.info['rejected_connections']
        except Exception, e:
            return 999

    def evicted_keys(self):
        try:
            return self.info['evicted_keys']
        except Exception, e:
            return 999

    def blocked_clients(self):
        try:
            return self.info['blocked_clients']
        except Exception, e:
            return 0

    def ops(self):
        try:
            return self.info['instantaneous_ops_per_sec']
        except Exception, e:
            return 0

    def hitRate(self):
        try:
            misses = self.info['keyspace_misses']
            hits = self.info['keyspace_hits']
            rate = float(hits) / float(int(hits) + int(misses))
            return "%.2f" % (rate * 100)
        except Exception, e:
            return 0

    def parse_config(self, type):
        try:
            return self.rds.config_get(type)[type]
        except Exception, e:
            return None

    def test(self):
        print 'Redis ping: %s' % self.redis_ping()
        print 'Redis alive: %s ' % check_alive(self.host, self.port)
        print 'Redis connections: %s' % self.redis_connections()
        print 'Redis blockedClients %s' % self.blocked_clients()
        print 'Redis connectionsUsage: %s%%' % self.redis_connections_usage()
        print 'Redis memoryUsage: %s' % self.redis_used_memory()
        print 'Redis memoryUsageRate: %s%%' % self.redis_memory_usage()
        print 'Redis evictedKeys: %s' % self.evicted_keys()
        print 'Redis rejectedConnections: %s' % self.rejected_connections()
        print 'Redis ops: %s' % self.ops()
        print 'Redis hitRate: %s%%' % self.hitRate()


def check_alive(host, port):
    cmd = 'nc -z %s %s > /dev/null 2>&1' % (host, port)
    return subprocess.call(cmd, shell=True)


def parse(type, host, port, password):
    rds = Redis(host, port, password)
    if type == 'connections':
        print rds.redis_connections()
    elif type == 'connectionsUsage':
        print rds.redis_connections_usage()
    elif type == 'blockedClients':
        print rds.blocked_clients()
    elif type == 'ping':
        print rds.redis_ping()
    elif type == 'alive':
        print check_alive(host, port)
    elif type == 'memoryUsage':
        print rds.redis_used_memory()
    elif type == 'memoryUsageRate':
        print rds.redis_memory_usage()
    elif type == 'rejectedConnections':
        print rds.rejected_connections()
    elif type == 'evictedKeys':
        print rds.evicted_keys()
    elif type == 'hitRate':
        print rds.hitRate()
    elif type == 'ops':
        print rds.ops()
    else:
        rds.test()

if __name__ == '__main__':
    try:
        type = sys.argv[1]
        host = sys.argv[2]
        port = sys.argv[3]
        if sys.argv.__len__() >=5:
            password = sys.argv[4]
        else:
            password = None
    except Exception, e:
        print "Usage: python %s type 127.0.0.1 6379" % sys.argv[0]
        sys.exit(1)
    parse(type, host, port, password)
