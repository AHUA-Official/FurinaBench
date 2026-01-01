# BPF 简介

BPF（Berkeley Packet Filter / eBPF，扩展的伯克利包过滤器）是 Linux 内核中的一个强大技术，允许在内核空间中安全、高效地运行用户定义的代码，用于系统跟踪、性能分析和网络监控。

## 主要功能

BPF 可以用于系统的多个方面：

- **系统跟踪**：跟踪系统调用、函数调用、内核事件等
- **性能分析**：分析 CPU、内存、I/O 等性能瓶颈
- **网络监控**：监控网络流量、数据包过滤、QoS 控制
- **安全监控**：检测异常行为、访问控制、审计日志
- **动态插桩**：在不修改代码的情况下动态注入监控代码
- **实时监控**：实时收集和分析系统行为数据

## 特点

- **内核集成**：直接在内核空间中运行，性能开销极低
- **安全可靠**：通过验证器确保代码安全性，不会导致内核崩溃
- **高性能**：采用 JIT 编译，执行效率接近原生代码
- **灵活性高**：支持多种编程语言，可以编写复杂的逻辑
- **低开销**：相比传统工具，对系统性能影响很小
- **功能强大**：可以访问内核数据结构和函数

## 常用工具

```bash
# BCC（BPF Compiler Collection）- 常用的 BPF 工具集
# 监控系统调用
sudo opensnoop

# 监控文件 I/O
sudo filetop
sudo fileslower

# CPU 性能分析
sudo execsnoop
sudo runqlat

# 网络监控
sudo tcplife
sudo tcptop

# bpftrace - 高级跟踪语言
# 跟踪系统调用
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_open { printf("%s %s\n", comm, str(args->filename)); }'

# 跟踪 CPU 使用
sudo bpftrace -e 'profile:hz:99 { @[ustack] = count(); }'

# 使用 perf 工具
perf trace
perf record -e 'sched:*' -a
```

## 相关项目

- **BCC**：BPF 编译器集合，提供 Python/Lua 接口
- **bpftrace**：高级跟踪语言，类似 DTrace
- **libbpf**：BPF 库，用于编写 BPF 程序
- **Falco**：基于 BPF 的运行时安全监控工具
- **Cilium**：基于 BPF 的网络和安全项目

