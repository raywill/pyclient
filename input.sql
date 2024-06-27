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
select c1, c2, c3 from col_text_table where c4 = "dream";