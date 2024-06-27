# pyclient
A customized python-mysql client support execute query multiple times

## install
依赖 python3 和 pymysql 库，请先安装 python3 及 pymysql 库。

```
pip3 install pymysql
```

## usage
命令行参数格式和 mysql 客户端参数类似。

> python3 pyclient.py  -h127.1 -P19519 -u admin@mysql -padmin -Dtest


```
usage: pyclient.py -h HOST -P PORT -u USER -p PASSWORD -D DATABASE [-f FILE] [--help]

在 MySQL 数据库上执行 SQL 语句。

optional arguments:
  -h HOST, --host HOST  MySQL 服务器的主机名或IP地址。
  -P PORT, --port PORT  MySQL 服务器的端口号。
  -u USER, --user USER  连接 MySQL 数据库的用户名。
  -p PASSWORD, --password PASSWORD
                        连接 MySQL 数据库的密码。
  -D DATABASE, --database DATABASE
                        要在其中执行 SQL 语句的数据库名称。
  -f FILE, --file FILE  要执行的 SQL 脚本路径。
  --help                显示此帮助信息并退出。
```



例如：

```
[pyclient] (main) $python3 pyclient.py  -h11.158.31.1 -P19519 -u admin@mysql -padmin -Dtest
正在执行 SQL 语句 1 次： DROP TABLE IF EXISTS text_table;
执行 1 次耗时： 0.113 秒
正在执行 SQL 语句 1 次： DROP TABLE IF EXISTS col_text_table;
执行 1 次耗时： 0.081 秒
正在执行 SQL 语句 1 次： DROP TABLE IF EXISTS varchar_table;
执行 1 次耗时： 0.071 秒
正在执行 SQL 语句 1 次： DROP TABLE IF EXISTS col_varchar_table;
执行 1 次耗时： 0.075 秒
正在执行 SQL 语句 1 次： CREATE TABLE text_table ( c1 text DEFAULT NULL,  c2 text DEFAULT NULL,  c3 text DEFAULT NULL,  c4 text DEFAULT NULL);
执行 1 次耗时： 0.146 秒
正在执行 SQL 语句 1 次： CREATE TABLE varchar_table ( c1 varchar(10) DEFAULT NULL, c2 varchar(10) DEFAULT NULL, c3 varchar(10) DEFAULT NULL, c4 varchar(10) DEFAULT NULL);
执行 1 次耗时： 0.096 秒
正在执行 SQL 语句 1 次： CREATE TABLE col_varchar_table (c1 varchar(10) DEFAULT NULL, c2 varchar(10) DEFAULT NULL, c3 varchar(10) DEFAULT NULL, c4 varchar(10) DEFAULT NULL) WITH COLUMN GROUP(each column);
执行 1 次耗时： 0.107 秒
正在执行 SQL 语句 1 次： CREATE TABLE col_text_table ( c1 text DEFAULT NULL, c2 text DEFAULT NULL, c3 text DEFAULT NULL,  c4 text DEFAULT NULL) WITH COLUMN GROUP(each column);
执行 1 次耗时： 0.134 秒
正在执行 SQL 语句 1000 次： insert into varchar_table values ("hello", "world", "go", "home");
执行 1000 次耗时： 0.838 秒
正在执行 SQL 语句 1000 次： insert into text_table values ("hello", "world", "go", "home");
执行 1000 次耗时： 0.860 秒
正在执行 SQL 语句 1000 次： select count(*), c1 from varchar_table group by c2;
执行 1000 次耗时： 1.132 秒
正在执行 SQL 语句 1000 次： select count(*), c1 from text_table group by c2;
执行 1000 次耗时： 1.450 秒
正在执行 SQL 语句 1000 次： select c1, c2, c3 from varchar_table where c4 = "dream";
执行 1000 次耗时： 1.269 秒
正在执行 SQL 语句 1000 次： select c1, c2, c3 from text_table where c4 = "dream";
执行 1000 次耗时： 1.795 秒
正在执行 SQL 语句 1000 次： insert into col_varchar_table values ("hello", "world", "go", "home");
执行 1000 次耗时： 0.781 秒
正在执行 SQL 语句 1000 次： insert into col_text_table values ("hello", "world", "go", "home");
执行 1000 次耗时： 0.873 秒
正在执行 SQL 语句 1000 次： select count(*), c1 from col_varchar_table group by c2;
执行 1000 次耗时： 1.072 秒
正在执行 SQL 语句 1000 次： select count(*), c1 from col_text_table group by c2;
执行 1000 次耗时： 1.423 秒
正在执行 SQL 语句 1000 次： select c1, c2, c3 from col_varchar_table where c4 = "dream";
执行 1000 次耗时： 1.292 秒
正在执行 SQL 语句 1000 次： select c1, c2, c3 from col_text_table where c4 = "dream";
执行 1000 次耗时： 1.765 秒
已断开数据库连接。
```

默认执行 input.sql 脚本里的 SQL，也可以通过 -f 指定自定义脚本。

脚本格式要求：
1. 每个 SQL 占一行
2. 如果 SQL 上有  --times N，则执行这个 SQL N 次。默认只执行一次

例如：
```
--
--input.sql 脚本，用于测试 text 和 varchar 的性能对比
--

DROP TABLE IF EXISTS text_table;
DROP TABLE IF EXISTS col_text_table;
DROP TABLE IF EXISTS varchar_table;
DROP TABLE IF EXISTS col_varchar_table;

CREATE TABLE text_table ( c1 text DEFAULT NULL,  c2 text DEFAULT NULL,  c3 text DEFAULT NULL,  c4 text DEFAULT NULL);
CREATE TABLE varchar_table ( c1 varchar(10) DEFAULT NULL, c2 varchar(10) DEFAULT NULL, c3 varchar(10) DEFAULT NULL, c4 varchar(10) DEFAULT NULL);
CREATE TABLE col_varchar_table (c1 varchar(10) DEFAULT NULL, c2 varchar(10) DEFAULT NULL, c3 varchar(10) DEFAULT NULL, c4 varchar(10) DEFAULT NULL) WITH COLUMN GROUP(each column);
CREATE TABLE col_text_table ( c1 text DEFAULT NULL, c2 text DEFAULT NULL, c3 text DEFAULT NULL,  c4 text DEFAULT NULL) WITH COLUMN GROUP(each column);

--times 1000
insert into varchar_table values ("hello", "world", "go", "home");
--times 1000
insert into text_table values ("hello", "world", "go", "home");
--times 1000
select count(*), c1 from varchar_table group by c2;
--times 1000
select count(*), c1 from text_table group by c2;
--times 1000
select c1, c2, c3 from varchar_table where c4 = "dream";
--times 1000
select c1, c2, c3 from text_table where c4 = "dream";

--times 1000
insert into col_varchar_table values ("hello", "world", "go", "home");
--times 1000
insert into col_text_table values ("hello", "world", "go", "home");
--times 1000
select count(*), c1 from col_varchar_table group by c2;
--times 1000
select count(*), c1 from col_text_table group by c2;
--times 1000
select c1, c2, c3 from col_varchar_table where c4 = "dream";
--times 1000
select c1, c2, c3 from col_text_table where c4 = "dream"
```

