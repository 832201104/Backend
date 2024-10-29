from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql.cursors
import numpy as np

# Connect to the database
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='root',
                             db='addressBook',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)


# 保持数据库连接
def getconnection():
    connection.ping(reconnect=True)
    return connection


# 搜索
@app.route('/search')
def search():
    id = request.args.get('id')
    name = request.args.get('name')
    try:
        with getconnection().cursor() as cursor:
            if id is not None:
                # 如果id参数不为空，执行带有id的查询
                sql = "SELECT * FROM `info` where id = %s"
                cursor.execute(sql, (id))
            elif name is not None:
                # 如果name参数不为空，执行带有name的查询
                sql = "SELECT * FROM `info` where name like %s"
                cursor.execute(sql, ('%' + name + '%'))
            else:
                # 查询全部
                sql = "SELECT * FROM `info`"
                cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            if not result:
                result = []
            return result
    except Exception as e:
        cursor.close()
        return "查询失败!"


@app.route('/add')
def add():
    name = request.args.get('name')
    tel = request.args.get('tel')
    birthday = request.args.get('birthday')
    remark = request.args.get('remark')
    try:
        with getconnection().cursor() as cursor:
            sql = "INSERT INTO `info` (`name`, `tel`,`birthday`,`remark`) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql, (name, tel, birthday, remark))
            connection.commit()
            cursor.close()
            return "添加成功"
    except Exception as e:
        cursor.close()
        return "添加失败"


# 修改
@app.route('/edit')
def edit():
    id = request.args.get('id')
    name = request.args.get('name')
    tel = request.args.get('tel')
    birthday = request.args.get('birthday')
    remark = request.args.get('remark')
    try:
        with getconnection().cursor() as cursor:
            sql = "update `info` set name=%s,tel=%s,birthday=%s,remark=%s where id=%s"
            cursor.execute(sql, (name, tel, birthday, remark, id))
            connection.commit()
            cursor.close()
            return "修改成功"
    except Exception as e:
        cursor.close()
        return "修改失败"


# 删除
@app.route('/remove/<int:id>/')
def remove(id):
    try:
        with getconnection().cursor() as cursor:
            sql = "delete from `info` where id=%s"
            cursor.execute(sql, (id))
            connection.commit()
            cursor.close()
            return "删除成功"
    except Exception as e:
        cursor.close()
        return "删除失败"


if __name__ == '__main__':
    # 指定程序运行端口为 8001
    app.run(host='127.0.0.1', port=8001, debug=True)
