```
#!/bin/bash

# 配置部分
VM_IP="172.25.16.241"  # 目标虚拟机的IP地址
TEST_DURATION=600          # 测试持续时间（秒）
INTERVAL=1                # 发送数据包的时间间隔（秒）
PACKET_SIZE=56           # 发送的数据包大小（字节）
SOURCE_IP="172.25.134.10"    # 发送数据包的源IP地址，通常是运行脚本的服务器IP
LOG_FILE="migration_test.log"  # 日志文件路径

# 准备测试环境
echo "开始测试环境设置..." | tee -a $LOG_FILE
ping -c 1 $VM_IP > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "无法到达虚拟机，请检查网络设置。" | tee -a $LOG_FILE
    exit 1
fi

# 测试开始时间
START_TIME=$(date +%s)

# 执行测试
echo "开始网络性能测试..." | tee -a $LOG_FILE
for (( i=0; i<$TEST_DURATION; i++ )); do
    echo "测试周期 $i 秒..." | tee -a $LOG_FILE
    # 使用ping发送数据包并记录丢包率
    ping -i $INTERVAL -s $PACKET_SIZE -c 1 $VM_IP >> $LOG_FILE
    sleep $((INTERVAL - 1))
done

# 测试结束时间
END_TIME=$(date +%s)

# 计算测试持续时间
ELAPSED_TIME=$((END_TIME - START_TIME))

# 输出测试结果
echo "网络性能测试完成。" | tee -a $LOG_FILE
echo "测试持续时间：$ELAPSED_TIME 秒。" | tee -a $LOG_FILE

# 绘制丢包率曲线图（如需）
echo "绘制丢包率曲线图..." | tee -a $LOG_FILE
# 这里可以使用如gnuplot等工具来绘制曲线图，示例略。

# 完成
echo "所有测试已完成。详细信息请查看日志文件：$LOG_FILE" | tee -a $LOG_FILE
```

# 脚本  ping 丢包率和响应时延                                            

​                                                                            Created by  张磊 on 十一月 05, 2024                        

```
#!/bin/bash

# 设置循环次数
LOOP_COUNT=100

for ((i=1; i<=LOOP_COUNT; i++)); do
    echo "循环 #$i 启动..."
    ping_output=$(ping -c 10 172.25.0.1)

# --- 172.25.0.1 ping statistics ---
# 10 packets transmitted, 10 received, 0% packet loss, time 9149ms
# rtt min/avg/max/mdev = 0.462/1.438/5.769/1.616 ms

    #
    packet_loss=$(echo "$ping_output" | grep 'packet loss' )
    avg_time=$(echo "$ping_output" | grep 'rtt' | awk '{print $4}' | tr -d ' ms')
    echo "丢包率: $packet_loss%"
    echo "平均响应时间 (avg): $avg_time ms"
    echo "-----------------------------------"


# 循环 #10 启动...
# 丢包率: received,%
# 平均响应时间 (avg): 0.519/0.810/2.470/0.559 ms


    sleep 0.1
done

echo "所有循环已完成。"
```

# 脚本 心跳发ping包                                            

​                                                                            Created by  张磊 on 十一月 05, 2024                        

```
#!/bin/bash

# 心跳包发送的目标服务器或IP地址
TARGET="baidu.com"
# 心跳包发送的间隔时间（秒）
INTERVAL=10

while true; do
   
    ping -c 1 $TARGET &> /dev/null

    # 检查ping命令的退出状态
    if [ $? -eq 0 ]; then
        # ping成功，连接是活跃的
        echo "$(date) - Heartbeat sent and received for $TARGET"
    else
       
        echo "$(date) - Heartbeat failed for $TARGET. Trying to reconnect..."
      
    fi

    # 等待指定的间隔时间
    sleep $INTERVAL
donei
```

待完善
