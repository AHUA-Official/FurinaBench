## 性能分析工具

| 工具      | 内容               | 参数                          | 基本命令                                         |
| --------- | ------------------ | ----------------------------- | ------------------------------------------------ |
| unixbench | CPU综合性能        | 单核、多核                    | ./Run -c 1 -i 3 -q                               |
| stream    | 内存               | 内存带宽                      | ./stream.o                                       |
| netperf   | TCP_RR回环         | TCP_RR                        | netperf -t TCP_RR -H 127.0.0.1 -l 1              |
| ebizzy    | 合成服务器基准测试 | ./ebizzy                      | ./ebizzy                                         |
| ping      | 网络连通性测试     |                               |                                                  |
| iperf3    | 网络测试           | (tcp,udp)x(单,多线程)x(1g,ng) | iperf3 -c {ip_target} {thread}{type} -t 30{size} |
| fio       | 磁盘性能           | (1M顺序,4k随机)x(读,写,延时)  |                                                  |

![See the source image](http://smb.zstack.io/mirror/performancedoc/performancemanualpic/23/214631471031997829202115255188174714924250_gopic_1635139608R-C.png)

## 进行性能分析

## 调优项目

### 调优准备！注意事项！！

1. 永远别在生产系统上调优
2. 控制变量，避免其它环境改变对结果造成影响
3. 反复多次测试提升性能的参数，测试次数少的结果不可靠
4. 调优执行前明白自己在做什么
5. 相关工具使用详见: http://www.longtao.fun/metaverse/linuxperformanceanalysis/

### CPU性能调优

1. 使用ps -ef来确保没有**不必要**的进程程序在后台运行(严重的有病毒和挖矿程序)，如果有，`kill掉`
2. 通过`top`找到非关键的、CPU密集型(CPU占用率高)进程，然后用`renice`修改它的优先级,或者使用`cron`让它在非高峰的时候运行。
3. 使用`taskset`绑定进程到指定cpu，避免进城在不同cpu之间切换引起cache刷新产生性能开销，若为多NUMA NODE 架构，尽量将相关进城绑定在同一NODE节点中
4. 确认你的应用是否能高效利用多CPU性能，若可以请提高CPU数量，若不可以，请更换更高频率CPU
5. 部分CPU指令集会导致性能下降，例如AVX512指令会导致CPU过热降频
6. 关闭一些安全补丁，如幽灵熔断
7. 使用CGroup进行CPU隔离

### 内存性能调优

1. 如CPU性能调优一样，限制非必要进程的运行
2. 物理机上使用多通道内存
3. 开启或关闭大页内存
4. 修改默认内存大小
5. 修改swap分区位置以及相关参数，例如：`vm.swappiness`
6. 修改`page-out`内存分页写入磁盘比率
7. 使用CGroup进行内存隔离

### 磁盘IO性能调优

1. 做RAID
2. 添加RAM，提升系统磁盘缓冲
3. 使用逻辑卷分区
4. 修改电梯算法
5. 更换更好的磁盘
6. http://www.longtao.fun/metaverse/diskperformanceestimation/

### 网络性能调优

1. 使用bond，lacp等
2. 开启网卡offload功能
3. 若网卡允许，开启DPDK

# 术语表

**并发数**：多个用户同时访问服务器站点的连接数

**吞吐量**：单位时间内系统处理的请求数量

**系统负载**：指服务器中正在执行和等待被CPU 执行的进程数目总和，是反映系统忙闲程度的重要指标

**延迟**：**Latency**又称**潜伏时间**、**响应时间**：记录收到响应和发出请求之间的时间差来计算系统响应时间

**IOPS**：I/O per Second，每秒处理的IO操作，一般用于度量磁盘IO的读写性能

**TPS**： Transaction Per Second，系统每秒处理的事务数量

**RPS**：Request per Second，每秒执行的请求数量，一般在Web系统中，指服务器每秒中处理的Request

**QPS**：Query per Second，每秒执行的请求数量，一般使用在数据库系统中，指数据库服务器每秒中处理的Query语句数量

**PPS**：Package per Second，每秒发送/接收的package数，一般用于网络传输吞吐量

待完善
