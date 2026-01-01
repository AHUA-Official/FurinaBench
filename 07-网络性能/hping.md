                                                                            Created by  张磊 on 十一月 05, 2024                        

![img](./assets/177274397.png)



hping 是一个功能强大的网络工具，主要用于发送自定义 TCP/IP 数据包并接收回复。它类似于 ping 工具，但提供了更多的灵活性和高级功能。hping 可以用于网络测试、故障排除、安全审计等多种场景。

主要功能
自定义数据包：
发送任意类型的 TCP、UDP 和 ICMP 数据包。
自定义 IP 头字段，如 TTL、TOS、ID 等。
自定义 TCP 头字段，如标志位（SYN、ACK、FIN 等）、序列号、窗口大小等。
扫描和探测：
进行端口扫描和主机发现。
检测防火墙规则和网络过滤器。
发现网络拓扑结构。
数据传输：
发送任意数据负载。
支持数据加密和解密。
分析和统计：
显示详细的统计数据，如往返时间（RTT）、丢包率等。
支持多种输出格式，包括标准输出和日志文件。





安装和使用看我空间下面 标题带hping的脚本



# 脚本 hping测试示例                                            

​                                                                            Created by  张磊 on 十一月 05, 2024                        

​       

```
#!/bin/bash

TOTAL_TIME=300


stress --cpu 4 --timeout $TOTAL_TIME &

STRESS_PID=$!
counter=0
while [ $counter -lt $TOTAL_TIME ]; do
    OUTPUT=$(hping3 -c 100 -i u100 -w 1 -q --icmp 223.5.5.5 | tail -n 3)
    

    CURRENT_TIME=$(date +%s)
    
    echo "$OUTPUT"
    
    echo "$CURRENT_TIME, Output: $OUTPUT" >> hping3_results.txt
    
    sleep 3
    ((counter+=3))
done

kill $STRESS_PID

echo "Testing completed.  echo to hping3_results.txt"
```

# 安装hping                                            

​                                                                            Created by  张磊 on 十一月 05, 2024                        

​       

```
#bin/bash
mkdir -p /hpingme
cd /hpingme

ls
ip r
ip  addr  
cd /etc
ls |grep resolv

cat resolv.conf
cd    /etc
 cd   /etc/yum.repos.d/
wget    http://smb.zstack.io/mirror/lei.zhang/h84ryumrepo/zstack-aliyun-yum.repo
# 定义所需的nameserver地址
NAMESERVER="223.5.5.5"

# 检查/etc/resolv.conf文件是否存在
if [ -f "/etc/resolv.conf" ]; then
    # 检查文件是否包含指定的nameserver
    if grep -q "nameserver ${NAMESERVER}" "/etc/resolv.conf"; then
        echo "resolv.conf已包含指定的nameserver: ${NAMESERVER}"
    else
        echo "更新resolv.conf以包含指定的nameserver: ${NAMESERVER}"
        # 使用echo和grep将nameserver写入resolv.conf
        echo "nameserver ${NAMESERVER}" | sudo tee -a "/etc/resolv.conf" > /dev/null
    fi
else
    # 如果文件不存在，创建它并添加nameserver
    echo "创建resolv.conf并添加nameserver: ${NAMESERVER}"
    echo "nameserver ${NAMESERVER}" | sudo tee "/etc/resolv.conf" > /dev/null
fi
cd  /hpingme
wget  http://smb.zstack.io/mirror/lei.zhang/hpingrepo/libpcap-1.10.4.tar.xz
wget  http://smb.zstack.io/mirror/lei.zhang/hpingrepo/hping-master.zip

unzip hping-master.zip
tar -xvf libpcap-1.10.4.tar.xz


yum install -y gcc libpcap libpcap-devel tcl tcl-devel
yum install -y  tcl tcl-devel
yum install -y  tcl tcpdump
yum install -y gcc libpcap libpcap-devel tcl tcl-devel
sudo yum install bison  -y
sudo yum install flex  -y 

cd  /hpingme/libpcap-1.10.4
ls  
./configure
make
make install

cd pcap/
ls 
cp bpf.h /usr/include/net/bpf.h

cd /hpingme/hping-master/
ls  
./configure
make
make install

hping3 -c 100 -i u10000 -w 1 -q --icmp 223.5.5.5
```

# 脚本  展示ping一个ip的延迟                                            

​                                                                            Created by  张磊 on 十一月 05, 2024                        

```
#!/bin/bash

# 定义变量
PING_IP="172.25.12.58"
COUNT=30 # 每次ping命令发送的数据包数量
RESULT_FILE="ping_temp.txt"

# 执行ping命令，并将完整输出重定向到临时文件，用于后续处理
ping -c $COUNT $PING_IP > "$RESULT_FILE"

# 提取每次ping的延迟时间到数组中
readarray -t PING_TIMES < <(grep -oP '\d+\.\d+(?=\sms)' "$RESULT_FILE")

# 计算并打印统计信息
if [ ${#PING_TIMES[@]} -eq 0 ]; then
    echo "未获取到有效的延迟数据，请检查ping命令是否执行成功。"
else
    # 计算最大、最小、平均延迟
    OVERALL_MIN_LATENCY=$(printf "%s\n" "${PING_TIMES[@]}" | sort -n | head -n1)
    OVERALL_MAX_LATENCY=$(printf "%s\n" "${PING_TIMES[@]}" | sort -nr | head -n1)
    OVERALL_AVG_LATENCY=$(awk '{sum += $1} END {print sum/NR}' <<<"${PING_TIMES[*]}")

    # 计算延迟方差
    SUM_OF_SQUARES=0
    for LATENCY in "${PING_TIMES[@]}"; do
        SUM_OF_SQUARES=$(echo "$SUM_OF_SQUARES + ($LATENCY * $LATENCY)" | bc)
    done
    OVERALL_VARIANCE=$(echo "scale=3; ($SUM_OF_SQUARES / ${#PING_TIMES[@]}) - ($OVERALL_AVG_LATENCY * $OVERALL_AVG_LATENCY)" | bc)

    # 打印统计结果
    echo "基于30次发包的ping测试统计："
    echo "最小延迟：$OVERALL_MIN_LATENCY ms"
    echo "最大延迟：$OVERALL_MAX_LATENCY ms"
    echo "平均延迟：$OVERALL_AVG_LATENCY ms"
    echo "延迟方差：$OVERALL_VARIANCE ms^2"
fi

# 删除临时文件，避免残留
#rm "$RESULT_FILE"
```

# 脚本   流程     使用hping来定时定量的完成虚拟机丢包率的测定                                            

​                                                                            Created by  张磊, last modified on 八月 06, 2024                        

## 介绍  



ping工具是我们常常用来处理网络连通性的一个工具    然后先略着奥  





所以要使用hping  我们首先要安装他  在我现在的任务h84r上 我换了很多个源  都无法以yum的形式找到hping  不能yum装了  那我们只能采用源码编译安装的方式  在下面  



## 安装hping  

嗯 虽然是源码编译 但是有一些依赖还是需要用yum的 使用这个脚本之前检查一下网络联通性和yum源   我的脚本里面只会带给你一个阿里云的源   推荐在新环境的时候先手动一步一步执行脚本  没有问题的话 以后就可以直接用了   

脚本的地址  http://smb.zstack.io/mirror/lei.zhang/hpingrepo/installhpingbyzl.sh

​       

```
#bin/bash
mkdir -p /hpingme
cd /hpingme

ls
ip r
ip  addr  
cd /etc
ls |grep resolv

cat resolv.conf

# 定义所需的nameserver地址
NAMESERVER="223.5.5.5"

# 检查/etc/resolv.conf文件是否存在
if [ -f "/etc/resolv.conf" ]; then
    # 检查文件是否包含指定的nameserver
    if grep -q "nameserver ${NAMESERVER}" "/etc/resolv.conf"; then
        echo "resolv.conf已包含指定的nameserver: ${NAMESERVER}"
    else
        echo "更新resolv.conf以包含指定的nameserver: ${NAMESERVER}"
        # 使用echo和grep将nameserver写入resolv.conf
        echo "nameserver ${NAMESERVER}" | sudo tee -a "/etc/resolv.conf" > /dev/null
    fi
else
    # 如果文件不存在，创建它并添加nameserver
    echo "创建resolv.conf并添加nameserver: ${NAMESERVER}"
    echo "nameserver ${NAMESERVER}" | sudo tee "/etc/resolv.conf" > /dev/null
fi

cd    /etc/yum.repos.d/
wget   http://smb.zstack.io/mirror/lei.zhang/h84ryumrepo/zstack-aliyun-yum.repo
cd  /hpingme
wget  http://smb.zstack.io/mirror/lei.zhang/hpingrepo/libpcap-1.10.4.tar.xz
wget  http://smb.zstack.io/mirror/lei.zhang/hpingrepo/hping-master.zip

unzip hping-master.zip
tar -xvf libpcap-1.10.4.tar.xz


yum install -y gcc libpcap libpcap-devel tcl tcl-devel
yum install -y  tcl tcl-devel
yum install -y  tcl tcpdump
yum install -y gcc libpcap libpcap-devel tcl tcl-devel



cd  /hpingme/libpcap-1.10.4
ls  
./configure
make
make install

cd pcap/
ls 
cp bpf.h /usr/include/net/bpf.h

cd /hpingme/hping-master/
ls  
./configure
make
make install

hping3 -c 100 -i u10000 -w 1 -q --icmp 223.5.5.5
```

## 使用hping做丢包率测试 



ICMP报文命令模板 

hping3 -c 100 -i u10000 -w 1 -q --icmp 223.5.5.5  



-c  参数   发送报文的次数

-i  

-u  发送报文的间隔  u是us的意思 -u10000  每隔10000us发送一次ICMP报文   



--icmp  发送报文的名字  

223.5.5.5  ping对象的ip    







hping3 -c 1000000 -i u100 -w 1 -q --icmp 172.25.126.248

待完善
