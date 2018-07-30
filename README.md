# 一个简单的监控redis性能的python脚本


## [上一篇](http://blog.51cto.com/legehappy/2145967)已经讲了如何监控memcached了，现在也顺带讲如何监控redis。

## 首先介绍下监控redis那些信息：
* Redis ping：检验ping
* Redis alive：查看检查端口是否alive
* Redis connections：查看连接数
* Redis blockedClients：正在等待阻塞客户端数量
* Redis connectionsUsage：redis的连接使用率
* Redis memoryUsage：redis内存使用量
* Redis memoryUsageRate：redis内存使用率
* Redis evictedKeys：运行以来删除过的key的数量
* Redis rejectedConnections：拒绝连接数
* Redis ops：redis的OPS
* Redis hitRate：redis命中率



### 安装需要的环境

```
pip install redis
```


### 测试脚本，查看监控redis信息（假如redis没设置密码，可不填密码执行）：

``` 
/bin/python /home/python/check_redis.py test 192.168.4.18 6379 password
Redis ping: True
Redis alive: 0
Redis connections: 447
Redis blockedClients 0
Redis connectionsUsage: 4.47%
Redis memoryUsage: 2885122048
Redis memoryUsageRate: 17.32%
Redis evictedKeys: 0
Redis rejectedConnections: 0
Redis ops: 1050
Redis hitRate: 71.87%
```

### 最后加入到zabbix自定义key上


```
cat /etc/zabbix/zabbix_agentd.d/redis.conf
# Redis
UserParameter=redis.stats[*],/bin/python /home/python/check_redis.py $1 192.168.4.18 6379 password
```
