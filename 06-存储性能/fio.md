fio

​       

```
#!/bin/bash
cd   /etc/yum.repos.d
wget   http://smb.zstack.io/mirror/lei.zhang/h84ryumrepo/zstack-aliyun-yum.repo
sudo yum install -y fio
sudo yum clean  all
sudo yum makecache
sudo yum install unzip -y

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

log_file="/root/fiologfile.log" # 日志文件
disk_a=/dev/vdb  
disk_b=/dev/vdc 
disk_c=/dev/vdd 
runtime=10
if [ ! -f "$log_file" ]; then
    echo "Log file not found."
    touch "$log_file"
    figlet  "getlog"
    figlet  "getlog----->Good!"
   
fi

if [ ! -f "$log_file" ]; then
    
     figlet  "getlog----->Good!"
   
fi

# figlet  "warmup"
# fio -name warmup    -filename="$disk_b" --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime="$runtime" -rw=write     --time_based=1 | tee -a "$log_file"
# figlet  "seqwrite"
# fio -name seqwrite  -filename="$disk_b" --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime="$runtime" -rw=write     --time_based=1  | tee -a "$log_file"
# figlet  "seqread"
# fio -name seqread   -filename="$disk_b" --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime="$runtime" -rw=read      --time_based=1  | tee -a "$log_file"

# figlet "randwrite"
# fio -name randwrite -filename="$disk_b" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=10G -runtime="$runtime" -rw=randwrite --time_based=1  | tee -a "$log_file"
# figlet "randread"
# fio -name randread  -filename="$disk_b" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=10G -runtime="$runtime" -rw=randread  --time_based=1  | tee -a "$log_file"


figlet "latwritelb"
fio -name latwrite  -filename="$disk_b" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime="$runtime" -rw=randwrite  --time_based=1  | tee -a "$log_file"
figlet "latreadlb"
fio -name latread   -filename="$disk_b" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime="$runtime" -rw=randread   --time_based=1  | tee -a "$log_file"
# #bin/bash


#怎么使用fio测试一个文件 
fio -name seqwrite  -filename=/dev/vdc --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime=100 -rw=write     --time_based=1  | tee -a "$log_file"


figlet "randwrite" | tee -a "$log_file"
figlet "randread"
fio -name randread  -filename=/dev/vdc --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=10G -runtime=100 -rw=randread  --time_based=1  | tee -a "$log_file"





fio -name seqwrite  -filename=/dev/nvme0n1 --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime=1000 -rw=write     --time_based=1
```



#                                                                             张磊 : fio的脚本本                                            

​                                                                            Created by  张磊 on 十一月 05, 2024                        

​       

```
#!/bin/bash

# 定义磁盘名字变量和日志文件路径
disk_name="/dev/sda"
log_file="/var/log/fio_test.log"
yum  install   fio 

# 确保日志文件存在
mkdir -p "$(dirname "$log_file")"
touch "$log_file"

# 函数：记录日志
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$log_file"
}
echo "欢迎使用磁盘性能测试脚本！"
echo "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
# 预热测试，执行3分钟
echo -e "正在启动预热测试..."
log "Starting warmup test."
fio -name warmup -filename="$disk_name" --numjobs=1 --allow_mounted_write=1  -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=10G -runtime=180 -rw=write --time_based=1 | tee -a "$log_file"
log "Warmup test completed."
echo -e "预热测试完成。\n"
# 顺序写入测试
echo -e "正在启动顺序写入测试..."
for numjobs in 1 10; do
    log "Starting sequential write test with $numjobs job(s)."
    fio -name seqwrite -filename="$disk_name" --numjobs="$numjobs" --allow_mounted_write=1  -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime=100 -rw=write --time_based=1 | tee -a "$log_file"
    log "Sequential write test with $numjobs job(s) completed."
done
echo -e "顺序写入测试完成。\n"
echo -e "正在启动顺序读出测试..."
# 顺序读出测试
log "Starting sequential read test."
fio -name seqread -filename="$disk_name" --numjobs=1 --allow_mounted_write=1   -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime=100 -rw=read --time_based=1 | tee -a "$log_file"
log "Sequential read test completed."
echo -e "正在完成顺序读出测试..."
echo -e "正在随机写入测试测试..."
# 随机写入测试
# 随机写入测试
log "Starting random write test."
fio -name randwrite -filename="$disk_name" --numjobs=64  --allow_mounted_write=1  -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=10G -runtime=100 -rw=randwrite --time_based=1 | tee -a "$log_file"
log "Random write test completed."
echo -e "正在完成随机写入测试测试..."
echo -e "正在 随机读出测试测试..."
# 随机读出测试
log "Starting random read test."
fio -name randread -filename="$disk_name" --numjobs=64 --allow_mounted_write=1   -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=10G -runtime=100 -rw=randread --time_based=1 | tee -a "$log_file"
log "Random read test completed."
echo -e "正在 完成随机读出测试测试..."
echo -e "正在 完成随机写入测试测试..关注延时."
# 随机写入测试，关注延时
log "Starting random write latency test."
fio -name randwrite_latency -filename="$disk_name" --numjobs=64  --allow_mounted_write=1  -ioengine=sync -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime=100 -rw=randwrite --time_based=1 | tee -a "$log_file"
log "Random write latency test completed."
echo -e "正在 完成随机写入测试测试..关注延时."
echo -e "正在 完成随机读出测试测试..关注延时."
# 随机读出测试，关注延时
log "Starting random read latency test."
fio -name randread_latency -filename="$disk_name" --numjobs=64  --allow_mounted_write=1  -ioengine=sync -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime=100 -rw=randread --time_based=1 | tee -a "$log_file"
log "Random read latency test completed."
echo -e "正在 完成随机读出测试测试..关注延时."
echo -e "测试完成日志保存在/var/log/fio_test.log"
```

#                                                                             张磊 : fio的脚本本本                                            

​                                                                            Created by  张磊 on 十一月 05, 2024                        

```
#!/bin/bash
#＃　　用于CPU跑分　　　　使用UNIXｂｅｎｃｈ　　　　获得的是最后的单核分数　　
#＃ｗｇｅｔ　　一个阿里云的ｙｕｍ镜像　　esfvfv 　　把他启用起来　　　
cd /etc
sudo yum upgrade
cd yum.repo.d
wget http://smb.zstack.io/mirror/lei.zhang/h84ryumrepo/zstack-aliyun-yum.repo
rm -rf /zapt
yum install git -y
cd /

mkdir /zapt
cd /zapt
git clone http://dev.zstack.io:9080/longtao.wu/apt_tools.git
rm -rf /apt_tools/.git
## 安装iperf3
yum install iperf3 -y
# 安装netperf
wget -c http://smb.zstack.io/mirror/mingmin.wen/tools/netperf-2.7.0-1.el7.lux.x86_64.rpm
rpm -i netperf-2.7.0-1.el7.lux.x86_64.rpm
rm -rf netperf-2.7.0-1.el7.lux.x86_64.rpm

## 配置avahi
wget -c http://smb.zstack.io/mirror/mingmin.wen/tools/avahi-0.6.31-20.el7.x86_64.rpm
wget -c http://smb.zstack.io/mirror/mingmin.wen/tools/avahi-libs-0.6.31-20.el7.x86_64.rpm
wget -c http://smb.zstack.io/mirror/mingmin.wen/tools/avahi-tools-0.6.31-20.el7.x86_64.rpm
yum localinstall -y avahi-libs-0.6.31-20.el7.x86_64.rpm avahi-0.6.31-20.el7.x86_64.rpm avahi-tools-0.6.31-20.el7.x86_64.rpm
rm -rf avahi-libs-0.6.31-20.el7.x86_64.rpm avahi-0.6.31-20.el7.x86_64.rpm avahi-tools-0.6.31-20.el7.x86_64.rpm
yum install avahi.x86_64 avahi-glib.x86_64 avahi-libs.x86_64 avahi-autoipd.x86_64 avahi-tools.x86_64

#部分系统还有这个依赖的问题
perl -v
sudo dnf install perl-Time-HiRes  -y
sudo  yum   install perl-Time-HiRes  -y 
#在正式开始前一定要进行预热   
sudo   yum  install    fio -y

#关心的磁盘性能    
#顺序读   顺序写     关心带宽      选取   numjobs 1   libaio   bs  1M    iodepth深度64    时间120s
#小块随机读   随机写     关心iops    选取 numjobs 64   libaio   bs  4k   iodepth深度64    时间120s
#小块随机    关心时延     numjobs  1       sync    bs  4k      iodepth深度1     时间120s

#例子 name  bs   time             深度  块大小  dircert  numjobs
# warm	1M	      120    write	    64  50G	     1	    1	libaio
# seqwrite	1M	360s	   write	64	50G	     1	    1	libaio
# seqread	1M	120s	    read	64	50G	     1	    1	libaio
# randwrite	4k	360s	randwrite	64	50G	     1	    64	libaio
# randread	4k	120s	randread	64	50G      1      64	libaio
# latwrite	4k	360s	randwrite	1	50G	     1	    1	sync
# latread	4k	120s	randread	1	50G	     1	    1	sync


#一般有2快盘    自己用df-h差一盘写入log文件    到时候我方便看 
# 定义磁盘名字变量和日志文件路径

# 磁盘名字变量和日志文件路径
disk_name="/dev/sdb"
log_file="/var/log/fio_test.log"

# 函数：记录日志
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$log_file"
}

# 函数：倒计时
countdown() {
    local seconds=$1
    while [ $seconds -gt 0 ]; do
        printf "%d 秒后开始...\r" $seconds
        sleep 1
        ((seconds--))
    done
    echo
}

# 确保日志文件存在
mkdir -p "$(dirname "$log_file")"
touch "$log_file"

# 预热测试
log "开始预热测试。预热测试时间为180秒。"
echo '预热测试开始，时间180s'
echo '预热测试开始，numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime=180 -rw=write --time_based=1'
countdown 3 # 倒计时3秒准备
fio -name warmup -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime=180 -rw=write --time_based=1 | tee -a "$log_file"
log "预热测试完成。"
echo '预热测试完成'
sleep 30

# 顺序写入测试

    log "开始顺序写入测试，任务数为 $numjobs。"
    echo "开始顺序写入测试，任务数为 $numjobs"
    countdown 3
    fio -name seqwrite -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=300 -rw=write --time_based=1 | tee -a "$log_file"
    log "顺序写入测试完成，任务数为 $numjobs。"
    sleep 30


# 顺序读出测试
log "开始顺序读出测试。"
echo "开始顺序读出测试"
countdown 3
fio -name seqread -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=300 -rw=read --time_based=1 | tee -a "$log_file"
log "顺序读出测试完成。"
sleep 30

# 随机写入测试
log "开始随机写入测试。"
echo "开始随机写入测试"
countdown 3
fio -name randwrite -filename="$disk_name" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime=300 -rw=randwrite --time_based=1 | tee -a "$log_file"
log "随机写入测试完成。"
sleep 30

# 随机读取测试
log "开始随机读取测试。"
echo "开始随机读取测试"
countdown 3
fio -name randread -filename="$disk_name" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime=300 -rw=randread --time_based=1 | tee -a "$log_file"
log "随机读取测试完成。"
sleep 30

# 高延迟写入测试
log "开始高延迟写入测试。"
echo "开始高延迟写入测试"
countdown 3
fio -name latwrite -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=sync -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=300 -rw=randwrite --time_based=1 | tee -a "$log_file"
log "高延迟写入测试完成。"
sleep 30

# 高延迟读取测试
log "开始高延迟读取测试。"
echo "开始高延迟读取测试"
countdown 3
fio -name latread -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=sync -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=300 -rw=randread --time_based=1 | tee -a "$log_file"
log "高延迟读取测试完成。"
sleep 30

log "所有测试已完成。日志已保存在 $log_file。"
echo '所有测试已完成，日志已保存在 $log_file'

# # 定义开始时间（如果需要的话）
# # START_TIME="2023-01-01 12:00:00"
# START_TIME=""

# # 磁盘名字变量和日志文件路径
# disk_name="/dev/sda"
# log_file="/var/log/fio_test.log"

# # 函数：记录日志
# log() {
#     echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$log_file"
# }

# # 函数：等待直到达到指定的时间点
# wait_until() {
#     local target_time=$1
#     while [[ $(date '+%Y-%m-%d %H:%M:%S') < $target_time ]]; do
#         sleep 1
#     done
# }

# # 确保日志文件存在
# mkdir -p "$(dirname "$log_file")"
# touch "$log_file"

# # 如果定义了开始时间，等待直到达到该时间点
# if [[ -n $START_TIME ]]; then
#     log "Waiting until $START_TIME before starting tests."
#     wait_until "$START_TIME"
# fi

# # 预热测试
# log "Starting warmup test.预热测试一下"
# echo 'Starting warmup test.预热测试一下   时间180s'

# fio -name warmup -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime=180 -rw=write --time_based=1 | tee -a "$log_file"
# sleep 30

# # 顺序写入测试
# for numjobs in 1 10; do
#     log "Starting sequential write test with $numjobs job(s)."
#     fio -name seqwrite -filename="$disk_name" --numjobs="$numjobs" --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=100 -rw=write --time_based=1 | tee -a "$log_file"
#     sleep 30
# done

# # 顺序读出测试
# log "Starting sequential read test."
# fio -name seqread -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=100 -rw=read --time_based=1 | tee -a "$log_file"
# sleep 30

# # 随机写入测试
# log "Starting random write test."
# fio -name randwrite -filename="$disk_name" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime=100 -rw=randwrite --time_based=1 | tee -a "$log_file"
# sleep 30

# # 随机读取测试
# log "Starting random read test."
# fio -name randread -filename="$disk_name" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime=100 -rw=randread --time_based=1 | tee -a "$log_file"
# sleep 30

# # 高延迟写入测试
# log "Starting latency write test."
# fio -name latwrite -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=sync -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=100 -rw=randwrite --time_based=1 | tee -a "$log_file"
# sleep 30

# # 高延迟读取测试
# log "Starting latency read test."
# fio -name latread -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=sync -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=100 -rw=randread --time_based=1 | tee -a "$log_file"
# sleep 30

# log "All tests completed. Logs saved in $log_file."
# # disk_name="/dev/sda"
# log_file="/var/log/fio_test.log"
# yum  install   fio 

# # 确保日志文件存在
# mkdir -p "$(dirname "$log_file")"
# touch "$log_file"

# # 函数：记录日志
# log() {
#     echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$log_file"
# }
# echo "欢迎使用磁盘性能测试脚本！"
# echo "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
# # 预热测试，执行3分钟
# echo -e "正在启动预热测试..."
# log "Starting warmup test."
# fio -name warmup -filename="$disk_name" --numjobs=1 --allow_mounted_write=1  -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime=180 -rw=write --time_based=1 | tee -a "$log_file"
# log "Warmup test completed."
# echo -e "预热测试完成。\n"
# # 顺序写入测试
# echo -e "正在启动顺序写入测试..."
# for numjobs in 1 10; do
#     log "Starting sequential write test with $numjobs job(s)."
#     fio -name seqwrite -filename="$disk_name" --numjobs="$numjobs" --allow_mounted_write=1  -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=100 -rw=write --time_based=1 | tee -a "$log_file"
#     log "Sequential write test with $numjobs job(s) completed."
# done
# echo -e "顺序写入测试完成。\n"
# echo -e "正在启动顺序读出测试..."
# # 顺序读出测试
# log "Starting sequential read test."
# fio -name seqread -filename="$disk_name" --numjobs=1 --allow_mounted_write=1   -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=100 -rw=read --time_based=1 | tee -a "$log_file"
# log "Sequential read test completed."
# echo -e "正在完成顺序读出测试..."
# echo -e "正在随机写入测试测试..."
# # 随机写入测试
# # 随机写入测试   buxian
# echo -e "测试完成日志保存在/var/log/fio_test.log"
```

#                                                                             张磊 : fio的脚本本本                                            

​                                                                            Created by  张磊 on 十一月 05, 2024                        

```
#!/bin/bash
#＃　　用于CPU跑分　　　　使用UNIXｂｅｎｃｈ　　　　获得的是最后的单核分数　　
#＃ｗｇｅｔ　　一个阿里云的ｙｕｍ镜像　　esfvfv 　　把他启用起来　　　
cd /etc
sudo yum upgrade
cd yum.repo.d
wget http://smb.zstack.io/mirror/lei.zhang/h84ryumrepo/zstack-aliyun-yum.repo
rm -rf /zapt
yum install git -y
cd /

mkdir /zapt
cd /zapt
git clone http://dev.zstack.io:9080/longtao.wu/apt_tools.git
rm -rf /apt_tools/.git
## 安装iperf3
yum install iperf3 -y
# 安装netperf
wget -c http://smb.zstack.io/mirror/mingmin.wen/tools/netperf-2.7.0-1.el7.lux.x86_64.rpm
rpm -i netperf-2.7.0-1.el7.lux.x86_64.rpm
rm -rf netperf-2.7.0-1.el7.lux.x86_64.rpm

## 配置avahi
wget -c http://smb.zstack.io/mirror/mingmin.wen/tools/avahi-0.6.31-20.el7.x86_64.rpm
wget -c http://smb.zstack.io/mirror/mingmin.wen/tools/avahi-libs-0.6.31-20.el7.x86_64.rpm
wget -c http://smb.zstack.io/mirror/mingmin.wen/tools/avahi-tools-0.6.31-20.el7.x86_64.rpm
yum localinstall -y avahi-libs-0.6.31-20.el7.x86_64.rpm avahi-0.6.31-20.el7.x86_64.rpm avahi-tools-0.6.31-20.el7.x86_64.rpm
rm -rf avahi-libs-0.6.31-20.el7.x86_64.rpm avahi-0.6.31-20.el7.x86_64.rpm avahi-tools-0.6.31-20.el7.x86_64.rpm
yum install avahi.x86_64 avahi-glib.x86_64 avahi-libs.x86_64 avahi-autoipd.x86_64 avahi-tools.x86_64

#部分系统还有这个依赖的问题
perl -v
sudo dnf install perl-Time-HiRes  -y
sudo  yum   install perl-Time-HiRes  -y 
#在正式开始前一定要进行预热   
sudo   yum  install    fio -y

#关心的磁盘性能    
#顺序读   顺序写     关心带宽      选取   numjobs 1   libaio   bs  1M    iodepth深度64    时间120s
#小块随机读   随机写     关心iops    选取 numjobs 64   libaio   bs  4k   iodepth深度64    时间120s
#小块随机    关心时延     numjobs  1       sync    bs  4k      iodepth深度1     时间120s

#例子 name  bs   time             深度  块大小  dircert  numjobs
# warm	1M	      120    write	    64  50G	     1	    1	libaio
# seqwrite	1M	360s	   write	64	50G	     1	    1	libaio
# seqread	1M	120s	    read	64	50G	     1	    1	libaio
# randwrite	4k	360s	randwrite	64	50G	     1	    64	libaio
# randread	4k	120s	randread	64	50G      1      64	libaio
# latwrite	4k	360s	randwrite	1	50G	     1	    1	sync
# latread	4k	120s	randread	1	50G	     1	    1	sync


#一般有2快盘    自己用df-h差一盘写入log文件    到时候我方便看 
# 定义磁盘名字变量和日志文件路径

# 磁盘名字变量和日志文件路径
disk_name="/dev/sdb"
log_file="/var/log/fio_test.log"

# 函数：记录日志
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$log_file"
}

# 函数：倒计时
countdown() {
    local seconds=$1
    while [ $seconds -gt 0 ]; do
        printf "%d 秒后开始...\r" $seconds
        sleep 1
        ((seconds--))
    done
    echo
}

# 确保日志文件存在
mkdir -p "$(dirname "$log_file")"
touch "$log_file"

# 预热测试
log "开始预热测试。预热测试时间为180秒。"
echo '预热测试开始，时间180s'
echo '预热测试开始，numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime=180 -rw=write --time_based=1'
countdown 3 # 倒计时3秒准备
fio -name warmup -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime=180 -rw=write --time_based=1 | tee -a "$log_file"
log "预热测试完成。"
echo '预热测试完成'
sleep 30

# 顺序写入测试

    log "开始顺序写入测试，任务数为 $numjobs。"
    echo "开始顺序写入测试，任务数为 $numjobs"
    countdown 3
    fio -name seqwrite -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=300 -rw=write --time_based=1 | tee -a "$log_file"
    log "顺序写入测试完成，任务数为 $numjobs。"
    sleep 30


# 顺序读出测试
log "开始顺序读出测试。"
echo "开始顺序读出测试"
countdown 3
fio -name seqread -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=300 -rw=read --time_based=1 | tee -a "$log_file"
log "顺序读出测试完成。"
sleep 30

# 随机写入测试
log "开始随机写入测试。"
echo "开始随机写入测试"
countdown 3
fio -name randwrite -filename="$disk_name" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime=300 -rw=randwrite --time_based=1 | tee -a "$log_file"
log "随机写入测试完成。"
sleep 30

# 随机读取测试
log "开始随机读取测试。"
echo "开始随机读取测试"
countdown 3
fio -name randread -filename="$disk_name" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime=300 -rw=randread --time_based=1 | tee -a "$log_file"
log "随机读取测试完成。"
sleep 30

# 高延迟写入测试
log "开始高延迟写入测试。"
echo "开始高延迟写入测试"
countdown 3
fio -name latwrite -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=sync -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=300 -rw=randwrite --time_based=1 | tee -a "$log_file"
log "高延迟写入测试完成。"
sleep 30

# 高延迟读取测试
log "开始高延迟读取测试。"
echo "开始高延迟读取测试"
countdown 3
fio -name latread -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=sync -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=300 -rw=randread --time_based=1 | tee -a "$log_file"
log "高延迟读取测试完成。"
sleep 30

log "所有测试已完成。日志已保存在 $log_file。"
echo '所有测试已完成，日志已保存在 $log_file'

# # 定义开始时间（如果需要的话）
# # START_TIME="2023-01-01 12:00:00"
# START_TIME=""

# # 磁盘名字变量和日志文件路径
# disk_name="/dev/sda"
# log_file="/var/log/fio_test.log"

# # 函数：记录日志
# log() {
#     echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$log_file"
# }

# # 函数：等待直到达到指定的时间点
# wait_until() {
#     local target_time=$1
#     while [[ $(date '+%Y-%m-%d %H:%M:%S') < $target_time ]]; do
#         sleep 1
#     done
# }

# # 确保日志文件存在
# mkdir -p "$(dirname "$log_file")"
# touch "$log_file"

# # 如果定义了开始时间，等待直到达到该时间点
# if [[ -n $START_TIME ]]; then
#     log "Waiting until $START_TIME before starting tests."
#     wait_until "$START_TIME"
# fi

# # 预热测试
# log "Starting warmup test.预热测试一下"
# echo 'Starting warmup test.预热测试一下   时间180s'

# fio -name warmup -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime=180 -rw=write --time_based=1 | tee -a "$log_file"
# sleep 30

# # 顺序写入测试
# for numjobs in 1 10; do
#     log "Starting sequential write test with $numjobs job(s)."
#     fio -name seqwrite -filename="$disk_name" --numjobs="$numjobs" --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=100 -rw=write --time_based=1 | tee -a "$log_file"
#     sleep 30
# done

# # 顺序读出测试
# log "Starting sequential read test."
# fio -name seqread -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=100 -rw=read --time_based=1 | tee -a "$log_file"
# sleep 30

# # 随机写入测试
# log "Starting random write test."
# fio -name randwrite -filename="$disk_name" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime=100 -rw=randwrite --time_based=1 | tee -a "$log_file"
# sleep 30

# # 随机读取测试
# log "Starting random read test."
# fio -name randread -filename="$disk_name" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime=100 -rw=randread --time_based=1 | tee -a "$log_file"
# sleep 30

# # 高延迟写入测试
# log "Starting latency write test."
# fio -name latwrite -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=sync -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=100 -rw=randwrite --time_based=1 | tee -a "$log_file"
# sleep 30

# # 高延迟读取测试
# log "Starting latency read test."
# fio -name latread -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=sync -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=100 -rw=randread --time_based=1 | tee -a "$log_file"
# sleep 30

# log "All tests completed. Logs saved in $log_file."
# # disk_name="/dev/sda"
# log_file="/var/log/fio_test.log"
# yum  install   fio 

# # 确保日志文件存在
# mkdir -p "$(dirname "$log_file")"
# touch "$log_file"

# # 函数：记录日志
# log() {
#     echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$log_file"
# }
# echo "欢迎使用磁盘性能测试脚本！"
# echo "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
# # 预热测试，执行3分钟
# echo -e "正在启动预热测试..."
# log "Starting warmup test."
# fio -name warmup -filename="$disk_name" --numjobs=1 --allow_mounted_write=1  -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime=180 -rw=write --time_based=1 | tee -a "$log_file"
# log "Warmup test completed."
# echo -e "预热测试完成。\n"
# # 顺序写入测试
# echo -e "正在启动顺序写入测试..."
# for numjobs in 1 10; do
#     log "Starting sequential write test with $numjobs job(s)."
#     fio -name seqwrite -filename="$disk_name" --numjobs="$numjobs" --allow_mounted_write=1  -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=100 -rw=write --time_based=1 | tee -a "$log_file"
#     log "Sequential write test with $numjobs job(s) completed."
# done
# echo -e "顺序写入测试完成。\n"
# echo -e "正在启动顺序读出测试..."
# # 顺序读出测试
# log "Starting sequential read test."
# fio -name seqread -filename="$disk_name" --numjobs=1 --allow_mounted_write=1   -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=100 -rw=read --time_based=1 | tee -a "$log_file"
# log "Sequential read test completed."
# echo -e "正在完成顺序读出测试..."
# echo -e "正在随机写入测试测试..."
# # 随机写入测试
# # 随机写入测试   buxian
# echo -e "测试完成日志保存在/var/log/fio_test.log"
```

# 脚本  使用fio进行本地磁盘IO测试的脚本                                            

​                                                                            Created by  张磊, last modified on 十一月 05, 2024                        

```

#!/bin/bash

# 定义磁盘名字变量和日志文件路径
disk_name="/dev/sda"
log_file="/var/log/fio_test.log"
yum  install   fio 

# 确保日志文件存在
mkdir -p "$(dirname "$log_file")"
touch "$log_file"

# 函数：记录日志
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$log_file"
}
echo "欢迎使用磁盘性能测试脚本！"
echo "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
# 预热测试，执行3分钟
echo -e "正在启动预热测试..."
log "Starting warmup test."
fio -name warmup -filename="$disk_name" --numjobs=1 --allow_mounted_write=1  -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime=180 -rw=write --time_based=1 | tee -a "$log_file"
log "Warmup test completed."
echo -e "预热测试完成。\n"
# 顺序写入测试
echo -e "正在启动顺序写入测试..."
for numjobs in 1 10; do
    log "Starting sequential write test with $numjobs job(s)."
    fio -name seqwrite -filename="$disk_name" --numjobs="$numjobs" --allow_mounted_write=1  -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=100 -rw=write --time_based=1 | tee -a "$log_file"
    log "Sequential write test with $numjobs job(s) completed."
done
echo -e "顺序写入测试完成。\n"
echo -e "正在启动顺序读出测试..."
# 顺序读出测试
log "Starting sequential read test."
fio -name seqread -filename="$disk_name" --numjobs=1 --allow_mounted_write=1   -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=100 -rw=read --time_based=1 | tee -a "$log_file"
log "Sequential read test completed."
echo -e "正在完成顺序读出测试..."
echo -e "正在随机写入测试测试..."
# 随机写入测试
# 随机写入测试   buxian
echo -e "测试完成日志保存在/var/log/fio_test.log"



















# #!/bin/bash

# # 定义磁盘名字变量
# disk_name="/dev/vda1"
# #存储预热   执行3分钟  
# fio -name warmup  -filename=/dev/sda --numjobs=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime=100 -rw=write --time_based=1
# fio -name warmup  -filename=/dev/sda --numjobs=10 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime=100 -rw=write --time_based=1
# #顺序写    大块   深度大  关心获得BW    job少    高吞吐
# fio -name seqwrite -filename=/dev/sda --numjobs=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=100 -rw=write --time_based=1
# fio -name seqwrite -filename=/dev/sda --numjobs=10 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=100 -rw=write --time_based=1
# #顺序读   大块        深度大  关心获得BW    job少    高吞吐
# fio -name seqwrite -filename=/dev/sda --numjobs=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=100 -rw=read --time_based=1
# # 随机 读写         小块      job多     深度大    关心iops

# fio -name seqwrite -filename=/dev/sda --numjobs=64 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime=100 -rw=randwrite --time_based=1
# fio -name seqwrite -filename=/dev/sda --numjobs=64 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime=100 -rw=randread --time_based=1
# # 随机读写    关心延时     小块     job少     深度低   模式为异步

# fio -name seqwrite -filename=/dev/sda --numjobs=64 -ioengine=sync -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=100 -rw=randwrite --time_based=1
# fio -name seqwrite -filename=/dev/sda --numjobs=64 -ioengine=sync -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=100 -rw=randread --time_based=1
# # # 函数：执行fio测试并计算最后三次平均值
# # run_fio_test() {
# #     local test_name=$1
# #     local rw_type=$2
# #     local runtime=$3
#     local bs=$4
#     local iodepth=$5
#     local size=$6
#     local time_based=$7

#     local -a results=() # 用于存储测试结果的数组

#     # 执行测试10次
#     for ((i=1; i<=3; i++)); do
#         echo "Running test ($i/10) for $test_name..."
#         # 执行fio命令并获取结果
#         result=$(fio --name="$test_name" --filename="$disk_name" --ioengine=libaio --direct=1 --group_reporting --bs="$bs" --iodepth="$iodepth" --size="$size" --runtime="$runtime" --rw="$rw_type" --time_based="$time_based" --output-format=json)
#         # 从json输出中提取BW或IOPS值
#         value=$(echo "$result" | jq -r '.jq[0] bw')
#         results+=($value)
#     done

#     # 计算最后三次测试的平均值
#     local last_three_sum=$(echo "${results[@]: -3}" | paste -sd+ - | bc)
#     local final_average=$(echo "scale=2; $last_three_sum / 3" | bc)

#     # 输出最终结果
#     echo "Final average for $test_name: $final_average"
# }

# # 顺序写入带宽测试
# run_fio_test "seqwrite" "write" 360 "1M" "64" "50G" "true"

# # 顺序读出带宽测试
# run_fio_test "seqread" "read" 120 "1M" "64" "50G" "true"

# # 随机写入IOPS测试
# run_fio_test "randwrite" "randwrite" 360 "4k" "64" "50G" "false"

# # 随机读出IOPS测试
# run_fio_test "randread" "randread" 120 "4k" "64" "50G" "false"

# # 深度随机写入测试 (iodepth=1)
# run_fio_test "randwrite_depth" "randwrite" 360 "4k" "1" "50G" "false"

# # 深度随机读出测试 (iodepth=1)
# run_fio_test "randread_depth" "randread" 120 "4k" "1" "50G" "false"
















# #!/bin/bash
# 顺序写带宽测试；以下指令重复10次观察记录输出的BW=$bw值,取后三次平均值作为最终值（换算成MiB/s）

# linux：fio -name seqwrite -filename=$driver –numjobs=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 –size=50G -runtime=360 -rw=write –time_based
# windows：fio -name seqwrite -filename=$driver –numjobs=1 -direct=1 -group_reporting -bs=1M -iodepth=64 –size=50G -runtime=360 -rw=write –time_based
# 顺序读带宽测试；测试前需保证待测磁盘已经写满，一般可用顺序写带宽指令跑两遍；以下指令重复10次观察记录输出的BW=$bw值,取后三次平均值作为最终值（换算成MiB/s）

# linux:fio -name seqread -filename=$driver –numjobs=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 –size=50G -runtime=120 -rw=read –time_based
# windows:fio -name seqread -filename=$driver –numjobs=1 -direct=1 -group_reporting -bs=1M -iodepth=64 –size=50G -runtime=120 -rw=read –time_based
# 随机写IOPS测试；以下指令重复10次观察记录输出的IOPS=$iops值,取后三次平均值作为最终值
# linux：fio -name randwrite -filename=$driver –numjobs=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 –size=50G -runtime=360 -rw=randwrite –time_based
# windows：fio -name randwrite -filename=$driver –numjobs=1 -direct=1 -group_reporting -bs=4k -iodepth=64 –size=50G -runtime=360 -rw=randwrite –time_based
# 随机读IOPS测试；测试前需保证待测磁盘已经写满，一般可用顺序写带宽指令跑两遍；以下指令重复10次观察记录输出的IOPS=$iops值,取后三次平均值作为最终值
# linux：fio -name randread -filename=$driver –numjobs=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 –size=50G -runtime=120 -rw=randread –time_based
# windows：fio -name randread -filename=$driver –numjobs=1 -direct=1 -group_reporting -bs=4k -iodepth=64 –size=50G -runtime=120 -rw=randread –time_based
# 深度随机写测试；以下指令重复10次观察记录输出的IOPS=$iops值、clat中avg=$avg值、99.90th[$th]值,各取后三次平均值作为最终值（clat值与99.90th值换算成msec）
# linux:fio -name randwrite -filename=$driver –numjobs=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=1 –size=50G -runtime=360 -rw=randwrite –time_based
# windows:fio -name randwrite -filename=$driver –numjobs=1 -direct=1 -group_reporting -bs=4k -iodepth=1 –size=50G -runtime=360 -rw=randwrite –time_based
# 深度随机读测试；测试前需保证待测磁盘已经写满，一般可用顺序写带宽指令跑两遍；以下指令重复10次观察记录输出的IOPS=$iops值、clat中avg=$avg值、99.90th[$th]值,各取后三次平均值作为最终值（clat值与99.90th值换算成msec）
# linux:fio -name randread -filename=$driver –numjobs=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=1 –size=50G -runtime=120 -rw=randread –time_based
# windows:fio -name randread -filename=$driver –numjobs=1 -direct=1 -group_reporting -bs=4k -iodepth=1 –size=50G -runtime=120 -rw=randread –time_based
# 重要场景实例＃　linux中$driver 使用fdisk -l 来查看

# windows 中$driver 使用 wmic diskdrive get deviceid 来查看 一般为‘\.\PHYSICALDRIVE1
# 1.　大块顺序读写　　　看带宽
# 2.小块随机读写　　　　看ｉｏｐｓ期望        存储    机械硬盘      iops和读写带宽的损耗应该是不大的      10以内  

# SATA盘的话        20  到30    预估  

# NVME                iops    带宽   20  30        延迟  可能干到50   

# 性能参数  配置   说针对虚拟机级别，有一些什么AIO, 还有什么predication，就是预分配策略或者什么    都需要配
# 3.

# #     问题    测试有问题     关心NVEME盘的数据     关心HDD盘的数据　　

# # # ＃核心的得到的数据　ｉｏｐｓ　　ｂｗ　　　　　ｌａｔ　　　　
# # ＃核心的得到的数据　低延迟iodepth、numjobs均设置1、IO引擎使用sync高IOPS/高带宽iodepth、
# # numjobs根据实际情况调整Iodepth一般128、IO引擎使用libaio　　　　　　
# # 定义测试参数fio   顺序读写         注意BS        大块        关心带宽  

# # fio    随机读写         注意BS   一般 4k    关心    iops  

# # # 随机写延迟      BS   4k    ios   深度1     观察整体输出    重点看一下     DV latency, 一个是什么LSLATE，有多个license. 这个license指的是说我每个IO在不同的完成阶段，它的一个指标
# # test_name="seqwrite"
# # block_size="1M"
# # iodepth="64"
# # test_size="50G"
# # runtime="360"
# # rw_type="write"
# # time_based="true"

# # # 查找大于30GB且未被挂载的磁盘（注意：这里简化处理，未考虑分区情况，根据实际情况调整）
# # disks=$(lsblk -b --output NAME,SIZE,MOUNTPOINT | awk '$2>31457280 && $3=="" {print $1}')

# # # 遍历找到的磁盘并执行FIO测试
# # for disk in $disks; do
# #     echo "Found disk: $disk, starting FIO test..."
# #     # 构建FIO命令，注意使用绝对路径和必要的安全检查
# #     fio_cmd="fio --name=$test_name --filename=/dev/$disk --ioengine=libaio --direct=1 --group_reporting --bs=$block_size --iodepth=$iodepth --size=$test_size --runtime=$runtime --rw=$rw_type"
# #     if [ "$time_based" = "true" ]; then
# #         fio_cmd="$fio_cmd --time_based"
# #     fi

# #     # 执行FIO命令
# #     echo "Executing: $fio_cmd"
# #     eval "$fio_cmd"
# #     echo "FIO test completed on $disk."
# # done

# # # 如果没有找到符合条件的磁盘，给出提示
# # if [ -z "$disks" ]; then
# #     echo "No disks larger than 30GB found that are not mounted."
# # fi

# #  fio --name=seqwrite --filename=/dev/vda1 --ioengine=libaio --direct=1 --group_reporting --bs=1M --iodepth=64 --size=50G --runtime=3 --rw=write --time_based 
# #   echo "No disks larger than 30GB found that are not mounted.顺序写入50G的数据“

# #   fio --name=seqread --filename=/dev/vda1 --ioengine=libaio --direct=1 --group_reporting --bs=1M --iodepth=64 --size=50G --runtime=3 --rw=read --time_based
# #   echo "No disks larger than 30GB found that are not mounted.顺序读入入50G的数据“

# # fio --name=randwrite_single --filename=/dev/vda1 --numjobs=1 --ioengine=libaio --direct=1 --group_reporting --bs=4k --iodepth=64 --size=50G --runtime=360 --rw=randwrite --time_based

# # fio --name=randread_single --filename=/dev/vda1 --numjobs=1 --ioengine=libaio --direct=1 --group_reporting --bs=4k --iodepth=64 --size=50G --runtime=360 --rw=randread --time_based


# # fio --name=randread_single --filename=/dev/vda1 --numjobs=1 --ioengine=libaio --direct=1 --group_reporting --bs=4k --iodepth=1 --size=50G --runtime=360 --rw=randread --time_based

# # fio --name=randwrite_latency --filename=/dev/vda1 --ioengine=libaio --direct=1 --group_reporting --bs=4k --iodepth=1 --size=50G --runtime=360 --rw=randwrite --time_based --norandommap








# #!/bin/bash

# # 定义磁盘名字变量
# disk_name="/dev/vda1"

# # 函数：执行fio测试并计算最后三次平均值
# run_fio_test() {
#     local test_name=$1
#     local rw_type=$2
#     local runtime=$3
#     local bs=$4
#     local iodepth=$5
#     local size=$6
#     local time_based=$7

#     local -a results=() # 用于存储测试结果的数组

#     # 执行测试10次
#     for ((i=1; i<=3; i++)); do
#         echo "Running test ($i/10) for $test_name..."
#         # 执行fio命令并获取结果
#         result=$(fio --name="$test_name" --filename="$disk_name" --ioengine=libaio --direct=1 --group_reporting --bs="$bs" --iodepth="$iodepth" --size="$size" --runtime="$runtime" --rw="$rw_type" --time_based="$time_based" --output-format=json)
#         # 从json输出中提取BW或IOPS值
#         value=$(echo "$result" | jq -r '.jq[0] bw')
#         results+=($value)
#     done

#     # 计算最后三次测试的平均值
#     local last_three_sum=$(echo "${results[@]: -3}" | paste -sd+ - | bc)
#     local final_average=$(echo "scale=2; $last_three_sum / 3" | bc)

#     # 输出最终结果
#     echo "Final average for $test_name: $final_average"
# }

# # 顺序写入带宽测试
# run_fio_test "seqwrite" "write" 360 "1M" "64" "50G" "true"

# # 顺序读出带宽测试
# run_fio_test "seqread" "read" 120 "1M" "64" "50G" "true"

# # 随机写入IOPS测试
# run_fio_test "randwrite" "randwrite" 360 "4k" "64" "50G" "false"

# # 随机读出IOPS测试
# run_fio_test "randread" "randread" 120 "4k" "64" "50G" "false"

# # 深度随机写入测试 (iodepth=1)
# run_fio_test "randwrite_depth" "randwrite" 360 "4k" "1" "50G" "false"

# # 深度随机读出测试 (iodepth=1)
# run_fio_test "randread_depth" "randread" 120 "4k" "1" "50G" "false"
















# # #!/bin/bash
# # 顺序写带宽测试；以下指令重复10次观察记录输出的BW=$bw值,取后三次平均值作为最终值（换算成MiB/s）

# # linux：fio -name seqwrite -filename=$driver –numjobs=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 –size=50G -runtime=360 -rw=write –time_based
# # windows：fio -name seqwrite -filename=$driver –numjobs=1 -direct=1 -group_reporting -bs=1M -iodepth=64 –size=50G -runtime=360 -rw=write –time_based
# # 顺序读带宽测试；测试前需保证待测磁盘已经写满，一般可用顺序写带宽指令跑两遍；以下指令重复10次观察记录输出的BW=$bw值,取后三次平均值作为最终值（换算成MiB/s）

# # linux:fio -name seqread -filename=$driver –numjobs=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 –size=50G -runtime=120 -rw=read –time_based
# # windows:fio -name seqread -filename=$driver –numjobs=1 -direct=1 -group_reporting -bs=1M -iodepth=64 –size=50G -runtime=120 -rw=read –time_based
# # 随机写IOPS测试；以下指令重复10次观察记录输出的IOPS=$iops值,取后三次平均值作为最终值
# # linux：fio -name randwrite -filename=$driver –numjobs=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 –size=50G -runtime=360 -rw=randwrite –time_based
# # windows：fio -name randwrite -filename=$driver –numjobs=1 -direct=1 -group_reporting -bs=4k -iodepth=64 –size=50G -runtime=360 -rw=randwrite –time_based
# # 随机读IOPS测试；测试前需保证待测磁盘已经写满，一般可用顺序写带宽指令跑两遍；以下指令重复10次观察记录输出的IOPS=$iops值,取后三次平均值作为最终值
# # linux：fio -name randread -filename=$driver –numjobs=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 –size=50G -runtime=120 -rw=randread –time_based
# # windows：fio -name randread -filename=$driver –numjobs=1 -direct=1 -group_reporting -bs=4k -iodepth=64 –size=50G -runtime=120 -rw=randread –time_based
# # 深度随机写测试；以下指令重复10次观察记录输出的IOPS=$iops值、clat中avg=$avg值、99.90th[$th]值,各取后三次平均值作为最终值（clat值与99.90th值换算成msec）
# # linux:fio -name randwrite -filename=$driver –numjobs=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=1 –size=50G -runtime=360 -rw=randwrite –time_based
# # windows:fio -name randwrite -filename=$driver –numjobs=1 -direct=1 -group_reporting -bs=4k -iodepth=1 –size=50G -runtime=360 -rw=randwrite –time_based
# # 深度随机读测试；测试前需保证待测磁盘已经写满，一般可用顺序写带宽指令跑两遍；以下指令重复10次观察记录输出的IOPS=$iops值、clat中avg=$avg值、99.90th[$th]值,各取后三次平均值作为最终值（clat值与99.90th值换算成msec）
# # linux:fio -name randread -filename=$driver –numjobs=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=1 –size=50G -runtime=120 -rw=randread –time_based
# # windows:fio -name randread -filename=$driver –numjobs=1 -direct=1 -group_reporting -bs=4k -iodepth=1 –size=50G -runtime=120 -rw=randread –time_based
# # 重要场景实例＃　linux中$driver 使用fdisk -l 来查看

# # windows 中$driver 使用 wmic diskdrive get deviceid 来查看 一般为‘\.\PHYSICALDRIVE1
# # 1.　大块顺序读写　　　看带宽
# # 2.小块随机读写　　　　看ｉｏｐｓ期望        存储    机械硬盘      iops和读写带宽的损耗应该是不大的      10以内  

# # SATA盘的话        20  到30    预估  

# # NVME                iops    带宽   20  30        延迟  可能干到50   

# # 性能参数  配置   说针对虚拟机级别，有一些什么AIO, 还有什么predication，就是预分配策略或者什么    都需要配
# # 3.

# # #     问题    测试有问题     关心NVEME盘的数据     关心HDD盘的数据　　

# # # # ＃核心的得到的数据　ｉｏｐｓ　　ｂｗ　　　　　ｌａｔ　　　　
# # # ＃核心的得到的数据　低延迟iodepth、numjobs均设置1、IO引擎使用sync高IOPS/高带宽iodepth、
# # # numjobs根据实际情况调整Iodepth一般128、IO引擎使用libaio　　　　　　
# # # 定义测试参数fio   顺序读写         注意BS        大块        关心带宽  

# # # fio    随机读写         注意BS   一般 4k    关心    iops  

# # # # 随机写延迟      BS   4k    ios   深度1     观察整体输出    重点看一下     DV latency, 一个是什么LSLATE，有多个license. 这个license指的是说我每个IO在不同的完成阶段，它的一个指标
# # # test_name="seqwrite"
# # # block_size="1M"
# # # iodepth="64"
# # # test_size="50G"
# # # runtime="360"
# # # rw_type="write"
# # # time_based="true"

# # # # 查找大于30GB且未被挂载的磁盘（注意：这里简化处理，未考虑分区情况，根据实际情况调整）
# # # disks=$(lsblk -b --output NAME,SIZE,MOUNTPOINT | awk '$2>31457280 && $3=="" {print $1}')

# # # # 遍历找到的磁盘并执行FIO测试
# # # for disk in $disks; do
# # #     echo "Found disk: $disk, starting FIO test..."
# # #     # 构建FIO命令，注意使用绝对路径和必要的安全检查
# # #     fio_cmd="fio --name=$test_name --filename=/dev/$disk --ioengine=libaio --direct=1 --group_reporting --bs=$block_size --iodepth=$iodepth --size=$test_size --runtime=$runtime --rw=$rw_type"
# # #     if [ "$time_based" = "true" ]; then
# # #         fio_cmd="$fio_cmd --time_based"
# # #     fi

# # #     # 执行FIO命令
# # #     echo "Executing: $fio_cmd"
# # #     eval "$fio_cmd"
# # #     echo "FIO test completed on $disk."
# # # done

# # # # 如果没有找到符合条件的磁盘，给出提示
# # # if [ -z "$disks" ]; then
# # #     echo "No disks larger than 30GB found that are not mounted."
# # # fi

# # #  fio --name=seqwrite --filename=/dev/vda1 --ioengine=libaio --direct=1 --group_reporting --bs=1M --iodepth=64 --size=50G --runtime=3 --rw=write --time_based 
# # #   echo "No disks larger than 30GB found that are not mounted.顺序写入50G的数据“

# # #   fio --name=seqread --filename=/dev/vda1 --ioengine=libaio --direct=1 --group_reporting --bs=1M --iodepth=64 --size=50G --runtime=3 --rw=read --time_based
# # #   echo "No disks larger than 30GB found that are not mounted.顺序读入入50G的数据“

# # # fio --name=randwrite_single --filename=/dev/vda1 --numjobs=1 --ioengine=libaio --direct=1 --group_reporting --bs=4k --iodepth=64 --size=50G --runtime=360 --rw=randwrite --time_based

# # # fio --name=randread_single --filename=/dev/vda1 --numjobs=1 --ioengine=libaio --direct=1 --group_reporting --bs=4k --iodepth=64 --size=50G --runtime=360 --rw=randread --time_based


# # # fio --name=randread_single --filename=/dev/vda1 --numjobs=1 --ioengine=libaio --direct=1 --group_reporting --bs=4k --iodepth=1 --size=50G --runtime=360 --rw=randread --time_based

# # # fio --name=randwrite_latency --filename=/dev/vda1 --ioengine=libaio --direct=1 --group_reporting --bs=4k --iodepth=1 --size=50G --runtime=360 --rw=randwrite --time_based --norandommap
#!/bin/bash
cd   /etc/yum.repos.d
wget   http://smb.zstack.io/mirror/lei.zhang/h84ryumrepo/zstack-aliyun-yum.repo
sudo yum install -y fio
sudo yum clean  all
sudo yum makecache
sudo yum install unzip -y

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




# fio -name warmup -filename=/dev/sda1 --numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime="$runtime" -rw=write --time_based=1 | tee -a "$log_file"
#################################################################################################################################################################################################################33
figlet  "warmup"
figlet  ""
fio -name warmup    -filename=/dev/sda1 --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime=60 -rw=write     --time_based=1



figlet  "seqwrite"
fio -name seqwrite  -filename=/dev/sda1 --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64  --size=50G -runtime=10 -rw=write     --time_based=1
figlet  "seqread"
fio -name seqread   -filename=/dev/sda1 --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64  --size=50G -runtime=10 -rw=read      --time_based=1 


figlet "randwrite"
fio -name randwrite -filename=/dev/sda1 --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64  --size=50G -runtime=10 -rw=randwrite --time_based=1 
figlet "randread"
fio -name randread  -filename=/dev/sda1 --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64  --size=50G -runtime=10 -rw=randread  --time_based=1

figlet "latwrite"
fio -name latwrite  -filename=/dev/sda1 --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1   --size=50G -runtime=10 -rw=randwrite  --time_based=1
figlet "latread"
fio -name latread   -filename=/dev/sda1 --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1   --size=50G -runtime=10 -rw=randread   --time_based=1


figlet "latwritelb"
fio -name latwrite  -filename=/dev/sda1 --numjobs=1 --allow_mounted_write=1 -ioengine=libaio    -direct=1 -group_reporting -bs=4k -iodepth=1   --size=50G -runtime=10 -rw=randwrite  --time_based=1
figlet "latreadlb"
fio -name latread   -filename=/dev/sda1 --numjobs=1 --allow_mounted_write=1 -ioengine=libaio    -direct=1 -group_reporting -bs=4k -iodepth=1   --size=50G -runtime=10 -rw=randread   --time_based=1
#################################################################################################################################################################################################################33



#################################################################################################################################################################################################################33
#bin/bash
figlet  "warmup"
fio -name warmup    -filename=/dev/nvme0n1p6 --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime=100 -rw=write     --time_based=1
figlet  "seqwrite"
fio -name seqwrite  -filename=/dev/nvme0n1p6 --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime=10 -rw=write     --time_based=1 
figlet  "seqread"
fio -name seqread   -filename=/dev/nvme0n1p6 --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime=10 -rw=read      --time_based=1 

figlet "randwrite"
fio -name randwrite -filename=/dev/nvme0n1p6 --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=10G -runtime=10 -rw=randwrite --time_based=1 
figlet "randread"
fio -name randread  -filename=/dev/nvme0n1p6 --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=10G -runtime=10 -rw=randread  --time_based=1 

figlet "latwrite"
fio -name latwrite  -filename=/dev/nvme0n1p6 --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime=10 -rw=randwrite  --time_based=1 
figlet "latread"
fio -name latread   -filename=/dev/nvme0n1p6 --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime=10 -rw=randread   --time_based=1 


figlet "latwritelb"
fio -name latwrite  -filename=/dev/nvme0n1p6 --numjobs=1 --allow_mounted_write=1 -ioengine=libaio    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime=10 -rw=randwrite  --time_based=1 
figlet "latreadlb"
fio -name latread   -filename=/dev/nvme0n1p6 --numjobs=1 --allow_mounted_write=1 -ioengine=libaio    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime=10 -rw=randread   --time_based=1 
# #bin/bash
# fio -name seqwrite  -filename=/dev/nvme0n1p6 --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime=10 -rw=write     --time_based=1 | grep "write"
# fio -name seqread   -filename=/dev/nvme0n1p6 --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime=10 -rw=read      --time_based=1 | grep "read"

# fio -name randwrite -filename=/dev/nvme0n1p6 --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=10G -runtime=10 -rw=randwrite --time_based=1 | grep "write"
# fio -name randread  -filename=/dev/nvme0n1p6 --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=10G -runtime=10 -rw=randread  --time_based=1 | grep "read"

# fio -name latwrite  -filename=/dev/nvme0n1p6 --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime=10 -rw=randwrite  --time_based=1 | grepp "lat"
# fio -name latread   -filename=/dev/nvme0n1p6 --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime=10 -rw=randread   --time_based=1 | grep "lat"
#################################################################################################################################################################################################################33
 
 
 #################################################################################################################################################################################################################33
 figlet  "warmup"
fio -name warmup    -filename=/dev/sdb1 --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=100 -rw=write     --time_based=1
figlet  "seqwrite"
fio -name seqwrite  -filename=/dev/sdb1 --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=10 -rw=write     --time_based=1 
figlet  "seqread"
fio -name seqread   -filename=/dev/sdb1 --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=10 -rw=read      --time_based=1 

figlet "randwrite"
fio -name randwrite -filename=/dev/sdb1 --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime=10 -rw=randwrite --time_based=1 
figlet "randread"
fio -name randread  -filename=/dev/sdb1 --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime=10 -rw=randread  --time_based=1 

figlet "latwrite"
fio -name latwrite  -filename=/dev/sdb1 --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=10 -rw=randwrite  --time_based=1 
figlet "latread"
fio -name latread   -filename=/dev/sdb1 --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=10 -rw=randread   --time_based=1 
 
 figlet "latwritelb"
fio -name latwrite  -filename=/dev/sdb1 --numjobs=1 --allow_mounted_write=1 -ioengine=libaio   -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=10 -rw=randwrite  --time_based=1 
figlet "latreadlb"
fio -name latread   -filename=/dev/sdb1 --numjobs=1 --allow_mounted_write=1 -ioengine=libaio    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=10 -rw=randread   --time_based=1 
 
 
#!/bin/bash
cd   /etc/yum.repos.d
wget   http://smb.zstack.io/mirror/lei.zhang/h84ryumrepo/zstack-aliyun-yum.repo
sudo yum install -y fio
sudo yum clean  all
sudo yum makecache
sudo yum install unzip -y

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

log_file="/root/fiologfile.log" # 日志文件
disk_a=/dev/vdb  
disk_b=/dev/vdc 
disk_c=/dev/vdd 
runtime=100 
if [ ! -f "$log_file" ]; then
    echo "Log file not found."
    touch "$log_file"
    figlet  "getlog"
    figlet  "getlog----->Good!"
   
fi

if [ ! -f "$log_file" ]; then
    
     figlet  "getlog----->Good!"
   
fi




# fio -name warmup -filename="$disk_a" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime="$runtime" -rw=write --time_based=1 | tee -a "$log_file"
#################################################################################################################################################################################################################33
figlet  "warmup" | tee -a "$log_file"
figlet  ""| tee -a "$log_file"
fio -name warmup    -filename="$disk_a" --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime="$runtime" -rw=write     --time_based=1 | tee -a "$log_file"



figlet  "seqwrite"
fio -name seqwrite  -filename="$disk_a" --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64  --size=50G -runtime="$runtime" -rw=write     --time_based=1 | tee -a "$log_file"
figlet  "seqread"
fio -name seqread   -filename="$disk_a" --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64  --size=50G -runtime="$runtime" -rw=read      --time_based=1  | tee -a "$log_file"


figlet "randwrite"
fio -name randwrite -filename="$disk_a" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64  --size=50G -runtime="$runtime" -rw=randwrite --time_based=1  | tee -a "$log_file"
figlet "randread"
fio -name randread  -filename="$disk_a" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64  --size=50G -runtime="$runtime" -rw=randread  --time_based=1 | tee -a "$log_file"

figlet "latwrite"
fio -name latwrite  -filename="$disk_a" --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1   --size=50G -runtime="$runtime" -rw=randwrite  --time_based=1 | tee -a "$log_file"
figlet "latread"
fio -name latread   -filename="$disk_a" --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1   --size=50G -runtime="$runtime" -rw=randread   --time_based=1 | tee -a "$log_file"


figlet "latwritelb"
fio -name latwrite  -filename="$disk_a" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio    -direct=1 -group_reporting -bs=4k -iodepth=1   --size=50G -runtime="$runtime" -rw=randwrite  --time_based=1 | tee -a "$log_file"
figlet "latreadlb"
fio -name latread   -filename="$disk_a" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio    -direct=1 -group_reporting -bs=4k -iodepth=1   --size=50G -runtime="$runtime" -rw=randread   --time_based=1 | tee -a "$log_file"
#################################################################################################################################################################################################################33



#################################################################################################################################################################################################################33
#bin/bash
figlet  "warmup"
fio -name warmup    -filename="$disk_b" --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime="$runtime" -rw=write     --time_based=1 | tee -a "$log_file"
figlet  "seqwrite"
fio -name seqwrite  -filename="$disk_b" --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime="$runtime" -rw=write     --time_based=1  | tee -a "$log_file"
figlet  "seqread"
fio -name seqread   -filename="$disk_b" --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime="$runtime" -rw=read      --time_based=1  | tee -a "$log_file"

figlet "randwrite"
fio -name randwrite -filename="$disk_b" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=10G -runtime="$runtime" -rw=randwrite --time_based=1  | tee -a "$log_file"
figlet "randread"
fio -name randread  -filename="$disk_b" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=10G -runtime="$runtime" -rw=randread  --time_based=1  | tee -a "$log_file"
figlet "latwrite"
fio -name latwrite  -filename="$disk_b" --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime="$runtime" -rw=randwrite  --time_based=1  | tee -a "$log_file"
figlet "latread"
fio -name latread   -filename="$disk_b" --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime="$runtime" -rw=randread   --time_based=1  | tee -a "$log_file"


figlet "latwritelb"
fio -name latwrite  -filename="$disk_b" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime="$runtime" -rw=randwrite  --time_based=1  | tee -a "$log_file"
figlet "latreadlb"
fio -name latread   -filename="$disk_b" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime="$runtime" -rw=randread   --time_based=1  | tee -a "$log_file"
# #bin/bash
# fio -name seqwrite  -filename="$disk_b" --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime=10 -rw=write     --time_based=1 | grep "write" | tee -a "$log_file"
# fio -name seqread   -filename="$disk_b" --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime=10 -rw=read      --time_based=1 | grep "read" | tee -a "$log_file"

# fio -name randwrite -filename="$disk_b" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=10G -runtime=10 -rw=randwrite --time_based=1 | grep "write" | tee -a "$log_file"
# fio -name randread  -filename="$disk_b" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=10G -runtime=10 -rw=randread  --time_based=1 | grep "read" | tee -a "$log_file"

# fio -name latwrite  -filename="$disk_b" --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime=10 -rw=randwrite  --time_based=1 | grepp "lat" | tee -a "$log_file"
# fio -name latread   -filename="$disk_b" --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime=10 -rw=randread   --time_based=1 | grep "lat" | tee -a "$log_file"
#################################################################################################################################################################################################################33
 
 
 #################################################################################################################################################################################################################33
 figlet  "warmup"
fio -name warmup    -filename="$disk_c" --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime="$runtime" -rw=write     --time_based=1 | tee -a "$log_file"
figlet  "seqwrite"
fio -name seqwrite  -filename="$disk_c" --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime="$runtime" -rw=write     --time_based=1  | tee -a "$log_file"
figlet  "seqread"
fio -name seqread   -filename="$disk_c" --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime="$runtime" -rw=read      --time_based=1  | tee -a "$log_file"

figlet "randwrite"
fio -name randwrite -filename="$disk_c" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime="$runtime" -rw=randwrite --time_based=1  | tee -a "$log_file"
figlet "randread"
fio -name randread  -filename="$disk_c" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime="$runtime" -rw=randread  --time_based=1  | tee -a "$log_file"

figlet "latwrite"
fio -name latwrite  -filename="$disk_c" --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime="$runtime" -rw=randwrite  --time_based=1  | tee -a "$log_file"
figlet "latread"
fio -name latread   -filename="$disk_c" --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime="$runtime" -rw=randread   --time_based=1  | tee -a "$log_file"
 
 figlet "latwritelb"
fio -name latwrite  -filename="$disk_c" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio   -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime="$runtime" -rw=randwrite  --time_based=1  | tee -a "$log_file"
figlet "latreadlb"
fio -name latread   -filename="$disk_c" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime="$runtime" -rw=randread   --time_based=1  | tee -a "$log_file"
 
 
```

​       

```
#!/bin/bash
cd   /etc/yum.repos.d
wget   http://smb.zstack.io/mirror/lei.zhang/h84ryumrepo/zstack-aliyun-yum.repo
sudo yum install -y fio
sudo yum clean  all
sudo yum makecache
sudo yum install unzip -y

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




# fio -name warmup -filename=/dev/vdb --numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime="$runtime" -rw=write --time_based=1 | tee -a "$log_file"
#################################################################################################################################################################################################################33
figlet  "warmup"
figlet  ""
fio -name warmup    -filename=/dev/vdb --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime=60 -rw=write     --time_based=1



figlet  "seqwrite"
fio -name seqwrite  -filename=/dev/vdb --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64  --size=50G -runtime=10 -rw=write     --time_based=1
figlet  "seqread"
fio -name seqread   -filename=/dev/vdb --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64  --size=50G -runtime=10 -rw=read      --time_based=1 


figlet "randwrite"
fio -name randwrite -filename=/dev/vdb --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64  --size=50G -runtime=10 -rw=randwrite --time_based=1 
figlet "randread"
fio -name randread  -filename=/dev/vdb --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64  --size=50G -runtime=10 -rw=randread  --time_based=1

figlet "latwrite"
fio -name latwrite  -filename=/dev/vdb --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1   --size=50G -runtime=10 -rw=randwrite  --time_based=1
figlet "latread"
fio -name latread   -filename=/dev/vdb --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1   --size=50G -runtime=10 -rw=randread   --time_based=1


figlet "latwritelb"
fio -name latwrite  -filename=/dev/vdb --numjobs=1 --allow_mounted_write=1 -ioengine=libaio    -direct=1 -group_reporting -bs=4k -iodepth=1   --size=50G -runtime=10 -rw=randwrite  --time_based=1
figlet "latreadlb"
fio -name latread   -filename=/dev/vdb --numjobs=1 --allow_mounted_write=1 -ioengine=libaio    -direct=1 -group_reporting -bs=4k -iodepth=1   --size=50G -runtime=10 -rw=randread   --time_based=1
#################################################################################################################################################################################################################33



#################################################################################################################################################################################################################33
#bin/bash
figlet  "warmup"
fio -name warmup    -filename=/dev/vdc --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime=100 -rw=write     --time_based=1
figlet  "seqwrite"
fio -name seqwrite  -filename=/dev/vdc --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime=10 -rw=write     --time_based=1 
figlet  "seqread"
fio -name seqread   -filename=/dev/vdc --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime=10 -rw=read      --time_based=1 

figlet "randwrite"
fio -name randwrite -filename=/dev/vdc --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=10G -runtime=10 -rw=randwrite --time_based=1 
figlet "randread"
fio -name randread  -filename=/dev/vdc --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=10G -runtime=10 -rw=randread  --time_based=1 

figlet "latwrite"
fio -name latwrite  -filename=/dev/vdc --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime=10 -rw=randwrite  --time_based=1 
figlet "latread"
fio -name latread   -filename=/dev/vdc --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime=10 -rw=randread   --time_based=1 


figlet "latwritelb"
fio -name latwrite  -filename=/dev/vdc --numjobs=1 --allow_mounted_write=1 -ioengine=libaio    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime=10 -rw=randwrite  --time_based=1 
figlet "latreadlb"
fio -name latread   -filename=/dev/vdc --numjobs=1 --allow_mounted_write=1 -ioengine=libaio    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime=10 -rw=randread   --time_based=1 
# #bin/bash
# fio -name seqwrite  -filename=/dev/vdc --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime=10 -rw=write     --time_based=1 | grep "write"
# fio -name seqread   -filename=/dev/vdc --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=10G -runtime=10 -rw=read      --time_based=1 | grep "read"

# fio -name randwrite -filename=/dev/vdc --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=10G -runtime=10 -rw=randwrite --time_based=1 | grep "write"
# fio -name randread  -filename=/dev/vdc --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=10G -runtime=10 -rw=randread  --time_based=1 | grep "read"

# fio -name latwrite  -filename=/dev/vdc --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime=10 -rw=randwrite  --time_based=1 | grepp "lat"
# fio -name latread   -filename=/dev/vdc --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=10G -runtime=10 -rw=randread   --time_based=1 | grep "lat"
#################################################################################################################################################################################################################33
 
 
 #################################################################################################################################################################################################################33
 figlet  "warmup"
fio -name warmup    -filename=/dev/vdd --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=100 -rw=write     --time_based=1
figlet  "seqwrite"
fio -name seqwrite  -filename=/dev/vdd --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=10 -rw=write     --time_based=1 
figlet  "seqread"
fio -name seqread   -filename=/dev/vdd --numjobs=1  --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=10 -rw=read      --time_based=1 

figlet "randwrite"
fio -name randwrite -filename=/dev/vdd --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime=10 -rw=randwrite --time_based=1 
figlet "randread"
fio -name randread  -filename=/dev/vdd --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime=10 -rw=randread  --time_based=1 

figlet "latwrite"
fio -name latwrite  -filename=/dev/vdd --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=10 -rw=randwrite  --time_based=1 
figlet "latread"
fio -name latread   -filename=/dev/vdd --numjobs=1 --allow_mounted_write=1 -ioengine=sync    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=10 -rw=randread   --time_based=1 
 
 figlet "latwritelb"
fio -name latwrite  -filename=/dev/vdd --numjobs=1 --allow_mounted_write=1 -ioengine=libaio   -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=10 -rw=randwrite  --time_based=1 
figlet "latreadlb"
fio -name latread   -filename=/dev/vdd --numjobs=1 --allow_mounted_write=1 -ioengine=libaio    -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=10 -rw=randread   --time_based=1 
 
 
 
 #################################################################################################################################################################################################################33
 
 
 
 
                     #vdb                                                          
# 顺序写入测试       491
# 顺序读出测试       537?vi
# 随机写入测试       1256
# 随机读取测试       2974
# 高延迟写入测试  clat percentiles (usec):
    #  |  1.00th=[  137],  5.00th=[  143], 10.00th=[  145], 20.00th=[  149],
    #  | 30.00th=[  153], 40.00th=[  157], 50.00th=[  161], 60.00th=[  167],
    #  | 70.00th=[  174], 80.00th=[  182], 90.00th=[  196], 95.00th=[  210],
    #  | 99.00th=[  273], 99.50th=[  306], 99.90th=[  857], 99.95th=[  988],
    #  | 99.99th=[ 7046]     clat (usec): min=123, max=25029, avg=170.51, stdev=180.91
# 高延迟读取测试     clat (usec): min=130, max=13336, avg=174.10, stdev=100.24
    #  |  1.00th=[  147],  5.00th=[  149], 10.00th=[  151], 20.00th=[  155],
    #  | 30.00th=[  157], 40.00th=[  159], 50.00th=[  161], 60.00th=[  165],
    #  | 70.00th=[  169], 80.00th=[  178], 90.00th=[  202], 95.00th=[  262],
    #  | 99.00th=[  310], 99.50th=[  322], 99.90th=[  816], 99.95th=[  898],
    #  | 99.99th=[ 1516]


#   sudo   yum  install    fio -y

# #关心的磁盘性能    
# #顺序读   顺序写     关心带宽      选取   numjobs 1   libaio   bs  1M    iodepth深度64    时间120s
# #小块随机读   随机写     关心iops    选取 numjobs 64   libaio   bs  4k   iodepth深度64    时间120s
# #小块随机    关心时延     numjobs  1       sync    bs  4k      iodepth深度1     时间120s

# #例子 name  bs   time             深度  块大小  dircert  numjobs
# # warm	1M	      120    write	    64  50G	     1	    1	libaio
# # seqwrite	1M	360s	   write	64	50G	     1	    1	libaio
# # seqread	1M	120s	    read	64	50G	     1	    1	libaio
# # randwrite	4k	360s	randwrite	64	50G	     1	    64	libaio
# # randread	4k	120s	randread	64	50G      1      64	libaio
# # latwrite	4k	360s	randwrite	1	50G	     1	    1	sync
# # latread	4k	120s	randread	1	50G	     1	    1	sync

# # 磁盘名字变量和日志文件路径
# disk_name="/dev/vdb"
# log_file="/var/log/fio_test.log"
# runtime="10"

# # 函数：记录日志
# log() {
#     echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$log_file"
# }

# # 函数：倒计时
# countdown() {
#     local seconds=$1
#     while [ $seconds -gt 0 ]; do
#         printf "%d 秒后开始...\r" $seconds
#         sleep 1
#         ((seconds--))
#     done
#     echo
# }

# # 确保日志文件存在
# mkdir -p "$(dirname "$log_file")"
# touch "$log_file"

# # 预热测试
# log "开始预热测试。预热测试时间为180秒。"
# echo '预热测试开始numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime=180 -rw=write --time_based=1'
# countdown 3 # 倒计时3秒准备
# fio -name warmup -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=128 --size=50G -runtime="$runtime" -rw=write --time_based=1 | tee -a "$log_file"
# log "预热测试完成。"
# echo '预热测试完成'
# sleep 30

# # 顺序写入测试

#     log "开始顺序写入测试，任务数为 $numjobs。"
#     echo "开始顺序写入测试，任务数为 $numjobs"
#     countdown 3
#     fio -name seqwrite -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=10 -rw=write --time_based=1 | tee -a "$log_file"
#     log "顺序写入测试完成，任务数为 $numjobs。"
#     sleep 30


# # 顺序读出测试
# log "开始顺序读出测试。"
# echo "开始顺序读出测试"
# countdown 3
# fio -name seqread -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=1M -iodepth=64 --size=50G -runtime=10 -rw=read --time_based=1 | tee -a "$log_file"
# log "顺序读出测试完成。"
# sleep 30

# # 随机写入测试
# log "开始随机写入测试。"
# echo "开始随机写入测试"
# countdown 3
# fio -name randwrite -filename="$disk_name" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime=10 -rw=randwrite --time_based=1 | tee -a "$log_file"
# log "随机写入测试完成。"
# sleep 30

# # 随机读取测试
# log "开始随机读取测试。"
# echo "开始随机读取测试"
# countdown 3
# fio -name randread -filename="$disk_name" --numjobs=64 --allow_mounted_write=1 -ioengine=libaio -direct=1 -group_reporting -bs=4k -iodepth=64 --size=50G -runtime=10 -rw=randread --time_based=1 | tee -a "$log_file"
# log "随机读取测试完成。"
# sleep 30

# # 高延迟写入测试
# log "开始高延迟写入测试。"
# echo "开始高延迟写入测试"
# countdown 3
# fio -name latwrite -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=sync -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=10 -rw=randwrite --time_based=1 | tee -a "$log_file"
# log "高延迟写入测试完成。"
# sleep 30

# # 高延迟读取测试
# log "开始高延迟读取测试。"
# echo "开始高延迟读取测试"
# countdown 3
# fio -name latread -filename="$disk_name" --numjobs=1 --allow_mounted_write=1 -ioengine=sync -direct=1 -group_reporting -bs=4k -iodepth=1 --size=50G -runtime=10 -rw=randread --time_based=1 | tee -a "$log_file"
# log "高延迟读取测试完成。"
# sleep 30

# log "所有测试已完成。日志已保存在 $log_file。"
# echo '所有测试已完成，日志已保存在 $log_file'
```

待完善
