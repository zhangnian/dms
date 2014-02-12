#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3


class Db:
	def __init__(self):
		pass

	''' 创建数据库 '''
	def create_db(self, name):
		self.connection = sqlite3.connect(name)

	''' 执行SQL语句 ''' 
	def execute(self, sql):
		cursor = self.connection.cursor()
		cursor.execute(sql)
		self.connection.commit()

	def query(self, sql):
		cursor = self.connection.cursor()
		cursor.execute(sql)

		return cursor.fetchall()


	''' 关闭数据库连接 '''
	def close(self):
		self.connection.close()


if __name__ == "__main__":
	db = Db()
	db.create_db("test.db")

	#db.execute("create table student(id integer primary key, name varchar(10))")
	#db.execute("insert into student(id, name) values(1, 'zhangnian')");

	print db.query("select name, id from student")