前提 使用过apt的tools部署脚本 部署过apt tools



​       

```
#bin   bash

cd  /zapt
cd   apt_tools
cd ebizzy-0.3
ll 

# 定义一个计数器

count=0


# 循环10次

while [ $count -lt 10 ]; do

    # 执行ebizzy并只取第一行输出（每秒处理的记录数）

    output=$(./ebizzy | head -n 1)

    echo "Test $((count+1)): $output"

    # 计数器加1

    ((count++))

done
```