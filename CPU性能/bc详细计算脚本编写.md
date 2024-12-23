# bc详细使用   计算脚本编写

> 参考考
>
> https://www.gnu.org/software/bc/manual/html_mono/bc.html
>
> https://cloud.tencent.com/developer/article/1544376

## 特殊变量

```
scale	定义某些操作如何使用小数点后的数字，默认值为 0
ibase	定义输入数的基数，默认为十进制数
obase	定义输出数的基数，默认为十进制数
last	表示最后的输出值
```

## 注释

块注释使用`/* */`，行注释使用 #

## 表达式

表达式的输入值可以是 2 到 16 进制的数值，数值的基数由特殊变量 ibase 决定。如果数值中包含字符 A-F，则必须使用大写，因为小写表示变量名。

在下面表达式的描述中，EXPR 指完整表达式，VAR 指简单变量或数组变量。简单变量只是一个名称，数组变量被指定为 NAME[EXPR]。

除非特别提到，结果的精度是表达式中最大的精度。

```
基本运算：
- EXPR
	相反数
++ VAR
	自增 1
-- VAR
	自减 1
VAR ++
	表达式的结果是变量的值，然后变量自增 1
VAR --
	表达式的结果是变量的值，然后变量自增 1
EXPR + EXPR
	两个表达式相加
EXPR - EXPR
	两个表达式相减
EXPR * EXPR
	两个表达式相乘
EXPR / EXPR
	两个表达式相除。结果的精度由特殊变量 scale 确定
EXPR % EXPR
	两个表达式取余
EXPR ^ EXPR
	取幂。第二个表达式 EXPR 必须是整数
( EXPR )
	这将更改标准优先级以强制执行表达式的计算
VAR = EXPR
	将表达式的结果赋给变量 VAR
VAR <OP>= EXPR
	这相当于 var = var EXPR

关系运算：
EXPR1 < EXPR2
EXPR1 <= EXPR2
EXPR1 > EXPR2
EXPR1 >= EXPR2
EXPR1 == EXPR2
EXPR1 != EXPR2

逻辑运算：
!EXPR
EXPR && EXPR
EXPR || EXPR
```

以上表达式涉及的运算符优先级由低到高依次为：

```javascript
||			左结合
&&			左结合
!			非结合的
关系运算符	左结合
赋值运算符	由结合
+, -		左结合
*, /, %		左结合
^			右结合
取反运算符	非结合的
++, --		非结合的
```

以上运算符优先级与 C 语言有些出入，使用时需要注意。比如表达式 a = 3 < 5 在 C 语言中 a 的值为 0，在 bc 中，因为 = 的优先级高于 <，所以 a 的值为 3。

bc 中提供了一些特殊的表达式，这些与用户定义的函数和标准函数有关，下文函数一节将会详述。



## 语句

bc 的语句使用分号和换行符进行分隔，下面将介绍 bc 中常用的语句。注意，中括号 [] 中的内容是可选的。

```javascript
EXPRESSION
	表达式分为赋值表达式与非赋值表达式，如果表达式不是赋值语句，则计算表达式并将其结果打印到输出
STRING
	使用双引号包围的内容被视为字符串。字符串可以包含特殊字符，使用反斜杠表示，\a 响铃，\b 退格，\f 换页，\n 换行，\r 回车，\q 双引号，\t 制表符，\\ 反斜杠
print LIST
	使用 print 语句进行输出。LIST 是逗号分隔的字符串或者表达式
{ STATEMENT_LIST }
	这是个复合语句，它允许将多个语句组合在一起执行
if ( EXPRESSION ) STATEMENT1 [else STATEMENT2]
	if 条件语句。如果表达式 EXPRESSION 结果非 0，则执行语句 STATEMENT1，否则执行 STATEMENT2
while ( EXPRESSION ) STATEMENT
	while 循环语句。如果表达式 EXPRESSION 结果非 0，则循环执行语句
for ( [EXPRESSION1] ; [EXPRESSION2] ; [EXPRESSION3] ) STATEMENT
	for 循环语句
break
	用于退出最近一层的 while 或 for 循环
continue
	用于最近一层的 while 或 for 循环提前进入下一轮循环
halt
	结束 bc
return
	从函数中返回 0
return ( EXPRESSION )
	从函数返回表达式 EXPRESSION 的值
limits
	打印 bc 的限制
quit
	结束 bc
warranty
	打印授权注意事项
```

## 8.函数

bc 支持函数，定义形式如下：



```javascript
define [void] NAME ( PARAMETERS ) {
	AUTO_LIST   STATEMENT_LIST }
```

其中 关键字 void 表示函数无返回值，NAME 为函数名，PARAMETERS 为函数参数，AUTO_LIST 为函数内部使用 auto 关键字申明的局部变量，STATEMENT_LIST 为函数 bc 语句。

函数调用形式：

```javascript
NAME(PARAMETERS)
```

常用的内置函数有：

```javascript
length ( EXPRESSION )
	数值的有效数字的个数
read ()
	从标准输入读取输入
scale ( EXPRESSION )
	数值小数点后的数字的个数
sqrt ( EXPRESSION )
	求平方根。如果 EXPRESSION 是一个负数，则引发运行时错误
```

如果使用 -l 选项调用 bc，则会预加载一个数学库，并将默认精度设置为 20。数学库定义了以下函数：

```javascript
s (x)
	求正弦值 sin(x)，x 的单位是弧度
c (x)
	求余弦值 cos()，x 的单位是弧度
a (x)
	x 的反正切，反正切返回弧度
l (x)
	x 的自然对数
e (x)
	指数函数，求自然 e 的 x 次幂
j (n,x)
	x 的整数阶 n 的贝塞尔函数
```

