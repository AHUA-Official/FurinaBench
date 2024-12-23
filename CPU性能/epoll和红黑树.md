# IO多路复用

## epoll模型

开发高性能网络程序时，windows开发者们言必称Iocp，linux开发者们则言必称Epoll。大家都明白Epoll是一种IO多路复用技术，可以非常高效的处理数以百万计的Socket句柄，比起以前的Select和Poll效率提高了很多。

## epoll接口

三个接口，epoll_create创建句柄，epoll_ctl事件注册，epoll_wait等待事件

### epoll_create

`int epoll_create(int size)` size告诉内核监听的数目，注意创建句柄后，可以在`/proc/进程ID/fd/`下看到，使用结束后，记得调用`close()`关闭

### epoll_ctl

```
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event)
```

`epfd`：epoll_create返回的epollfd值

`op`：表示操作类型，有三个

- EPOLL_CTL_ADD: 注册新fd到epfd
- EPOLL_CTL_MOD:修改epfd中的fd
- EPOLL_CTL_DEL:删除epfd中的fd

`fd`：代表被监听的fd

`epoll_event`: 被监听的事件

epoll_event 结构如下:

```c
typedef union epoll_data {
    void *ptr;
    int fd;
    __uint32_t u32;
    __uint64_t u64;
} epoll_data_t;

struct epoll_event {
    __uint32_t events; /* Epoll events */
    epoll_data_t data; /* User data variable */
};
```

其中`__uint32_t events`选项有

- EPOLLIN ：表示对应的文件描述符可以读（包括对端SOCKET正常关闭）；
- EPOLLOUT：表示对应的文件描述符可以写；
- EPOLLPRI：表示对应的文件描述符有紧急的数据可读（这里应该表示有带外数据到来）；
- EPOLLERR：表示对应的文件描述符发生错误；
- EPOLLHUP：表示对应的文件描述符被挂断；
- EPOLLET： 将EPOLL设为边缘触发(Edge Triggered)模式，这是相对于水平触发(Level Triggered)来说的。
- EPOLLONESHOT：只监听一次事件，当监听完这次事件之后，如果还需要继续监听这个socket的话，需要再次把这个socket加入到EPOLL队列里

## epoll_wait

## 例子

```c
#define MAX_EVENTS 10
struct epoll_event ev, events[MAX_EVENTS];
int listen_sock, conn_sock, nfds, epollfd;

/* Code to set up listening socket, 'listen_sock',
              (socket(), bind(), listen()) omitted */

epollfd = epoll_create1(0);
if (epollfd == -1) {
    perror("epoll_create1");
    exit(EXIT_FAILURE);
}

ev.events = EPOLLIN;
ev.data.fd = listen_sock;
if (epoll_ctl(epollfd, EPOLL_CTL_ADD, listen_sock, &ev) == -1) {
    perror("epoll_ctl: listen_sock");
    exit(EXIT_FAILURE);
}

for (;;) {
    nfds = epoll_wait(epollfd, events, MAX_EVENTS, -1);
    if (nfds == -1) {
        perror("epoll_wait");
        exit(EXIT_FAILURE);
    }

    for (n = 0; n < nfds; ++n) {
        if (events[n].data.fd == listen_sock) {
            conn_sock = accept(listen_sock,
                               (struct sockaddr *) &addr, &addrlen);
            if (conn_sock == -1) {
                perror("accept");
                exit(EXIT_FAILURE);
            }
            setnonblocking(conn_sock);
            ev.events = EPOLLIN | EPOLLET;
            ev.data.fd = conn_sock;
            if (epoll_ctl(epollfd, EPOLL_CTL_ADD, conn_sock,
                          &ev) == -1) {
                perror("epoll_ctl: conn_sock");
                exit(EXIT_FAILURE);
            }
        } else {
            do_use_fd(events[n].data.fd);
        }
    }
}
```

| IO多路复用 | select                         | poll                           | epoll                                         |
| ---------- | ------------------------------ | ------------------------------ | --------------------------------------------- |
| 操作方式   | 遍历                           | 遍历                           | 回调                                          |
| 句柄管理   | 数组                           | 链表                           | 红黑树                                        |
| IO效率     | 线性遍历O(n)                   | 线性遍历O(n)                   | 同志回调O(1)                                  |
| 最大连接数 | 32位系统1024,64位系统2048      | 无上限，系统最大打开文件数     | 无上限，系统最大打开文件数                    |
| 陷入       | 每次都需要将sockfd拷贝到内核态 | 每次都需要将sockfd拷贝到内核态 | 调用epoll_ctl拷贝到内核，每次epoll_wait不拷贝 |

# 树的妙用

## 红黑树RBTree

### 使用场景

主要用在频繁增删改查的场景，个人觉得都是内存中的增删改查(内查找)，与IO相关的(外查找)应该用B族树

1. IO多路复用epoll中使用红黑树管理sockfd(socket文件句柄)
2. ngnix中用用红黑树管理timer(定时器)
3. CFS(Completely Fair Scheduler)，负责进程排程
4. STL的map和set的内部实现就是红黑树

## B-树：

多路搜索树，每个结点存储M/2到M个关键字，非叶子结点存储指向关键

字范围的子结点；

所有关键字在整颗树中出现，且只出现一次，非叶子结点可以命中；

![img](http://smb.zstack.io/mirror/performancedoc/performancemanualpic/23/22140175193189175972317246521515822912582_gopic_2141762376114554206137923422614811394125_1318434-20210428210558933-1291524231.png)

![btree.png](http://smb.zstack.io/mirror/performancedoc/performancemanualpic/23/117122321196012914111113267220176531116524_gopic_117122321196012914111113267220176531116524_191222245116132197115808129763111525192161_bfdef57484c5735008814c1f73fb5ca1.png)

## B+树：

在B-树基础上，为叶子结点增加链表指针，所有关键字都在叶子结点

中出现，非叶子结点作为叶子结点的索引；B+树总是到叶子结点才命中；

![img](http://smb.zstack.io/mirror/performancedoc/performancemanualpic/23/132212220892257150237173178243951631354882_gopic_59901463272292181885519349261462135321_1318434-20210428210627737-1900531640.png)

![img](http://smb.zstack.io/mirror/performancedoc/performancemanualpic/23/1108423083163224421381112532506031195243138_gopic_6510627232441881448521985690576311044_60b8fc23503492a4740249b9d93e4c9c.jpg)

## B*树：

在B+树基础上，为非叶子结点也增加链表指针，将结点的最低利用率

从1/2提高到2/3；

| 树   | AVL  | RB   | B/B- | B+   | B*   | Trie |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
|      |      |      |      |      |      |      |
|      |      |      |      |      |      |      |