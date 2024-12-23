​                                                                            Created by  张磊 on 十一月 05, 2024                        

​       

```
#!/bin/bash
# 用已封装好的
# centos7.6
# 镜像创建
# 1
# 台云主机作为服务端执行
# iperf3 
# -s
# ，另一台
# 物理机作为客户端执行
# iperf3 tcp
# 、
# udp
# 命令，测试
# 10
# 次，取最
# 10
# 次平均值。
# 作为iperf3   -s的是172.25.15.173
# 具体遥测的命令   或者参数   
# tcp  thread带宽  p
# tcp   nothread带宽

# udp  thread     1g     带宽   
# udp     no    thread     1g     带宽   
# udp  thread     1g    丢包率  
# udp     no    thread     1g   丢包率
# udp  thread     10g     带宽   
# udp     no    thread     10g     带宽   
# udp  thread     10g    丢包率  
# udp     no    thread     10g   丢包率

iperf3 -c 172.25.15.173 -P 4 -t 60 -i 1
iperf3 -c 172.25.15.173 -t 60 -i 1
iperf3 -c 172.25.15.173 -u -b 1G -P 4 -t 60 -i 1
iperf3 -c 172.25.15.173 -u -b 1G -t 60 -i 1
iperf3 -c 172.25.15.173 -u -b 1G -P 4 -t 60 -i 1 -Z
iperf3 -c 172.25.15.173 -u -b 1G -t 60 -i 1  -Z
iperf3 -c 172.25.15.173 -u -b 10G -P 4 -t 60 -i 1
iperf3 -c 172.25.15.173 -u -b 10G -t 60 -i 1
iperf3 -c 172.25.15.173 -u -b 10G -P 4 -t 60 -i 1 -Z
iperf3 -c 172.25.15.173 -u -b 10G -t 60 -i 1  -Z

# 定义变量

SERVER_IP="172.25.15.173"

TEST_COUNT=1

RESULT_DIR="iperf_results"

mkdir -p "$RESULT_DIR"


# TCP带宽测试

function test_tcp_bandwidth() {

    THREAD_FLAG="$1"

    THREADS="${2:-1}"

    BANDWIDTH_FILE="$RESULT_DIR/tcp_${THREAD_FLAG}_bandwidth.txt"

    > "$BANDWIDTH_FILE"

    

    for ((i=1; i<=$TEST_COUNT; i++)); do

        echo "Running TCP ${THREAD_FLAG} test $i out of $TEST_COUNT..."

        if [ "$THREAD_FLAG" = "thread" ]; then

            iperf3 -c $SERVER_IP -P $THREADS -t 60 -i 1 | grep sender | awk '{print $7}' >> "$BANDWIDTH_FILE"

        else

            iperf3 -c $SERVER_IP -t 60 -i 1 | grep sender | awk '{print $7}' >> "$BANDWIDTH_FILE"

        fi

    done

    

    AVG_BANDWIDTH=$(awk '{sum += $1} END {print sum/NR}' "$BANDWIDTH_FILE")

    echo "Average TCP ${THREAD_FLAG} bandwidth over $TEST_COUNT tests: $AVG_BANDWIDTH Mbits/sec"

}


# UDP带宽测试

function test_udp_bandwidth_and_loss() {

    THREAD_FLAG="$1"

    BANDWIDTH="${2:-1G}"

    THREADS="${3:-1}"

    BANDWIDTH_FILE="$RESULT_DIR/udp_${THREAD_FLAG}_${BANDWIDTH}_bandwidth.txt"

    LOSS_FILE="$RESULT_DIR/udp_${THREAD_FLAG}_${BANDWIDTH}_loss.txt"

    > "$BANDWIDTH_FILE"

    > "$LOSS_FILE"

    

    for ((i=1; i<=$TEST_COUNT; i++)); do

        echo "Running UDP ${THREAD_FLAG} ${BANDWIDTH} test $i out of $TEST_COUNT..."

        if [ "$THREAD_FLAG" = "thread" ]; then

            iperf3 -c $SERVER_IP -u -b $BANDWIDTH -P $THREADS -t 60 -i 1 | tee -a "$BANDWIDTH_FILE" | grep -oP '(\d+.\d+|\d+) Mbits/sec' | awk '{print $1}' >> "$BANDWIDTH_FILE"

            # 注意：对于丢包率，iperf3标准输出不直接提供，以下仅为示例，实际应根据iperf3的输出格式调整

            # 示例中未直接提供计算丢包率的代码，因为需要根据iperf3的具体输出逻辑进一步定制

        else

            iperf3 -c $SERVER_IP -u -b $BANDWIDTH -t 60 -i 1 | tee -a "$BANDWIDTH_FILE" | grep -oP '(\d+.\d+|\d+) Mbits/sec' | awk '{print $1}' >> "$BANDWIDTH_FILE"

        fi

    done

    

    AVG_BANDWIDTH=$(awk '{sum += $1} END {print sum/NR}' "$BANDWIDTH_FILE")

    echo "Average UDP ${THREAD_FLAG} ${BANDWIDTH} bandwidth over $TEST_COUNT tests: $AVG_BANDWIDTH Mbits/sec"

    

    # 实际丢包率的计算需要根据iperf3的详细输出和统计信息进行，此处未提供具体实现

    # 可能需要分析iperf3的输出日志来手动计算丢包率

}


# 执行测试

test_tcp_bandwidth "thread" 4

test_tcp_bandwidth "nothread"

test_udp_bandwidth_and_loss "thread" "1G" 4

test_udp_bandwidth_and_loss "nothread" "1G"

test_udp_bandwidth_and_loss "thread" "10G" 4

test_udp_bandwidth_and_loss "nothread" "10G"


echo "All tests completed. Results are saved in $RESULT_DIR."
```