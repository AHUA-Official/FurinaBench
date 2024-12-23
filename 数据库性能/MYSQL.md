# MySQL性能监控分析

## 一、使用show命令监控分析MySQL性能

```sql
# 最大连接使用数量
show status like 'Max_used_connections';
# 当前打开的连接数
show status like 'Threads_connected';
# 未从缓冲池读取的次数
show status like 'Innodb_buffer_pool_reads';
# 从缓冲池读取的次数
show status like 'Innodb_buffer_pool_read_requests';
# 缓冲池的总页数
show status like 'Innodb_buffer_pool_pages_total';
# 缓冲池的空闲页数
show status like 'Innodb_buffer_pool_pages_free';
# 缓存命中率 = ( 1 - innodb_buffer_poll_reads/innodb_buffer_pool_read_requests ) * 100%

# 锁等待的个数(累加数量，每次获取可以跟之前的数据相减，得到当前的数据)
show status like 'Innodb_row_lock_waits';
# 平均每次锁等待的时间
show status like 'Innodb_row_lock_time_avg';
# 查看是否存在表锁
show open TABLES where in_use>0;

# sql日志记录是否开启
show variables like 'slow_query_log';
# 查看慢sql阈值
show variables like 'long_query_time';
# 慢sql日志目录
show variables like 'slow_query_log_file';
# 格式化慢sql日志,显示耗时最长的10个sql信息(执行次数、平均执行时间、sql)
mysqldumpslow -s at -t 10 /export/data/mysql/log/slow.log

# insert数量
show status like 'Com_insert';
# delete数量
show status like 'Com_delete';
# update数量
show status like 'Com_update';
# select数量
show status like 'Com_select';

# 发送的吞吐量
show status like 'Bytes_sent';
# 接收的吞吐量
show status like 'Bytes_received';
# 总吞吐量 = bytes_sent+bytes_received
```

## 二、慢SQL分析

慢SQL指的是MySQL慢查询，具体指运行时间超过`long_query_time`值的SQL。我们常听MySQL中有二进制日志binlog、中继日志relaylog、重做回滚日志redolog、undolog  等。针对慢查询，还有一种慢查询日志slowlog，用来记录在MySQL中响应时间超过阀值的语句。慢SQL对实际生产业务影响是很严重的，所以对数据库SQL语句执行情况实施监控，提供准确的性能优化意见显得尤为重要。

设置慢SQL阈值、慢SQL日志位置后打开慢SQL记录开关，然后通过`mysqldumpslow`工具分析慢SQL日志。

```sql
# 取出使用最多的10条慢查询
./mysqldumpslow -s c -t 10 /export/data/mysql/log/slow.log
# 取出查询时间最慢的3条慢查询
./mysqldumpslow -s t -t 3 /export/data/mysql/log/slow.log
```

> 使用`mysqldumpslow`的分析结果不会显示完整的sql语句。

### 2.1 一些慢查询处理

1. 避免使用子查询；
2. 避免使用函数索引；
3. 使用in替换低效的or查询；
4. like模糊匹配(两个%)无法使用索引；
5. group by(分组统计)可以借助于order by null来避免排序带来的消耗；
6. 禁用不必要的order by排序;



## timeout相关参数

> 使用 `set {global | session} {arg_name}={value}` 命令来设置这些参数

```textfile
MariaDB [(none)]> show variables like '%timeout%';
+----------------------------+----------+
| Variable_name | Value |
+----------------------------+----------+
| connect_timeout | 10 |
| deadlock_timeout_long | 50000000 |
| deadlock_timeout_short | 10000 |
| delayed_insert_timeout | 300 |
| innodb_lock_wait_timeout | 50 |
| innodb_rollback_on_timeout | OFF |
| interactive_timeout | 100 |
| lock_wait_timeout | 31536000 |
| net_read_timeout | 30 |
| net_write_timeout | 60 |
| slave_net_timeout | 60 |
| thread_pool_idle_timeout | 60 |
| wait_timeout | 100 |
+----------------------------+----------+
13 rows in set (0.00 sec)
MySQL test@172.20.16.9:(none)> show variables like '%timeout%';
+-----------------------------+----------+
| Variable_name | Value |
+-----------------------------+----------+
| connect_timeout | 10 |
| delayed_insert_timeout | 300 |
| have_statement_timeout | YES |
| innodb_flush_log_at_timeout | 1 |
| innodb_lock_wait_timeout | 50 |
| innodb_rollback_on_timeout | OFF |
| interactive_timeout | 28800 |
| lock_wait_timeout | 31536000 |
| net_read_timeout | 30 |
| net_write_timeout | 60 |
| rpl_stop_slave_timeout | 31536000 |
| slave_net_timeout | 60 |
| wait_timeout | 28800 |
+-----------------------------+----------+
13 rows in set
```

## 参数说明

### connect_timeout

在获取连接阶段(authenticate)起作用，获取MySQL连接是多次握手的结果，除了用户名和密码的匹配校验外，还有IP->HOST->DNS->IP验证，任何一步都可能因为网络问题导致线程阻塞。为了防止线程浪费在不必要的校验等待上，超过connect_timeout的连接请求将会被拒绝。

### delayed_insert_timeout

为MyISAM INSERT DELAY设计的超时参数，表示INSERT DELAY handler线程在INSERT  DELAY语句终止前等待这个INSERT语句的时间，注意是表示insert  delay延迟插入的超时时间，不是insert语句。默认值是300S，从5.6.7开始被弃用（因为delayed  insert功能被弃用）后续版本将移除。

### innodb_lock_wait_timeout(innodb的dml操作的行级锁的等待时间)

innodb使用这个参数能够有效避免在资源有限的情况下产生太多的锁等待；指的是事务等待获取资源时等待的最长时间，超过这个时间还未分配到资源则会返回应用失败；参数的时间单位是秒，最小可设置为1s(一般不会设置得这么小)，最大可设置1073741824秒(34年)，默认安装时这个值是50s，超过这个时间会报 ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting  transaction。

### innodb_rollback_on_timeout

默认情况下innodb_lock_wait_timeout 超时后只是超时的sql执行失败，整个事务并不回滚，也不做提交，如需要事务在超时的时候回滚，则需要设置innodb_rollback_on_timeout=ON，该参数默认为OFF。

### interactive_timeout & wait_timeout

在连接空闲阶段(sleep)起作用，即使没有网络问题，也不能允许客户端一直占用连接。对于保持sleep状态超过了wait_timeout(或interactive_timeout，取决于client_interactive标志)的客户端，MySQL会主动断开连接。

### lock_wait_timeout

获取MDL锁的等待时间，默认值是31536000秒=1年。 凡是需要获取MDL锁的操作都受到这个参数的影响，不单单是DDL语句，包含在表上的DML、DDL操作，以及视图、存储过程、存储函数、lock  table，flush table with read lock语句等。但不适用于隐式访问系统表的语句，如：grant和revoke等。

### net_read_timeout & net_write_timeout

在连接繁忙阶段(query)起作用，即使连接没有处于sleep状态，即客户端忙于计算或者存储数据，MySQL也选择了有条件的等待。在数据包的分发过程中，客户端可能来不及响应（发送、接收、或者处理数据包太慢）。为了保证连接不被浪费在无尽的等待中，MySQL也会选择有条件（net_read_timeout和net_write_timeout）地主动断开连接。 这个参数只对TCP/IP链接有效，只针对在Activity状态下的线程有效。

### slave_net_timeout

Slave判断主库是否挂掉的超时设置，在设定时间内依然没有获取到Master的回应就认为Master已经挂掉了，后续根据超时重连参数设置进行重连主库的操作。默认值：3600s。

### innodb_flush_log_at_timeout

5.6.6引入，参数innodb_flush_log_at_trx_commit=1时，此超时参数不起作用，当innodb_flush_log_at_trx_commit=0/2时才起作用。5.6.6之后表示每innodb_flush_log_at_timeout秒一次的频率刷新redo log(在5.6.6之前是固定每秒一次刷新redo log，5.6.6之后刷新频率可以通过这个参数设置，当然，这个参数本身默认值也是1S)。

### rpl_semi_sync_master_timeout

为semi-sync复制时，主库在某次事务提交时，如果等待超过rpl_semi_sync_master_timeout多秒之后仍然没有接收到任何从库做回包响应，那么主库自动降级为异步复制模式，当主库探测到有备库恢复回包时，主库自动恢复到semi-sync复制模式。默认值为10000毫秒=10秒。

### rpl_stop_slave_timeout

5.6.13之后引入的参数，控制stop slave 的执行时间，在重放一个大的事务的时候,突然执行stop slave,命令 stop  slave会执行很久,这个时候可能产生死锁或阻塞,严重影响性能，可以通过rpl_stop_slave_timeout参数控制stop slave 的执行时间。默认值是31536000秒=1年。