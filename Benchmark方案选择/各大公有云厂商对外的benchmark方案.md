# 各大云厂商的Benchmark方案 

> 摘要    调研了 火山  腾讯  阿里   华为   腾讯对外公布的benchmark方案 （部分） 



## 火山引擎

![177274455](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/177274455.png)

#### 文档评价 

https://www.volcengine.com/docs/6396/105001

https://www.volcengine.com/docs/6396/69496

https://www.volcengine.com/docs/6396/192731

https://www.volcengine.com/docs/6396/69496

如上 可以自己去读一下 

我个人理解的话  字节的文档写的还挺好的  主要是比较新 所以基本没啥错 而且人的文档很体系化 

虽然我自己没有怎么用过字节 他好像没啥学生优惠    

但是这个文档质量我还比较认可

 比阿里云的好  阿里云的那个性能测试文档是201几年的了  太老了  

唉  可惜我面字节一面的时候写不出算法   挂掉了   后面也没有消息   

唉  我爱字节    字节爱我吗？

## 腾讯云

嗯 腾讯云没有提供 ALL IN ONE的性能测试方案   他的测试方法几乎都是分开的  

所以我只能东找找西找找了      不过我给腾讯云提了issue之后   人家就回复我说会加上   而且还给我了100块钱京东卡  和100块腾讯云的卷     唉   腾讯云太好了    我个人给腾讯云中国最好的公有云的称号   如果我可以进腾讯云的话就好了

如下是我搜到的他们的测试方案  

或许等腾讯云做好了之后  我会更新一把



#### CPU

#### 内存

#### 文件

https://cloud.tencent.com/document/product/582/105654

使用的是fio

![img](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/177274485.png)

https://cloud.tencent.com/document/product/436/47974



![img](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/177274500.png)









#### 网络



netperf   iperf

sar    ethtppl

![img](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/177274488.png)

![img](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/177274491.png)





#### 数据库

sysbench

https://cloud.tencent.com/document/product/236/68810



![img](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/177274492.png)

![img](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/177274495.png)

![img](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/177274503.png)

![img](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/177274504.png)

![img](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/177274505-1734929021326-4.png)

## 京东云

他们在服务器的产品文档里面倒是提供了 一个性能测试的实践  很新 基本复制粘贴过来可以直接用   但是问题是 在这个里面只提供了

CPU测试的UnixBench  SUPER PI 

内存测试的  Stream  MLC 

如何评价京东云呢    love~

还有一些其他的一些杂七杂八的

路径如下

![image-20241223124949945](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/image-20241223124949945.png)

![image-20241223125103843](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/image-20241223125103843.png)

![image-20241223125128803](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/image-20241223125128803.png)

![image-20241223125148645](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/image-20241223125148645.png)

## 华为云

![image-20241223125237062](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/image-20241223125237062.png)

## 阿里云

![image-20241223125337642](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/image-20241223125337642.png)

![image-20241223125409339](https://raw.githubusercontent.com/AHUA-Official/TAEveryday/main/assets/image-20241223125409339.png)