# 导入Flask框架和必要的库
from flask import Flask, request, jsonify,Blueprint  # Flask框架，请求对象和JSON响应
from flask_cors import CORS
import sqlite3  # SQLite数据库库
from hashlib import sha256  # 用于生成密码哈希的SHA-256算法
# 创建蓝图
user = Blueprint('user', __name__)
CORS(user)
#app = Flask(__name__)  # 初始化Flask应用

# 数据库初始化函数（通常应在部署时运行一次）
def init_db():
    conn = sqlite3.connect("users.db")  # 连接到SQLite数据库文件
    cur = conn.cursor()  # 创建游标对象
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user (
        phone TEXT PRIMARY KEY,  
        password TEXT NOT NULL,  
        birthday TEXT,  
        avatar TEXT  
    )
    """)  # 如果表不存在，则创建用户表
    conn.commit()  # 提交事务
    conn.close()  # 关闭数据库连接

# 密码哈希生成函数
def generate_password_hash(password):
    return sha256(password.encode()).hexdigest()  # 将密码编码为字节串，使用SHA-256算法生成哈希值，并返回十六进制表示的字符串

# 注册路由
@user.route('/users/register', methods=['POST'])
def register():
    #data = request.get_json()  # 从POST请求中获取JSON数据
    # 提取请求数据
    init_db()
    phone = request.form.get('phone')
    password = request.form.get('password')
    #confirmPassword = request.form.get('confirmPassword')
    birthday = request.form.get('birthday')
    avatar = request.form.get('avatar')

    # 检查两次输入的密码是否一致
    #if password != confirmPassword:
    #    return jsonify({'message': 'Passwords do not match'}), 400  # 密码不匹配，返回400错误

    # 检查手机号是否已存在
    conn = sqlite3.connect("users.db")
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE phone=?", (phone,))
        if cur.fetchone():
            return jsonify({'message': 'Phone number already exists'}), 400  # 手机号已存在，返回400错误

        # 将密码哈希后存入数据库
        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO user (phone, password, birthday, avatar) VALUES (?, ?, ?, ?)",
                    (phone, hashed_password, birthday, avatar))
        conn.commit()  # 提交事务
        return jsonify({'message': 'User registered successfully'}), 201  # 注册成功，返回201状态码
    finally:
        conn.close()  # 关闭数据库连接

# 登录路由
@user.route('/users/login', methods=['POST'])
def login():
    init_db()
    data = request.get_json()  # 从POST请求中获取JSON数据
    phone = data.get('phone')
    password = data.get('password')

    # 验证登录信息
    conn = sqlite3.connect("users.db")
    try:
        cur = conn.cursor()
        cur.execute("SELECT password FROM user WHERE phone=?", (phone,))
        user_password_hash = cur.fetchone()

        if user_password_hash:
            stored_hash = user_password_hash[0]  # 数据库中存储的密码哈希
            input_hash = generate_password_hash(password)  # 输入密码的哈希

            if stored_hash == input_hash:
                return jsonify({'message': 'Login successful'}), 200  # 登录成功，返回200状态码
            else:
                return jsonify({'message': 'Invalid credentials'}), 401  # 凭证无效，返回401错误
        else:
            return jsonify({'message': 'Invalid credentials'}), 401  # 凭证无效，返回401错误
    finally:
        conn.close()  # 关闭数据库连接

# 忘记密码验证生日路由
@user.route('/forgot-password/verify', methods=['POST'])
def verify_birthday():
    init_db()
    data = request.get_json()  # 从POST请求中获取JSON数据
    phone = data.get('phone')
    birthday = data.get('birthday')

    # 验证手机号和生日
    conn = sqlite3.connect("users.db")
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE phone=? AND birthday=?", (phone, birthday))
        user = cur.fetchone()

        if user:
            return jsonify({'message': 'Verification successful'}), 200  # 验证成功，返回200状态码
        else:
            return jsonify({'message': 'Invalid phone or birthday'}), 400  # 手机号或生日无效，返回400错误
    finally:
        conn.close()  # 关闭数据库连接

# 重置密码路由
@user.route('/users/reset-password', methods=['POST'])
def reset_password():
    init_db()
    data = request.get_json()  # 从POST请求中获取JSON数据
    phone = data.get('phone')
    newPassword = data.get('newPassword')

    # 重置密码
    conn = sqlite3.connect("users.db")
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE phone=?", (phone,))
        user = cur.fetchone()

        if user:
            hashed_password = generate_password_hash(newPassword)  # 新密码哈希
            cur.execute("UPDATE user SET password=? WHERE phone=?", (hashed_password, phone))
            conn.commit()  # 提交事务
            return jsonify({'message': 'Password reset successful'}), 200  # 密码重置成功，返回200状态码
        else:
            return jsonify({'message': 'User not found'}), 404  # 用户未找到，返回404错误
    finally:
        conn.close()  # 关闭数据库连接

#if __name__ == '__main__':
#    app.run(debug=True)  # 运行Flask应用，开启调试模式
