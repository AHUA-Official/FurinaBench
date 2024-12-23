# 使用bc计算pi  校验单核计算能力



### bc介绍   

bc是一个用于进行数学计算的命令行工具。它主要用于执行高精度运算和复杂的数学表达式。  

使用bc可以在bash或者shell环境下快速进行复杂的科学计算 

#### 安装bc   

大部分OS  可以直接使用包管理工具安装bc  ，  因为bc是GNU下的开源软件   大部分的源都会包含gnu下面的著名项目的

```shell
yum  install   bc 
apt  install   bc 
```

不过如果你想要获得源码的话   在如下网址

> [https://www.gnu.org/software/bc/](https://www.gnu.org/software/bc/)

> [https://ftp.gnu.org/gnu/bc/bc-1.07.tar.gz](https://ftp.gnu.org/gnu/bc/bc-1.07.tar.gz)

源码编译安装步骤如下

```
#可能需要处理的依赖问题
apt install   build-essential   libreadline-dev
# build-essential   编译工具链
# libreadline-dev     Readline 库 用于支持交互式命令行输入功能
apt  install    texinfo
# textinfo 用于生成文档的工具支持，特别是 .info 文件

#获取源码
 wget https://ftp.gnu.org/gnu/bc/bc-1.07.1.tar.gz
 tar -zxvf   bc-1.07.1.tar.gz 
 cd bc-1.07.1   
 
 #编译安装
 ./configure
 make
 make install
 
 #使用示例
 cd  bc 
 ./bc   -v
 echo "10.13*10.13" | ./bc 
 time echo "scale=500; 4*a(1)" | ./bc -l -q
```

#### bc使用

使用语法

```
#详细使用见  https://www.gnu.org/software/bc/manual/html_mono/bc.html官方文档说明明
bc  <选项>   <参数>
```

选项说明

```
-h  --help         print this usage and exit    帮助信息
-i  --interactive  force interactive mode       强制进入交互模式
-l  --mathlib      use the predefined math routines  预加载标准数学库 （用了才可以用a1（） sqrt()等函数）
-q  --quiet        don't print initial banner        不打印正常的GNU环境信息
-s  --standard     non-standard bc constructs are errors      不支持标准的POSIX bc描述以外的扩展
-w  --warn         warn about non-standard bc constructs      对POSIX bc的扩展给出警告信息
-v  --version      print version information and exit        版本信息
```

参数说明

```
文件：指定包含计算任务的文件。（写入了bc可以看懂的计算任务的文本文件）
```

举个例子（标准用法）

![image-20241223105242608](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/image-20241223105242608.png)

举个例子（常见用法）

```
#使用管道符  可以直接调bc  使用 -l -q 可以直接不进bc的交互环境   写远程脚本的时候这样干我喜欢
echo "10^10" | bc
abc=11000000
echo "obase=10;ibase=2;$abc" | bc
```



### 方法流程

想要使用bc计算pi的话   容易想到的办法是  反正切函数  arctan(1)=pi/4   那么使用bc  容易想到 

```
echo "scale=5000; 4*a(1)" | bc -l -q
# scale 指定小数点后位数   如图  计算小数点后5000位的pi  使用bc
```

需要获得bc计算的时间来评估计算性能

```
time   echo "scale=5000; 4*a(1)" | bc -l -q 
echo "`time (echo "scale=50; 4*a(1)" | taskset -c 1 -l -q) 2>&1 | grep 'real\|user\|sys'`"
echo "$(time (echo "scale=50; 4*a(1)" | taskset -c 1 -l -q) 2>&1 | grep 'real\|user\|sys')"
# 结果
# real      0m44.33s      实际时间
# user      0m44.31s      用户空间时间
# sys       0m0.02s       syscall时间
```

关于计算性能  我们主要关注单核计算性能的benchmark（多核的计算性能不是很稳定） 

```
time   echo "scale=5000; 4*a(1)" |  taskset -c 1 bc -l -q 
#taskset  绑核   
root@iZ2vcdgpo69rod4d4wovilZ:~# taskset -h
Usage: taskset [options] [mask | cpu-list] [pid|cmd [args...]]


Show or change the CPU affinity of a process.

Options:
 -a, --all-tasks         operate on all the tasks (threads) for a given pid
 -p, --pid               operate on existing given pid
 -c, --cpu-list          display and specify cpus in list format
 -h, --help              display this help
 -V, --version           display version

The default behavior is to run a new command:
    taskset 03 sshd -b 1024
You can retrieve the mask of an existing task:
    taskset -p 700
Or set it:
    taskset -p 03 700
List format uses a comma-separated list instead of a mask:
    taskset -pc 0,3,7-11 700
Ranges in list format can take a stride argument:
    e.g. 0-31:2 is equivalent to mask 0x55555555

For more details see taskset(1).

```

想要run一下CPU的每一个核

```
#!/bin/bash
#@author lei.zhang
# 定义 bits 变量，表示计算 π 的小数位数
bits=50
# 获取 CPU 核心数
cpu_c=$(cat /proc/cpuinfo | grep -c ^processor)
# 检查是否成功获取 CPU 核心数
if [ "$cpu_c" -eq 0 ]; then
    echo "Error: Could not determine the number of CPU cores."
    exit 1
fi

# 计算需要运行的 CPU num序号最大值
cpu_num=$((cpu_c - 1))

# 遍历每个 CPU 核心，使
for cpu_seq in $(seq 0 $cpu_num); do
    echo "Running on CPU $cpu_seq..."
    
    # 使用 time 计算时间，并将输出重定向到文件
    # 2>&1   标准错误（stderr）的内容合并到标准输出（stdout）
    #标准（std）文件描述符。每个进程都有三个默认的文件描述符：
	#0：标准输入（stdin）
	#1：标准输出（stdout）
	#2：标准错误（stderr）
	#&1  标识1是一个标准文件描述符
	#grep 'real\|user\|sys'  
	#文件正则表达式   \|：这是正则表达式中的“或”操作符，表示匹配 real、user 或 sys 中的任意一个
	echo "$(time (echo "scale=50; 4*a(1)" | taskset -c 1 -l -q) 2>&1 | grep 'real\|user\|sys')"
	
	
    

    
done
```

如果你想要run多次

```
for i in $(seq 1 20); do (bash d.sh); done
for i in $(seq 1 20); do (bash d.sh | tee -a results.txt); done | tee  -a a.txt
```

> 不知道为啥   我tee不进去 我好难受 
>
> 





评估

在使用cpu绑定   并设定适当的位数的时候   该方法可以跑满cpu （全运行流程跑mpstat进行监控）  且多次运行的结果相对稳定    在使用我的云主机 和旧电脑在Debian系列发行版上跑    对比还是挺明显的    不过  使用bc做benchmark 不是一个标准方法   没有任何厂商或者专家给我背书   

所以这个玩意只能做实验性的测试    检测计算能力， 不能进到正式的benchmark报告书里面去