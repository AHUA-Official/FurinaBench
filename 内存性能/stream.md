```
#!/bin/bash

cd   /etc
cd   yum.repo.d
wget     http://smb.zstack.io/mirror/lei.zhang/linuxTESTshell/repo/aliyun.repo
# rm -rf /zapt   
# yum install git -y
# cd /

# mkdir /zapt
# cd /zapt
# git clone http://dev.zstack.io:9080/longtao.wu/apt_tools.git
# rm -rf /apt_tools/.git  
# ## 安装iperf3
# yum install iperf3 -y
# # 安装netperf
# wget -c http://smb.zstack.io/mirror/mingmin.wen/tools/netperf-2.7.0-1.el7.lux.x86_64.rpm
# rpm -i netperf-2.7.0-1.el7.lux.x86_64.rpm
# rm -rf netperf-2.7.0-1.el7.lux.x86_64.rpm
cd /zapt
cd apt_tools
cd  STREAM
./stream.o
./stream.o |grep "Triad"   
#  #   获得的数据如下所示
#  -------------------------------------------------------------
# Function    Best Rate MB/s  Avg time     Min time     Max time
# Copy:           19405.7     0.008844     0.008245     0.010708
# Scale:          20967.6     0.008312     0.007631     0.010818
# Add:            21871.9     0.011750     0.010973     0.015864
# Triad:          22111.7     0.011133     0.010854     0.011556
#拿出Triad这一行来     求写入txt文件stram。txt中    记录十次    最后记录下每列的平均值
# 运行
# ./stream.o
# 进行测试，测试十遍并记录
# Triad
# 的值，最终对十次测试数据取平均值

# 初始化计数器和数组用于存储数据


cat stream_temp.txt

# count=0

# declare -a triad_rates

# declare -a triad_avg_times

# declare -a triad_min_times

# declare -a triad_max_times


# # 循环运行stream.o十次

# for ((i=1; i<=10; i++)); do

#     ./stream.o | grep "Triad" >> stream_temp.txt

#     # 读取最新一次的Triad行数据

#     read -r _ _ rate _ avg_time _ min_time _ max_time < <(tail -n 1 stream_temp.txt)

#     # 存储数据到数组

#     triad_rates+=("$rate")

#     triad_avg_times+=("$avg_time")

#     triad_min_times+=("$min_time")

#     triad_max_times+=("$max_time")

# done


# # 清理临时文件

# rm -f stream_temp.txt


# # 打开或创建stream.txt文件准备写入数据

# # echo "Triad Test Results (Average of 10 runs)" > stream.txt

# # echo "Function, Best Rate MB/s, Avg time, Min time, Max time" >> stream.txt

# # echo "Triad, ${triad_rates[*]}, ${triad_avg_times[*]}, ${triad_min_times[*]}, ${triad_max_times[*]}" >> stream.txt
# # ./stream.o |grep "Triad"  
# ./stream.o | grep "Triad" > stream.txt
# # 计算平均值

# average_rate=$(awk '{sum+=$1} END{print sum/NR}' <<< "${triad_rates[*]}")

# average_avg_time=$(awk '{sum+=$1} END{print sum/NR}' <<< "${triad_avg_times[*]}")

# average_min_time=$(awk '{sum+=$1} END{print sum/NR}' <<< "${triad_min_times[*]}")

# average_max_time=$(awk '{sum+=$1} END{print sum/NR}' <<< "${triad_max_times[*]}")


# # 在文件中追加平均值

# echo "Averages: Triad, $average_rate, $average_avg_time, $average_min_time, $average_max_time" >> stream.txt


# # 显示最终的平均值

# echo "Average Triad Results:"

# echo "Best Rate MB/s: $average_rate"

# echo "Avg time: $average_avg_time"

# echo "Min time: $average_min_time"

# echo "Max time: $average_max_time"


# # wget  http://smb.zstack.io/mirror/lei.zhang/linuxTESTshell/cshowmestream.sh
# # bash  cshowmestream.sh
```









排查的现象  客户机器现场的Stream结果 在物理机器和虚拟机上漂移都比较严重 严重影响了跑分结果和性能测试的数据， 同时虚拟机上严重偏低   





###### 当前的调优配置 







做的工作

```
 1. 同步手册里面的内容
2. 
```

##### 月蓉姐给的调优截图

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd5304252c6e4116a5165d657c91b29b515281838eac0cbc9b054f94edcf9481864915cf8b6795f07bf7e24fb4c8ed7016461c.png)

##### 小米测试手册里面的测试用例

上传stress.c到测试机上，gcc编译，生成stream.o文件。

[stream.c]

```
gcc-O-fopenmp-DSTREAM_ARRAY_SIZE=<array_size>-DNTIME=20
stream.c-ostream.o
```

<array_size>需要替换对应的数值，按下表计算。例如Intel8358P三级缓存48MB，

对应的ArraySize是50331648

size取值是 

执行.o文件，结果取Triad行BestRatesMB/s列的值。

Shell

./stream.o



###### 对应的.c文件源代码

http://www.cs.virginia.edu/stream/FTP/Code/stream.c

```
wget http://smb.zstack.io/mirror/lei.zhang/tools/stream.c
ls
```



##### 小米物理机配置 lscpu

左边虚拟 右边物理 （11月8号上午数据）

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd5304a89fe60809e32434efeb206769f3b615a9a3cb6b49c51fecf9f19ba4a0c21507184cc4567d36f5144fb4c8ed7016461c.png)

##### mlc拉取脚本

```
wget     http://smb.zstack.io/mirror/lei.zhang/mlc_v3.11b.tgz

tar  -zxvf     mlc_v3.11b.tgz  

cd  Linux  

ls

./mlc  
```



##### 我测试的物理机器配置







## 小米的问题是什么

1. strean在不指定线程的情况下比较弱
2. 直接运行。/stream的结果很低 特别是前5次 









## 今天下午开会记录的可能解决办法





## 可能有用的资料



#### 硬件信息脚本

```
#!/bin/bash
#用于获取软件版本  硬件信息   ForCentOS　
yum   install  lshw
 
 
 
# 获取并打印CPU型号和数量
lshw   | grep "product"
echo "1. CPU型号和数量:" | tee hardware_info.txt
> software_info.txt
truncate -s 0 software_info.txt
echo "1. CPU型号和数量:" | tee hardware_info.txt
cpu_model=$(lshw -class processor | grep "product" | uniq | awk -F': ' '{print $2}')
cpu_count=$(lshw -class processor | grep -c "product")
echo "CPU型号: $cpu_model" | tee -a hardware_info.txt
echo "CPU数量: $cpu_count" | tee -a hardware_info.txt
 
# 获取并打印内存条型号和数量   还需要排除description   product      中两个都满足这样的情况的product   为 NO DIMM 
#  description是empty的
echo "" | tee -a hardware_info.txt
 
echo "lscpu"
 
 
lscpu
 
lscpu  | tee   -a   hardware_info.txt
 
 
 
echo "lscpu"
 
echo "___________________________________________________________________________________________________________________________"
 
echo "2. 内存条型号和数量:" | tee -a hardware_info.txt
# lshw -class memory | tee -a hardware_info.txt  # 打印原始内存信息
# lshw -class memory |  grep -v -E "description: DIMM \[empty\]|product: NO DIMM"
# lshw -class memory | grep -v "description: DIMM \[empty\]" | grep -v "product: NO DIMM"  | grep -v "vendor: NO DIMM"   | grep -v "serial: NO DIMM"  | grep "size:"
# lshw -class memory | grep -v "description: DIMM \[empty\]" | grep -v "product: NO DIMM"  | grep -v "vendor: NO DIMM"   | grep -v "serial: NO DIMM"
# lshw -class memory | grep -v "description: DIMM \[empty\]" | grep -v "product: NO DIMM" | grep -v "vendor: NO DIMM" | grep -v "serial: NO DIMM" | awk '' | awk 'BEGIN{FS=":"}{if ($2 ~ /size/) print}'
# # 0246   lshw -class memory | grep -v "description: DIMM \[empty\]" | grep -v "product: NO DIMM" | grep -v "vendor: NO DIMM" | grep -v "serial: NO DIMM" | grep "size:"lshw -class memory | grep -A 10 "-bank:" | grep -v "description: DIMM \[empty\]" | grep -v "product: NO DIMM" | grep -v "vendor: NO DIMM" | grep -v "serial: NO DIMM" | grep -B 1 "size:"
memory_info=$(lshw -class memory | grep -v "description: DIMM \[empty\]" | grep -v "product: NO DIMM"  | grep -v "vendor: NO DIMM"   | grep -v "serial: NO DIMM"  | grep -E "description|size|product"  | awk '/description: DIMM/ {do {print; getline} while ($0 ~ /product:/ || $0 ~ /size:/ || $0 ~ /description: DIMM/)}')
memory_count=$(echo "$memory_info" | grep -c "product")
lshw -class memory | grep -v "description: DIMM \[empty\]" | grep -v "product: NO DIMM"  | grep -v "vendor: NO DIMM"   | grep -v "serial: NO DIMM"  | grep -E "description|size|product"  | awk '/description: DIMM/ {do {print; getline} while ($0 ~ /product:/ || $0 ~ /size:/ || $0 ~ /description: DIMM/)}'
 
echo "$memory_info" | tee -a hardware_info.txt
echo "内存条数量: $memory_count" | tee -a hardware_info.txt
 
echo "内存"
free -h
free -h | tee   -a   hardware_info.txt
dmidecode -t memory
echo "内存"
 
lshw -class disk | grep -E "description|logical name|size|product" | awk '
BEGIN { RS=""; ORS="\n" }
{
    if ($2 ~ /description:/) {
        # 遇到新的 description:，清空 buffer 并开始收集信息
        clear();
        add_to_buffer($0);
    }
    else if ($2 ~ /size:/) {
        # 遇到 size:，打印 buffer 中的内容并清空 buffer
        print_buffer();
        clear();
    }
    else {
        # 遇到其他行，将其添加到 buffer
        add_to_buffer($0);
    }
}
function clear() {
    # 清空 buffer
    delete buffer;
    buffer_idx = 0;
}
function add_to_buffer(line) {
    # 将行添加到 buffer
    buffer[++buffer_idx] = line;
}
function print_buffer() {
    # 打印 buffer 中的所有行
    for (i = 1; i <= buffer_idx; i++) {
        print buffer[i];
    }
}
'
 
# 获取并打印系统盘信息和挂载的SSD/HDD信息
echo "" | tee -a hardware_info.txt
echo "3. 系统盘和挂载的SSD/HDD盘:" | tee -a hardware_info.txt
lshw -class disk | grep -E "description|logical name|size|product"
disk_info=$(lshw -class disk | grep -E "description|logical name|size|product")
echo "$disk_info" | tee -a hardware_info.txt
 
# 获取并打印网卡信息
echo "" | tee -a hardware_info.txt
echo "4. 网卡信息:" | tee -a hardware_info.txt
gigabit_nics=$(lshw -class network | grep -A 12 "Ethernet" | grep -B 11 "size: 1Gbit/s")
ten_gigabit_nics=$(lshw -class network | grep -A 12 "Ethernet" | grep -B 11 "size: 10Gbit/s")
echo "Gigabit网卡:" | tee -a hardware_info.txt
echo "$gigabit_nics" | tee -a hardware_info.txt
echo "" | tee -a hardware_info.txt
echo "10-Gigabit网卡:" | tee -a hardware_info.txt
echo "$ten_gigabit_nics" | tee -a hardware_info.txt
 
# 获取并打印RAID卡信息
lshw -class storage
echo "" | tee -a hardware_info.txt
echo "5. RAID卡信息:" | tee -a hardware_info.txt
raid_info=$(lshw -class storage )
echo "$raid_info" | tee -a hardware_info.txt
 
# 获取并打印服务器型号
echo "" | tee -a hardware_info.txt
echo "6. 服务器型号:" | tee -a hardware_info.txt
server_model=$( lshw -class  system | grep  " product" )
echo "服务器型号: $server_model" | tee -a hardware_info.txt
 lshw -class  system | grep  " product"
echo "信息已保存到 hardware_info.txt 文件中."
 
#获取系统版本和Zsphere版本
cat /etc/zstack-release
cat   /etc/centos-release
cat   /etc/redhat-release
 libvirtd -V
 qemu-img  -V
#清空该文件里面记录  software_info.txt
 
 
echo "" | tee -a software_info.txt
> software_info.txt
truncate -s 0 software_info.txt
echo "1. linux系统:" | tee -a software_info.txt
linux_version=$( cat /etc/zstack-release )
echo "linux系统: $linux_version" | tee -a software_info.txt
echo "1. Zsphere版本:" | tee -a software_info.txt
zsv_version=$(cat   /etc/centos-release)
echo "Zsphere版本: $zsv_version" | tee -a software_info.txt
echo "1. libivirted版本:" | tee -a software_info.txt
libivirted_version=$( libvirtd -V)
echo "libivirted版本: $libivirted_version" | tee -a software_info.txt
echo "qemu版本:" | tee -a software_info.txt
qemu_version=$( qemu-img  -V)
echo "qemu版本: $qemu_version" | tee -a software_info.txt
 
 #lshw -class  system | grep  " product"
echo "信息已保存到 software_info.txt 文件中."
 
 
 
 
LOGFILE="/root/machine.log"
(
cd   /etc/yum.repos.d
wget   http://smb.zstack.io/mirror/lei.zhang/h84ryumrepo/zstack-aliyun-yum.repo
sudo yum install -y fio
sudo yum clean  all
sudo yum makecache
sudo yum install unzip -y
 
 
cd /root
 
# wget -r -l1 -np -k http://smb.zstack.io/mirror/lei.zhang/tools/figlet
wget http://smb.zstack.io/mirror/lei.zhang/tools/figlet.zip
unzip  figlet.zip
# git  clone https://github.com/cmatsuoka/figlet.git
# cd figlet/
cd  figlet/
ls
sudo make
sudo make install
 
figlet  "Good Luck!"
 
figlet  "HAPPY    HAPPY       HAPPY!"
figlet   "??????♥ 或 <3"
 
figlet -f slant ""
 
wget    http://smb.zstack.io/mirror/lei.zhang/linuxTESTshell/furina._wave_her_hand_so_cute.txt
cat    furina._wave_her_hand_so_cute.txt
figlet  "furina._wave_her_hand_so_cute.txt"
figlet  "eth"
lspci | grep Eth
figlet  "CPU"
lscpu
figlet  "FREE"
free -g
free -h
figlet  "DISK"
figlet  "Disk layout"
lsblk
figlet "Disk space usage:"
df -h 
figlet sda
smarctl -i  /dev/sda
figlet   "SMART information for all disks:"
echo "SMART information for all disks:"
for disk in /dev/sd* /dev/nvme*; do
    if [ -e "$disk" ]; then
        echo "Checking $disk..."
        smartctl -i "$disk"
    else
        echo "No such disk: $disk"
    fi
done
) |& tee -a  "$LOGFILE"
```

#### stream 调参说明

http://confluence.zstack.io/pages/viewpage.action?pageId=133572551



##### 参考信息 海光调优

```
针对hygon平台的编译参数优化，虚机中需要配置host-passthrogh后特性生效。
单线程
gcc-march=bdver3 -O3 -mcmodel=medium -DN=64000000 -DNTIMES=100 stream.c -osingle_stream
多线程
gcc-mtune=bdver1 -march=bdver1 -O3 -mcmodel=medium -LNO:prefetch=2 -fopenmp-DSTREAM_ARRAY_SIZE=64000000 -DNTIMES=100 stream.c -o multi_stream 我们打电话吧 开一个钉钉视频会议
```



#### 采取的STReam 编译的结果

编译1 

```
gcc -O3 -mcmodel=medium -fopenmp -DSTREAM_ARRAY_SIZE=64000000 -DNTIMES=30 -DOFFSET=4096 stream.c -o stream.o
```

反馈 

编译2 小米要求的编译指令

```
gcc -O -fopenmp     -DSTREAM_ARRAY_SIZE=    -DNTIMES=20      stream.c -o stream.o
```

以及 size参数 

L3缓存*4*CPU路数/8

L3缓存= L3缓存单位MB*1024*1024 

所以物理机器 

```
gcc -O -fopenmp -DSTREAM_ARRAY_SIZE=16000000 -DNTIMES=20 stream.c -o stream.o
```





##### stream运行只查看Traid的命令

```
./stream.o | grep "Triad" | tee  stream_temp.txt
```



指定跑的线程的指令

```
export  OMP_NUM_THREADS=16
```





## 11月8日 自己的实验环境上的实验记录

### 分布式环境

分布式环境的硬件信息



```
HOST2  物理机器    172.25.16.181 
     H84             172.27.112.190
C79                   172.27.112.169   
wget     http://smb.zstack.io/mirror/lei.zhang/mlc_v3.11b.tgz

tar  -zxvf     mlc_v3.11b.tgz  

cd  Linux  

ls

./mlc  
```





#### 测试环境 双核服务器

172.24.0.96 password

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd5304bba343de0d780f31a7fd6df8a46312a09f478a1a12ba3bee7b3e6d877d5e4128ba337d9bbd7d8e8e4fb4c8ed7016461c.png)

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd53041da6c96b1c27e933faec3ca8bf8b1ee2bf0614fa2e23723007875814ed7e584970549ae253dc49994fb4c8ed7016461c.png)

单片cpu是16个物理核（每哥物理核可以给两个逻辑核）

我是双核服务器 给了两个NUMA节点 0 1 以及详情是这个样子

```
Intel(R) Memory Latency Checker - v3.11b
Measuring idle latencies for sequential access (in ns)...
                Numa node
Numa node            0       1
       0          90.6   146.4
       1         145.5    88.7

Measuring Peak Injection Memory Bandwidths for the system
Bandwidths are in MB/sec (1 MB/sec = 1,000,000 Bytes/sec)
Using all the threads from each core if Hyper-threading is enabled
Using traffic with the following read-write ratios
ALL Reads        :      190909.3
3:1 Reads-Writes :      182249.5
2:1 Reads-Writes :      180180.1
1:1 Reads-Writes :      177746.6
Stream-triad like:      157829.0

Measuring Memory Bandwidths between nodes within system
Bandwidths are in MB/sec (1 MB/sec = 1,000,000 Bytes/sec)
Using all the threads from each core if Hyper-threading is enabled
Using Read-only traffic type
                Numa node
Numa node            0       1
       0        96253.8 31712.3
       1        31696.1 96077.7

Measuring Loaded Latencies for the system
Using all the threads from each core if Hyper-threading is enabled
Using Read-only traffic type
Inject  Latency Bandwidth
Delay   (ns)    MB/sec
==========================
 00000  201.58   192290.8
 00002  202.05   191296.8
 00008  200.37   192229.8
 00015  199.74   191327.3
 00050  189.20   190433.5
 00100  129.09   151730.3
 00200  100.79    96529.2
 00300   96.26    66466.0
 00400   93.43    51091.1
 00500   94.80    41143.2
 00700   91.64    30187.4
 01000   92.56    21374.0
 01300   90.67    16798.0
 01700   90.58    13024.3
 02500   90.08     9146.8
 03500   90.32     6732.6
 05000   90.62     4928.1
 09000   89.98     3068.7
 20000   90.00     1772.1

Measuring cache-to-cache transfer latency (in ns)...
Local Socket L2->L2 HIT  latency        48.8
Local Socket L2->L2 HITM latency        48.9
Remote Socket L2->L2 HITM latency (data address homed in writer socket)
                        Reader Numa Node
Writer Numa Node     0       1
            0        -   112.8
            1    113.4       -
Remote Socket L2->L2 HITM latency (data address homed in reader socket)
                        Reader Numa Node
Writer Numa Node     0       1
            0        -   190.9
            1    189.3       -
```

值得同步的信息 1 有人对双核服务器的两个CPU是这个样子叫的 本地socket和 交叉socket 我不知道为啥 



```
Command line parameters: --latency_matrix

Using buffer size of 200.000MiB
Measuring idle latencies for sequential access (in ns)...
                Numa node
Numa node            0       1
       0          90.6   146.8
       1         145.3    88.7

Numa node 0 到 Numa node 0：90.6 ns
Numa node 0 到 Numa node 1：146.8 ns
Numa node 1 到 Numa node 0：145.3 ns
Numa node 1 到 Numa node 1：88.7 ns
[root@172-24-0-96 Linux]# ./mlc   --bandwidth_matrix
Intel(R) Memory Latency Checker - v3.11b
Command line parameters: --bandwidth_matrix

Using buffer size of 100.000MiB/thread for reads and an additional 100.000MiB/thread for writes
Measuring Memory Bandwidths between nodes within system
Bandwidths are in MB/sec (1 MB/sec = 1,000,000 Bytes/sec)
Using all the threads from each core if Hyper-threading is enabled
Using Read-only traffic type
                Numa node
Numa node            0       1
       0        96183.4 31682.2
       1        31639.1 96211.4
./mlc --idle_latency
[root@172-24-0-96 Linux]# ./mlc --idle_latency
Intel(R) Memory Latency Checker - v3.11b
Command line parameters: --idle_latency

Using buffer size of 200.000MiB
Each iteration took 186.5 base frequency clocks (       89.0    ns)
./mlc --loaded_latency
```

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd53049019ecea28a5ebdda3f6c72228cc54c768ba4ed75d747a316412e1c7bdb60f9c90b2f44cd5645c384fb4c8ed7016461c.png)

```
./mlc --peak_injection_bandwidth
```

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd530444030820a9a8fd33c7ab4e89edc83990d9c6839ca24ec9292faeb5b59383ab4538536d71a2f6ca7a4fb4c8ed7016461c.png)![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd53043d9809bf1553a5af99a3cf549d8223f87b8819e06e43a1d0d3fbc15b121a99bc728a6f5e66404faa4fb4c8ed7016461c.png)

```
 ./mlc --c2c_latency
测量缓存到缓存（cache-to-cache）的数据传输延迟
一个核心的缓存（例如L2缓存）向另一个核心的缓存（例如L2缓存）传输数据所需的时间
测量本地socket（同一物理CPU插槽）和远程socket（不同物理CPU插槽）之间的缓存到缓存延迟
```

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd53046a0b6f09adf3e2eaca195c07235808eadfef5cff4b715f01080196cbe54a1905c02caa30073486104fb4c8ed7016461c.png)



STREAM测试

普通小米编译

```
gcc -O -fopenmp -DSTREAM_ARRAY_SIZE=16000000 -DNTIMES=20 stream.c -o stream.o
```



超大内存编译

```
gcc -O -fopenmp -DSTREAM_ARRAY_SIZE=200000000  -mcmodel=large -DNTIMES=20 stream.c -o stream.o
# 1-63 序号的单线程绑核测试
taskset -c 2./stream.o
```

单线程绑核不波动



```
 taskset -c 2,6,9,7,45,61 ./stream.o
```

多线程 随便绑核要波动 

多线程8 绑同一个numa节点呢 8xianc 看一看

```
 taskset -c 2,4,6,8,10,16,18,20 ./stream.o
taskset -c 2,4,6,8,10,16,18,20 ./stream.o | grep Triad
taskset -c 2,4,6,8,10,16,18,20 ./stream.o | grep Triad
taskset -c 2,4,6,8,10,16,18,20 ./stream.o | grep Triad
taskset -c 2,4,6,8,10,16,18,20 ./stream.o | grep Triad
taskset -c 2,4,6,8,10,16,18,20 ./stream.o | grep Triad
taskset -c 2,4,6,8,10,16,18,20 ./stream.o | grep Triad
taskset -c 2,4,6,8,10,16,18,20 ./stream.o | grep Triad
taskset -c 2,4,6,8,10,16,18,20 ./stream.o | grep Triad
taskset -c 2,4,6,8,10,16,18,20 ./stream.o | grep Triad
```

不波动物理机

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd530487dcd39ff4a61433249ad51c5bc690626fd21ed09053e5961a9f1b87c4f26c3b66f4c047ef1d0b094fb4c8ed7016461c.png)

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd5304e8df9355f0018d82c581cecdfbe723b3052b9dec1a8fdbe616baa0008731d1698bc6755ed6f5c21d4fb4c8ed7016461c.png)

高度一致

多线程8 绑不同一个numa节点呢 8xianc 看一看

```
 taskset -c 2,4,6,8,10,16,18,20 ./stream.o
taskset -c 11,12,13,14,15,16,17,18 ./stream.o | grep Triad
taskset -c 11,12,13,14,15,16,17,18 ./stream.o | grep Triad
taskset -c 11,12,13,14,15,16,17,18 ./stream.o | grep Triad
taskset -c 11,12,13,14,15,16,17,18 ./stream.o | grep Triad
taskset -c 11,12,13,14,15,16,17,18 ./stream.o | grep Triad
taskset -c 11,12,13,14,15,16,17,18 ./stream.o | grep Triad
taskset -c 11,12,13,14,15,16,17,18 ./stream.o | grep Triad
taskset -c 11,12,13,14,15,16,17,18 ./stream.o | grep Triad
taskset -c 11,12,13,14,15,16,17,18 ./stream.o | grep Triad
```

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd5304990ad64c98c4fd3ecb91f66ce5b84e8a16a39b858b3e0e526d4702134527ca882cd4e7b7b8e89a6a4fb4c8ed7016461c.png)第一次run

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd53046951667d44ad544bf86679797f4bc50315de2bf2e73da53ddf57678ff66b25ab28f47bf547a1ceec4fb4c8ed7016461c.png)第二次run 

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd5304ae92fe2dfdaf34a6e15b15361ac1281bd5438b68c595a155a0a874017834cd8b320a77fa00bc09194fb4c8ed7016461c.png) 第三次run 

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd53043a2d18e7ae5d01926376aee55c28374aeef6e0b6fffe90782285eccf4d218f28ea3ab3b59272a0784fb4c8ed7016461c.png) 第四次

用脚本run 确实很奇怪 按我的想象来说 应该到处乱飘的 但是后面就不怎么乱飘了 虽然比绑同一个NUMA节点的比还是有点飘 

直接run的结果

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd530458273e6fcf3f17c23daaf1c7435a4c38f92954cf62ed7c5362cc3aab0be418b3b485ad0a33f378684fb4c8ed7016461c.png)







#### 测试环境 把这个双核服务器搭建成计算节点之后的上面的C79虚拟机

172.24.0.96 这个是计算节点

https://172.25.122.160/ 想要让这个做管理节点 

```
172.25.122.160
```

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd530403063bf0dcb3b03cae9808330c82eadec014bdb5269465eec98100bbfe1b1d256220991798c2ee1b4fb4c8ed7016461c.png)

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd5304b61c1b50be6bf4cde10748a4b1425bd6c74fdd5a1def697d3b57907589875a69c593d65f0482e5e94fb4c8ed7016461c.png)

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd530493ebc76fa0758fd1f6d97228e96d45e1827d5216b98630a875897f51464ce8b7687f26fe69d2adac4fb4c8ed7016461c.png)

看/var/log/zstack/zstack-kvmagent.log这个里面搜索8080，对应的IP地址就是管理的IP 

C79 url http://172.25.14.98:8001/imagestore/download/CentOS7.9-image-e91e6c6af9f17fe0733d4e43683128a8dadd2475.qcow2

去搞一个公网IP段 

- Name: 172.19.40.232
- Ipmi: 172.19.40.232
- IpRange: 172.25.128.224-172.25.128.255

100.254我怎么进不去 先用这个顶一下把

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd530456e0c453ea2eb75b2d1b107e1cf863c79afdfd8a4e3fa6923c0c34c0530c299ee7624a3f9c97d2d24fb4c8ed7016461c.png)





虚拟机结果

```
 taskset -c 0-7  ./stream.o
taskset -c 0-7 ./stream.o | grep Triad
taskset -c 0-7 ./stream.o | grep Triad
taskset -c 0-7 ./stream.o | grep Triad
taskset -c 0-7 ./stream.o | grep Triad
taskset -c 0-7 ./stream.o | grep Triad
taskset -c 0-7 ./stream.o | grep Triad
taskset -c 0-7 ./stream.o | grep Triad
taskset -c 0-7 ./stream.o | grep Triad
taskset -c 0-7 ./stream.o | grep Triad
```

8C8G 不配NUMA 

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd53046bee4779d9984dfdc5fc26dd01f6058bbd3d0e8778f16391583a244dd7107aa2b56685d2e69beb7b4fb4c8ed7016461c.png)

8C8G 配置NUMA 在同一个NUMA节点

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd5304af88a433cf2f46f8e1b970410dbd1ffb9707d05b7936aad3f401183fbb2bd8d938553f1f6e26e3ca4fb4c8ed7016461c.png)

```
./stream.o | grep Triad
./stream.o | grep Triad
  ./stream.o | grep Triad
  ./stream.o | grep Triad
  ./stream.o | grep Triad
  ./stream.o | grep Triad
  ./stream.o | grep Triad
  ./stream.o | grep Triad
  ./stream.o | grep Triad
  ./stream.o | grep Triad
```

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd530447c47897c73c599632f75cfa0959e7d245cad0ed2dd920754cc9d364975f6970d7f1bf825974a82d4fb4c8ed7016461c.png)

--》 回去物理机 

```
taskset -c  0,2,4,6,8,10,12,14 ./stream.o | grep Triad
taskset -c  0,2,4,6,8,10,12,14 ./stream.o | grep Triad
taskset -c  0,2,4,6,8,10,12,14 ./stream.o | grep Triad
taskset -c  0,2,4,6,8,10,12,14 ./stream.o | grep Triad
taskset -c  0,2,4,6,8,10,12,14 ./stream.o | grep Triad
taskset -c  0,2,4,6,8,10,12,14 ./stream.o | grep Triad
taskset -c  0,2,4,6,8,10,12,14 ./stream.o | grep Triad
taskset -c  0,2,4,6,8,10,12,14 ./stream.o | grep Triad
taskset -c  0,2,4,6,8,10,12,14 ./stream.o | grep Triad
taskset -c  0,2,4,6,8,10,12,14 ./stream.o | grep Triad

taskset -c  0-7 ./stream.o | grep Triad
for i in {1..20}; do taskset -c 0-7 ./stream.o | grep Triad; done
for i in {1..20}; do taskset -c 8-15 ./stream.o | grep Triad; done
for i in {1..20}; do taskset -c 0-15 ./stream.o | grep Triad; done
for i in {1..20}; do taskset -c 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30./stream.o | grep Triad; done
```

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd5304d2df60a1e36a3b067cd3815b3228f763ba7c1ac8c73de0cf0e5cc09a89b2e7558f0e853684c3443b4fb4c8ed7016461c.png)





```
taskset -c 0 ./stream.o | grep Triad
taskset -c 0,2 ./stream.o | grep Triad
taskset -c 0,2,4 ./stream.o | grep Triad
taskset -c 0,2,4,6 ./stream.o | grep Triad
taskset -c 0,2,4,6,8 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14,16 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14,16,18 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14,16,18,20 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14,16,18,20,22 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14,16,18,20,22,24 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14,16,18,20,22,24,26 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46 ./stream.o | grep Triad
taskset -c 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48 ./stream.o | grep Triad
```

# 11月9日 现场 

另外一个上面没有正在running的计算节点 pool-cd999e2f8c8c4006be7cab8e6a86a109 

- 10.229.8.72

希望看一下 只绑定单个CPU上面的核的话 同一个NUMA节点的核大概到多少个就稳定不变了 或者到顶峰了

```
taskset -c 0 ./stream.o | grep Triad
taskset -c 0-1 ./stream.o | grep Triad
taskset -c 0-2 ./stream.o | grep Triad
taskset -c 0-3 ./stream.o | grep Triad
taskset -c 0-4 ./stream.o | grep Triad
taskset -c 0-5 ./stream.o | grep Triad
taskset -c 0-6 ./stream.o | grep Triad
taskset -c 0-7 ./stream.o | grep Triad
taskset -c 0-8 ./stream.o | grep Triad
taskset -c 0-9 ./stream.o | grep Triad
taskset -c 0-10 ./stream.o | grep Triad
taskset -c 0-11 ./stream.o | grep Triad
taskset -c 0-12 ./stream.o | grep Triad
taskset -c 0-13 ./stream.o | grep Triad
taskset -c 0-14 ./stream.o | grep Triad
taskset -c 0-15 ./stream.o | grep Triad
```

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd530423fe293b8eb002a0ecee0347602ed340c18f5cffa2647a95558cc345d0436b8e70e1832313b132054fb4c8ed7016461c.png)

继续加 Copy

```
taskset -c 0 ./stream.o | grep  Copy
taskset -c 0,1 ./stream.o | grep  Copy
taskset -c 0,1,2 ./stream.o | grep COPY
taskset -c 0,1,2,3 ./stream.o | grep COPY
taskset -c 0,1,2,3,4 ./stream.o | grep COPY
taskset -c 0,1,2,3,4,5 ./stream.o | grep COPY
taskset -c 0,1,2,3,4,5,6 ./stream.o | grep COPY
taskset -c 0,1,2,3,4,5,6,7 ./stream.o | grep COPY
taskset -c 0,1,2,3,4,5,6,7,8 ./stream.o | grep COPY
taskset -c 0,1,2,3,4,5,6,7,8,9 ./stream.o | grep COPY
taskset -c 0,1,2,3,4,5,6,7,8,9,10 ./stream.o | grep COPY
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11 ./stream.o | grep COPY
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12 ./stream.o | grep COPY
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13 ./stream.o | grep COPY
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14 ./stream.o | grep COPY
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 ./stream.o | grep COPY
```





```
taskset -c 0 ./stream.o | grep Triad
taskset -c 0,1 ./stream.o | grep Triad
taskset -c 0,1,2 ./stream.o | grep Triad
taskset -c 0,1,2,3 ./stream.o | grep Triad
taskset -c 0,1,2,3,4 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 ./stream.o | grep Triad
taskset -c 32 ./stream.o | grep Triad
taskset -c 32,33 ./stream.o | grep Triad
taskset -c 32,33,34 ./stream.o | grep Triad
taskset -c 32,33,34,35 ./stream.o | grep Triad
taskset -c 32,33,34,35,36 ./stream.o | grep Triad
taskset -c 32,33,34,35,36,37 ./stream.o | grep Triad
taskset -c 32,33,34,35,36,37,38 ./stream.o | grep Triad
taskset -c 32,33,34,35,36,37,38,39 ./stream.o | grep Triad
taskset -c 32,33,34,35,36,37,38,39,40 ./stream.o | grep Triad
taskset -c 32,33,34,35,36,37,38,39,40,41 ./stream.o | grep Triad
taskset -c 32,33,34,35,36,37,38,39,40,41,42 ./stream.o | grep Triad
taskset -c 32,33,34,35,36,37,38,39,40,41,42,43 ./stream.o | grep Triad
taskset -c 32,33,34,35,36,37,38,39,40,41,42,43,44 ./stream.o | grep Triad
taskset -c 32,33,34,35,36,37,38,39,40,41,42,43,44,45 ./stream.o | grep Triad
taskset -c 32,33,34,35,36,37,38,39,40,41,42,43,44,45,46 ./stream.o | grep Triad
taskset -c 32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,35 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,35,36 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,35,36,37 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,35,36,37,38 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,35,36,37,38,39 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,35,36,37,38,39,40 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,35,36,37,38,39,40,41 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,35,36,37,38,39,40,41,42 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,35,36,37,38,39,40,41,42,43 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,35,36,37,38,39,40,41,42,43,44 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,35,36,37,38,39,40,41,42,43,44,45 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46 ./stream.o | grep Triad
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47 ./stream.o | grep Triad
```

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd530412b4c493a6eb80256bd86b19659f2ef2e3b59967ad5486089b484c20988d154a3b9b160102b195594fb4c8ed7016461c.png)

NUMA 

如果是多个CPU呢？

```
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47 ./stream.o | grep Triad
```



```
taskset -c 0-64 ./stream.o | grep Triad
```

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd530451cbca6f734c9a354a846f64bc0c93333abba96f431bd6b103e42bf1edf455a9c85c633569b216f34fb4c8ed7016461c.png)

写死的 



这样绑好像不行唉

写死试试

```
taskset -c 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47 ./stream.o | grep Triad
```

16-31 48-63的



第一次不行的解释

可以的 tlb的 cache miss

现场的lscpu状态是什么 

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd530455d7790c02ea5238371a8cfee1f911f7c5593b77488bca10a109fa33503d708da28e971ecfca8a394fb4c8ed7016461c.png)

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd5304d24e933ad22d3d1f806446f2d92979957e652b77929d74688f7c10305dd9944fd06d1567ddb4008a4fb4c8ed7016461c.png)



```

```





# 最后确定的测试方法 

stream的编译方法

```
gcc -O -fopenmp -DSTREAM_ARRAY_SIZE=16777216 -DNTIMES=20 stream.c -o stream.o
gcc -O -fopenmp -DSTREAM_ARRAY_SIZE=25165824 -DNTIMES=20 stream.c -o stream.o
```

如果采用上面是虚拟机的编译方法 下面是物理机的编译方法的话 虚拟机会比物理机器高 

如果都采用一样的编译方法的话 虚拟机会比物理机器低 



采取的运行方法

```
./stream.o     
 taskset -c 0-31  ./stream.o
```

采取的虚拟机配置方法 

需要注意的一点 虚拟机必须让同一个插槽里面的cpu是物理机上面同一个插槽的的NUMA节点里面的 而且需要两个NUMA节点的都配进去

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd5304620b4331c2fcd3515e72b94ac81467d32ef47783d7771f9eb4c4c9c9b51d4bf07a9777f79fc237884fb4c8ed7016461c.png)

![img](./assets/5eecdaf48460cde5c81eb3eb638e68be51a700420352ee298433de2d5aa4e7b02a17809207092929ec177c308ebd5304bee67c8d04407a4a98bd2941f797620acac90e7f6952b2b665b817da99cd822b77a2d66c715ecc544fb4c8ed7016461c.png)





## Attachments:

​                                                            ![img](./assets/bullet_blue.gif)                                [image2024-11-11_14-7-8.png](file:///E:/github/Confluence-space-export-082101-45.html/lei.zhang/attachments/182132530/182132533.png) (image/png)                                