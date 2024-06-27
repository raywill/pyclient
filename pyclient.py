#!/usr/bin/env python3

import argparse
import pymysql
import time
import re

# 解析 SQL 文件并获取每条 SQL 语句及其执行次数
def parse_sql_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    pattern = re.compile(r'--times\s*(\d+)', re.IGNORECASE)
    sql_statements_with_times = []
    execute_times = 1

    for line in lines:
        match = pattern.search(line)
        if match:
            execute_times = int(match.group(1))  # 获取执行次数
        elif line.strip() and not line.startswith('--'):
            # 这是 SQL 语句
            sql_statements_with_times.append((line.strip(), execute_times))
            execute_times = 1  # 重置执行次数

    return sql_statements_with_times

# 设置命令行参数
parser = argparse.ArgumentParser(description="在 MySQL 数据库上执行 SQL 语句。", add_help=False)
parser.add_argument("-h", "--host", required=True, help="MySQL 服务器的主机名或IP地址。")
parser.add_argument("-P", "--port", required=True, help="MySQL 服务器的端口号。", type=int)
parser.add_argument("-u", "--user", required=True, help="连接 MySQL 数据库的用户名。")
parser.add_argument("-p", "--password", required=False, help="连接 MySQL 数据库的密码。")
parser.add_argument("-D", "--database", required=True, help="要在其中执行 SQL 语句的数据库名称。")
parser.add_argument("-f", "--file", default="input.sql", help="要执行的 SQL 脚本路径。")
parser.add_argument("--help", action="help", default=argparse.SUPPRESS, help="显示此帮助信息并退出。")

args = parser.parse_args()

# 建立连接到数据库
connection = pymysql.connect(host=args.host,
                             port=args.port,
                             user=args.user,
                             password=args.password,
                             db=args.database)
cursor = connection.cursor()

# 从 input.sql 文件中读取 SQL 语句及其执行次数
print(f"解析脚本： {args.file}")
sql_statements_with_times = parse_sql_file(args.file)

# 执行 SQL 语句
for statement, times in sql_statements_with_times:
    print(f"正在执行 SQL 语句 {times} 次： {statement}")
    start_time = time.time()  # 记录开始时间

    try:
        for _ in range(times):
            cursor.execute(statement)

            # 如果是 SELECT 语句，取出并丢弃所有结果
            if statement.lower().startswith('select'):
                cursor.fetchall()
            else:
                connection.commit()
    except Exception as e:
        print(f"执行 SQL 语句时出错： {e}")
        continue  # 跳过当前 SQL 语句的剩余次数，并继续下一个

    end_time = time.time()  # 记录结束时间
    time_taken = end_time - start_time  # 计算经过的时间
    print(f"执行 {times} 次耗时： {time_taken:.3f} 秒")

# 断开数据库连接
cursor.close()
connection.close()
print("已断开数据库连接。")