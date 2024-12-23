# NTP介绍

未完成 mark  furina









#### ntp同步脚本示例

```
#!/bin/bash
  yum install -y sshpass
# 设置远程服务器的IP地址
SERVER1="172.0.0.1"
SERVER2="192.168.1.1"

# 设置SSH登录信息
SSH_USER="root"
SSH_PASS="password" # 请替换为您的密码

# 设置NTP服务器
NTP_SERVER="time.google.com"

# 使用sshpass和SSH配置NTP服务并同步时间的函数
configure_ntp() {
    local server_ip=$1

    # 使用sshpass通过SSH登录到服务器并执行命令
    sshpass -p "$SSH_PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 $SSH_USER@$server_ip << EOF
        # 安装NTP服务（如果尚未安装）
        yum install -y ntp

        # 配置NTP服务器
        echo "server $NTP_SERVER iburst" >> /etc/ntp.conf

        # 重启NTP服务以应用配置
        systemctl restart ntpd

        # 强制立即同步时间
        ntpd -gq
EOF
}

# 配置两个服务器的NTP服务并同步时间
configure_ntp $SERVER1
configure_ntp $SERVER2

echo "NTP配置和时间同步完成。"
```

