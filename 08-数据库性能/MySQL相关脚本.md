需求  hammerdb测试  我看到华为云的一个数据库产品里面用hammerdb测试 特意说 构建的数据集大于内存大小   按道理来说  人都这样特意注明了  那肯定有人家的道理的 

## 方法1  全部数据库合在一起的大小

```
mysql> use information_schema;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> select concat(round(sum(data_length/1024/1024),2),'MB') as data from tables;
+----------+
| data     |
+----------+
| 935.25MB |
+----------+
1 row in set (1.18 sec)

mysql>exit



mysql -uroot -p'Furina@1013' -e "USE information_schema; SELECT CONCAT(ROUND(SUM(data_length/1024/1024),2),'MB') AS data FROM tables;"
```



## 法二  每一个数据库的大小

mysql -uroot -p'Furina@1013' -e "SELECT table_schema 'Database', CONCAT(ROUND(SUM(data_length)/1024/1024, 2),  'MB') AS 'Data Size' FROM information_schema.tables GROUP BY  table_schema;"



```
mysql -uroot -p'Furina@1013' -e "SELECT table_schema 'Database', CONCAT(ROUND(SUM(data_length)/1024/1024, 2), 'MB') AS 'Data Size' FROM information_schema.tables GROUP BY table_schema;"


[root@172-25-133-132 ~]# mysql -uroot -p'Furina@1013' -e "SELECT table_schema 'Database', CONCAT(ROUND(SUM(data_length)/1024/1024, 2), 'MB') AS 'Data Size' FROM information_schema.tables GROUP BY table_schema;"
mysql: [Warning] Using a password on the command line interface can be insecure.
+--------------------+-----------+
| Database           | Data Size |
+--------------------+-----------+
| information_schema | 0.00MB    |
| mysql              | 2.28MB    |
| performance_schema | 0.00MB    |
| sys                | 0.02MB    |
| tpcc               | 8228.83MB |
+--------------------+-----------+
[root@172-25-133-132 ~]#
```

# 数据库先验配置   MySQL80卸载重装重置密码远程登录                                            

​                                                                            Created by  张磊 on 八月 15, 2024                        

操作   

http://smb.zstack.io/mirror/lei.zhang/HammerDBEtc/DeleteMySQL.sh

http://smb.zstack.io/mirror/lei.zhang/HammerDBEtc/InstallMySQL80.sh