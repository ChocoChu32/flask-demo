from flask import Flask, jsonify, request
import re
from common.mysql_oprate import db

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/users", methods=["GET"])
def get_all_users():
    """获取所有用户信息"""
    sql = "SELECT * FROM user"
    data = db.select_db(sql)
    print(f"获取所有用户信息 == >> {data}")
    return jsonify({"code": "0", "data": data, "msg": "查询成功"})


@app.route("/users/<string:username>", methods=["GET"])
def get_user(username):
    """获取某个用户信息"""
    sql = "SELECT * FROM user WHERE username = '{}'".format(username)
    data = db.select_db(sql)
    print(f"获取 {username} 用户信息 == >> {data}")
    if data:
        return jsonify({"code": "0", "data": data, "msg": "查询成功"})
    return jsonify({"code": "1004", "msg": "查不到相关用户的信息"})


@app.route("/register", methods=['POST'])
def user_register():
    """用户注册"""
    username = request.json.get("username").strip()  # 用户名
    password = request.json.get("password").strip()  # 密码
    sex = request.json.get("sex", "0").strip()  # 性别，默认为0(男性)
    telephone = request.json.get("telephone", "").strip()  # 手机号，默认为空串
    address = request.json.get("address", "").strip()  # 地址，默认为空串
    if username and password and telephone:
        sql1 = f"SELECT username FROM user WHERE username = '{username}'"
        res1 = db.select_db(sql1)
        print(f"查询到用户名 ==>> {res1}")
        sql2 = f"SELECT telephone FROM user WHERE telephone = '{telephone}'"
        res2 = db.select_db(sql2)
        print(f"查询到手机号 ==>> {res2}")
        if res1:
            return jsonify({"code": 2002, "msg": "用户名已存在，注册失败！！！"})
        elif not (sex == "0" or sex == "1"):
            return jsonify({"code": 2003, "msg": "输入的性别只能是 0(男) 或 1(女)！！！"})
        elif not (len(telephone) == 11 and re.match("^1[3,5,7,8]\d{9}$", telephone)):
            return jsonify({"code": 2004, "msg": "手机号格式不正确！！！"})
        elif res2:
            return jsonify({"code": 2005, "msg": "手机号已被注册！！！"})
        else:
            sql3 = f"INSERT INTO user(username, password, role, sex, telephone, address) " \
                f"VALUES('{username}', '{password}', '1', '{sex}', '{telephone}', '{address}')"
            db.execute_db(sql3)
            print(f"新增用户信息 ==>> {sql3}")
            return jsonify({"code": 0, "msg": "恭喜，注册成功！"})
    else:
        return jsonify({"code": 2001, "msg": "用户名/密码/手机号不能为空，请检查！！！"})


@app.route("/login", methods=['POST'])
def user_login():
    """用户登录"""
    username = request.values.get("username").strip()
    password = request.values.get("password").strip()
    if username and password:
        sql1 = f"SELECT username FROM user WHERE username = '{username}'"
        res1 = db.select_db(sql1)
        print(f"查询到用户名 ==>> {res1}")
        if not res1:
            return jsonify({"code": 1003, "msg": "用户名不存在！！！"})
        sql2 = f"SELECT * FROM user WHERE username = '{username}' and password = '{password}'"
        res2 = db.select_db(sql2)
        print(f"获取 {username} 用户信息 == >> {res2}")
        if res2:
            return jsonify({"code": 0, "msg": "恭喜，登录成功！"})
        return jsonify({"code": 1002, "msg": "用户名或密码错误！！！"})
    else:
        return jsonify({"code": 1001, "msg": "用户名或密码不能为空！！！"})
