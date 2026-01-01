在linux内核中会有许多小对象，这些对象构造销毁十分频繁，比如i-node，dentry。这么这些对象如果每次构建的时候就向内存要一个页，而其实际大小可能只有几个字节，这样就非常浪费，为了解决这个问题就引入了一种新的机制来处理在同一页框中如何分配小存储器区。这就是我们要讨论的slab层。在linux中内存都是以页为单位来进行管理的(通常为4KB)，当内核需要内存就调用如：kmem_getpages这样的接口(底层调用__alloc_pages())。那么内核是如何管理页的分配的，这里linux使用了伙伴算法。slab也是向内核申请一个个页，然后再对这些页框做管理来达到分配小存储区的目的的。

## slab及其作用

slab是一种内存分配器，通过将内存划分不同大小的空间分配给对象来使用来进行缓存管理，应用于内核对象的缓存。

slab有两个主要作用：

1. slab小对象分配，不用为每一个小对象分配一个页，节省空间；
2. 内核中小对象的构建析构很频繁，slab对这些小对象做缓存，可以重复利用，减少内存分配次数；

`cat /proc/meminfo`命令输出的内存情况中有一项是slabinfo，也可以通过`cat /proc/slabinfo`和`slabtop`命令来查看详细的slabinfo。

```textile
# cat /proc/meminfo 
...
Slab:             347768 kB  # slab总量
SReclaimable:     110448 kB  # 可回收slab量
...
```

![slabtop结果示例](http://smb.zstack.io/mirror/performancedoc/performancemanualpic/23/2522120514312914804415241179925515150182_gopic_Snipaste_2022-09-01_17-56-21.png)

## /proc/slabinfo文件信息

在slab中，可分配内存块成为对象，每种对象占用的内存总量=num_objs*objsize。

```textile
# cat /proc/slabinfo
slabinfo - version: 2.1
# name            <active_objs> <num_objs> <objsize> <objperslab> <pagesperslab> : tunables <limit> <batchcount> <sharedfactor> : slabdata <active_slabs> <num_slabs> <sharedavail>
nf_conntrack_ffff9990dcb49480      0      0    320   51    4 : tunables    0    0    0 : slabdata      0      0      0
nf_conntrack_ffff9990db67a900    969    969    320   51    4 : tunables    0    0    0 : slabdata     19     19      0
nf_conntrack_ffff9990db678000   2499   2499    320   51    4 : tunables    0    0    0 : slabdata     49     49      0
nf_conntrack_ffffffffbf311ac0   3060   3060    320   51    4 : tunables    0    0    0 : slabdata     60     60      0
rpc_inode_cache       51     51    640   51    8 : tunables    0    0    0 : slabdata      1      1      0
fat_inode_cache       90     90    720   45    8 : tunables    0    0    0 : slabdata      2      2      0
fat_cache            102    102     40  102    1 : tunables    0    0    0 : slabdata      1      1      0
kvm_vcpu             104    106  15552    2    8 : tunables    0    0    0 : slabdata     53     53      0
xfs_dqtrx              0      0    528   62    8 : tunables    0    0    0 : slabdata      0      0      0
xfs_dquot              0      0    488   67    8 : tunables    0    0    0 : slabdata      0      0      0
xfs_ili             9072   9072    168   48    2 : tunables    0    0    0 : slabdata    189    189      0
xfs_inode          22916  22916    960   34    8 : tunables    0    0    0 : slabdata    674    674      0
xfs_efd_item        4056   4524    416   39    4 : tunables    0    0    0 : slabdata    116    116      0
xfs_log_ticket      3168   3168    184   44    2 : tunables    0    0    0 : slabdata     72     72      0
bio-3               8313   8313    320   51    4 : tunables    0    0    0 : slabdata    163    163      0
kcopyd_job             0      0   3312    9    8 : tunables    0    0    0 : slabdata      0      0      0
dm_uevent              0      0   2608   12    8 : tunables    0    0    0 : slabdata      0      0      0
dm_rq_target_io     4680   4680    136   60    2 : tunables    0    0    0 : slabdata     78     78      0
ip6_dst_cache       5040   5040    448   36    4 : tunables    0    0    0 : slabdata    140    140      0
# 统计slab占用超过10M的对象
cat /proc/slabinfo |awk '{if($3*$4/1024/1024 > 10){print $1,$3*$4/1024/1024} }'
```

待完善
