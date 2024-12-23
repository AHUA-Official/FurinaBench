mark  furina

上面那个文档 我有画那个性能的每个CPU的图 这个图是这个样子画的

1. 拿到mpstat的监控数据

```
#!/bin/bash

# 文件名
logfile="moho.txt"

# 检查文件是否存在
if [ -f "$logfile" ]; then
    # 删除文件
    rm -f "$logfile"
fi

# 运行 mostat 命令并将输出重定向到文件和终端
mpstat -P ALL 3 | tee "$logfile"
```

在跑Unixbench的时候 我们就开一个新终端 跑这个 Unixbench跑完了  掐掉 同路径下对应的logfile我们要这个



拿到之后 把他下到电脑

用pycharm创建一个jupterNote book的环境 

然后把可视化的脚本贴进去

这个里面就那个sample.ipynb的脚本有用  其他的没啥用

里面的函数作用

```
filter_mpstat_data    清洗日志  存到另外一个洗了之后的文件
parse_mpstat_data       存成字典列表   把洗了之后的文件数据变成一个字典
plot_cpu_idle_usage     画图     拿这个字典列表进行有选择的画图  可以传mpstat显示的CPU使用参数进去画对应的图


依赖
matplotlib  
```