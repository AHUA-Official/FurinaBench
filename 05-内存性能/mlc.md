因为是Intel 公司自己出的  所以在I搭载Intel芯片 上的裸板进行内存性能测试的时候  这个的指标比ebbizy好看一些  当然 其实ebizzy做的更好  因为人家是多线程的那啥 更符合高并发的要求 







安装 部署 



wget   http://smb.zstack.io/mirror/lei.zhang/mlc_v3.11b.tgz

tar -zxvf   [mlc_v3.11b.tgz](http://smb.zstack.io/mirror/lei.zhang/mlc_v3.11b.tgz) 

cd Linux 

ls

./mlc  









之后就会自动启动一个整套的mlc流程了  



```
[root@172-25-12-8 Linux]# ./mlc
Intel(R) Memory Latency Checker - v3.11b
Measuring idle latencies for sequential access (in ns)...
                Numa node
Numa node            0
       0          83.8

Measuring Peak Injection Memory Bandwidths for the system
Bandwidths are in MB/sec (1 MB/sec = 1,000,000 Bytes/sec)
Using all the threads from each core if Hyper-threading is enabled
Using traffic with the following read-write ratios
ALL Reads        :      34419.9
3:1 Reads-Writes :      32227.1
2:1 Reads-Writes :      31617.5
1:1 Reads-Writes :      29912.5
Stream-triad like:      29556.1

Measuring Memory Bandwidths between nodes within system
Bandwidths are in MB/sec (1 MB/sec = 1,000,000 Bytes/sec)
Using all the threads from each core if Hyper-threading is enabled
Using Read-only traffic type
                Numa node
Numa node            0
       0        34915.2

Measuring Loaded Latencies for the system
Using all the threads from each core if Hyper-threading is enabled
Using Read-only traffic type
Inject  Latency Bandwidth
Delay   (ns)    MB/sec
==========================
 00000  383.60    35243.8
 00002  392.71    35042.9
 00008  385.82    35177.1
 00015  389.95    35023.8
 00050  376.43    35268.1
 00100  359.80    35165.4
 00200  136.70    28180.5
 00300  114.95    19704.3
 00400  104.93    15204.2
 00500   98.29    12482.7
 00700   96.44     9173.9
 01000   93.99     6734.8
 01300   92.15     5340.9
 01700   91.35     4296.1
 02500   89.33     3155.6
 03500   88.44     2480.5
 05000   87.97     1951.8
 09000   87.33     1419.1
 20000   87.02     1042.6

Measuring cache-to-cache transfer latency (in ns)...
Local Socket L2->L2 HIT  latency        54.5
Local Socket L2->L2 HITM latency        54.9





也可以自己指定想要测试的对象  

./mlc --latency_matrix
结果

        Numa node
Numa node        0       1  
       0      82.2   129.6  
       1     131.1    81.6
表示node之间/内部的空闲内存访问延迟矩阵，以ns为单位

带宽
带宽反映了单位时间的传输速率马路越宽，就不会堵车了。带宽反映了单位时间的传输速率

Measuring Peak Injection Memory Bandwidths for the system
Bandwidths are in MB/sec (1 MB/sec = 1,000,000 Bytes/sec)
Using all the threads from each core if Hyper-threading is enabled
Using traffic with the following read-write ratios
ALL Reads        :  69143.9 
3:1 Reads-Writes :  61908.4 
2:1 Reads-Writes :  60040.5 
1:1 Reads-Writes :  54517.6 
Stream-triad like:  57473.4 
r:w 表示不同读写比下的内存带宽

一般情况下，内存的写速度慢于读取速度（Talk is easy, show me the CODE）

所以当读写比下降时，带宽会下降（路窄了，塞车了）

问题分析：如果带宽急剧下降，可能是写入程序增多；或者是写入程序出问题，速度太慢了

测试样例

查询存访问带宽 指令（单独判断numa节点间内存访问是否正常还可以使用 ）

./mlc --bandwidth_matrix
结果

Measuring Memory Bandwidths between nodes within system 
Bandwidths are in MB/sec (1 MB/sec = 1,000,000 Bytes/sec)
Using all the threads from each core if Hyper-threading is enabled
Using Read-only traffic type
        Numa node
Numa node        0       1  
       0    35216.6 32537.9 
       1    31875.1 35048.5 
问题分析：如果副对角线数值相差过大，表明两个node相互访问的带宽差距较大

解决方法：出现不平衡的时候一般从内存插法、内存是否故障以及numa平衡等角度进行排查

内存访问带宽和内存延迟的关系（读操作）
Measuring Loaded Latencies for the system
Using all the threads from each core if Hyper-threading is enabled
Using Read-only traffic type
Inject  Latency Bandwidth
Delay   (ns)    MB/sec
==========================
 00000  523.74    69057.4
 00002  589.55    68668.7
 00008  686.99    68571.4
 00015  549.87    68873.6
 00050  575.48    68673.0
 00100  524.74    68877.5
 00200  197.61    64225.8
 00300  131.60    47141.0
 00400  110.39    36803.0
 00500  117.32    30135.2
 00700  100.90    22179.1
 01000  100.93    15762.8
 01300   91.74    12351.6
 01700   98.61     9475.2
 02500   86.66     6927.8
 03500   88.13     5132.6
 05000   87.68     3818.6
 09000   85.36     2473.5
 20000   84.83     1538.7
可以观察内存在负载压力下的响应变化，以及是否在到达一定带宽时，出现不可接受的内存响应时间

测量CPU cache到CPU cache之间的访问延迟
Measuring cache-to-cache transfer latency (in ns)...
Local Socket L2->L2 HIT  latency    38.6
Local Socket L2->L2 HITM latency    43.6
Remote Socket L2->L2 HITM latency (data address homed in writer socket)
        Reader Socket
Writer Socket         0         1
            0         -     133.4
            1     133.7         -
Remote Socket L2->L2 HITM latency (data address homed in reader socket)
        Reader Socket
Writer Socket         0         1
            0         -     133.5
            1     133.7         -
峰值带宽
指令

mlc --peak_bandwidth
结果

Using buffer size of 100.000MB/thread for reads and an additional 100.000MB/thread for writes

Measuring Peak Memory Bandwidths for the system
Bandwidths are in MB/sec (1 MB/sec = 1,000,000 Bytes/sec)
Using all the threads from each core if Hyper-threading is enabled
Using traffic with the following read-write ratios
ALL Reads        :    50035.2
3:1 Reads-Writes :    48119.3
2:1 Reads-Writes :    47434.3
1:1 Reads-Writes :    48325.5
Stream-triad like:    44029.0
空闲内存延迟
指令

mlc --idle_latency
结果

Using buffer size of 200.000MB
Each iteration took 260.5 core clocks (    113.3    ns)
有负载内存延时
指令

mlc --loaded_latency
结果

Using buffer size of 100.000MB/thread for reads and an additional 100.000MB/thread for writes

Measuring Loaded Latencies for the system
Using all the threads from each core if Hyper-threading is enabled
Using Read-only traffic type
Inject    Latency    Bandwidth
Delay    (ns)    MB/sec
==========================
 00000    217.32      49703.4
 00002    258.98      49482.4
 00008    217.48      49908.1
 00015    220.12      49973.7
 00050    206.33      49185.7
 00100    174.02      43811.8
 00200    141.63      27651.1
 00300    130.65      19614.6
 00400    126.05      15217.0
 00500    122.70      12506.0
 00700    121.46       9253.0
 01000    120.55       6690.6
 01300    118.75       5314.9
 01700    120.18       4148.7
 02500    119.53       3055.7
 03500    119.60       2349.4
 05000    116.60       1816.9
 09000    116.17       1257.8
 20000    116.87        867.6
其余操作（未完待续
测量指定node之间的访问延迟

测量CPU cache的访问延迟

测量cores/Socket的指定子集内的访问带宽

测量不同读写比下的带宽

指定随机的访问模式以替换默认的顺序模式进行测量

指定测试时的步幅
```



适用于分析不同负载下系统的内存性能。以下是 MLC 工具的六种主要工作模式及其对应命令：

1. **延迟矩阵**：打印本地和跨插槽内存延迟矩阵。

   ```
   ./mlc --latency_matrix
   ```

2. **带宽矩阵**：打印本地和跨插槽内存带宽矩阵。

   ```
   ./mlc --bandwidth_matrix
   ```

3. **峰值注入带宽**：测量平台在不同读写比率下的峰值内存带宽。

   ```
   ./mlc --peak_injection_bandwidth
   ```

4. **空闲延迟**：测量平台的空闲内存延迟。

   ```
   ./mlc --idle_latency
   ```

5. **加载延迟**：测量平台的加载内存延迟。

   ```
   ./mlc --loaded_latency
   ```

6. **缓存到缓存延迟**：测量平台的缓存到缓存数据传输延迟。

   ```
   ./mlc --c2c_latency
   ```

7. **内存带宽扫描**：打印每个 1GB 地址范围内的内存带宽。

   ```
   ./mlc --memory_bandwidth_scan
   ```

## 常用选项

以下选项可与上述命令结合使用，以自定义分析：

- `-a`：在所有可用 CPU 上测量空闲延迟；如果指定 `-X`，则每个核心仅使用一个线程。
- `-b`：缓冲区大小（默认=100000 KiB）。
- `-e`：不修改硬件预取器状态。
- `-r`：使用随机访问获取延迟。
- `-X`：每个核心仅使用一个超线程进行带宽测量。
- `-L`：使用大页面（2MB），假设已启用。
- `-Wn`：指定读写比率（例如：`-W2` 表示 2:1 的读写比率）。
- `-Z`：使用 AVX-512 64 字节加载/存储指令。

## 完整选项列表

以下是 MLC 支持的所有选项：
`./mlc [模式] [选项] `

- `-a`：测量所有可用 CPU 的空闲延迟。
- `-b`：缓冲区大小（默认=100000 KiB）。
- `-B`：打印每线程吞吐量。
- `-c`：将延迟测量线程绑定到核心 #n。
- `-d`：注入请求到内存之间的延迟周期（默认=0），值越高带宽越低。
- `-D`：延迟线程的随机访问范围（默认=4096）。
- `-e`：不修改硬件预取器状态。
- `-f`：延迟直方图桶大小。
- `-g`：指定用于延迟测量的输入文件。
- `-h`：在 Windows 上使用大页面（1GB）。
- `-i`：从核心 #n 初始化内存。
- `-I`：检查读取数据的完整性，仅适用于所有读取的加载延迟模式。
- `-j`：从 NUMA 节点 #n 初始化内存。
- `-J`：指定创建 mmap 文件的目录（默认为不创建文件）。
- `-k`：指定核心编号列表（例如：`3-6,9-13,19,20`）。
- `-l`：步幅长度（默认=64 字节）。
- `-L`：使用大页面（2MB）。
- `-m`：指定用于带宽测量的 CPU 掩码（建议使用 `-k` 选项）。
- `-M`：使用特定模式初始化内存。
- `-n`：用于随机带宽生成的随机访问范围。
- `-o`：指定用于每线程分配选项的输入文件。
- `-p`：指定核心列表，用于防止相应插槽进入睡眠状态。
- `-P`：使用 CLFLUSH 驱逐存储到持久内存。
- `-Q`：使用 CLFLUSH 驱逐存储到任意内存。
- `-r`：延迟线程的随机访问读取。
- `-R`：生成只读负载。
- `-s`：指定对象名称，可由外部应用程序触发以同步加载延迟流量。
- `-S`：将第三线程绑定到核心 #n。
- `-t`：测试时间（默认=2 秒）。
- `-T`：仅进行吞吐量测试，不测量延迟。
- `-u`：加载延迟测试中，所有加载生成线程共享同一缓冲区。
- `-U`：生成带宽时的随机访问（默认关闭）。
- `-v`：打印详细输出。
- `-w`：将 hit/hitm 写线程绑定到核心 #n。
- `-Wn`：指定读写比率。
- `-x`：迭代次数（以百万次为单位），指定时不应指定 `-t`。
- `-X`：每个核心仅使用一个超线程进行带宽测量。
- `-Y`：使用 AVX2 32 字节加载/存储指令。
- `-Z`：使用 AVX-512 64 字节加载/存储指令。

## 常见用法示例

1. **测量延迟矩阵**：

   ```
   ./mlc --latency_matrix
   ```

2. **测量峰值注入带宽**：

   ```
   ./mlc --peak_injection_bandwidth
   ```

3. **测量加载延迟**：

   ```
   ./mlc --loaded_latency
   ```

4. **打印详细输出**：

   ```
   ./mlc --latency_matrix -v
   ```

5. **使用大页面测量延迟**：

   ```
   ./mlc --latency_matrix -L
   ```

待完善
