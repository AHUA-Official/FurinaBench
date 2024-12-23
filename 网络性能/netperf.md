```
#!/bin/bash

# ssh
# 到云主机操作系统中，运行
# netserver 
# ;   netperf 
# -t 
# TCP_RR 
# 127.0.0.1 -l 60
# 开始测试，测试十遍并记录测试数据，最终对十次测试数据取平均值

yum    install  netperf
netserver
netperf  -t  TCP_RR  127.0.0.1 -l 60 > output.txt
tail -n 2 output.txt | head -n 1 | awk '{print substr($0,length($0)-13)}'
rm  -rf  output.txt
(netperf  -t  TCP_RR  127.0.0.1 -l 60) | tail -n 2 | head -n 1 | awk '{print substr($0,length($0)-13)}'
(netperf  -t  TCP_RR  127.0.0.1 -l 60) | tail -n 2 | head -n 1 | awk '{print substr($0,length($0)-13)}'
(netperf  -t  TCP_RR  127.0.0.1 -l 60) | tail -n 2 | head -n 1 | awk '{print substr($0,length($0)-13)}'
(netperf  -t  TCP_RR  127.0.0.1 -l 60) | tail -n 2 | head -n 1 | awk '{print substr($0,length($0)-13)}'
(netperf  -t  TCP_RR  127.0.0.1 -l 60) | tail -n 2 | head -n 1 | awk '{print substr($0,length($0)-13)}'
(netperf  -t  TCP_RR  127.0.0.1 -l 60) | tail -n 2 | head -n 1 | awk '{print substr($0,length($0)-13)}'
(netperf  -t  TCP_RR  127.0.0.1 -l 60) | tail -n 2 | head -n 1 | awk '{print substr($0,length($0)-13)}'
(netperf  -t  TCP_RR  127.0.0.1 -l 60) | tail -n 2 | head -n 1 | awk '{print substr($0,length($0)-13)}'
(netperf  -t  TCP_RR  127.0.0.1 -l 60) | tail -n 2 | head -n 1 | awk '{print substr($0,length($0)-13)}'
```