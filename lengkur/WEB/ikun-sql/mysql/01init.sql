CREATE DATABASE IF NOT EXISTS cttraining DEFAULT CHARACTER SET utf8mb4;
USE `cttraining`;
CREATE TABLE user(
  id int PRIMARY KEY,
  name varchar(10),
  password varchar(60)
);
INSERT INTO `user`(id,name,password) VALUES(1,'ikun','呀！真的是你呀啊嘿哈哈哈~'),(2,'flag','什么flag，没坐！！！'),(3,'Re0l flag','f14g');
