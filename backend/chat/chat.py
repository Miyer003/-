from flask import Flask, request, jsonify, Blueprint, current_app, g
from openai import OpenAI
import sqlite3
from datetime import datetime
import os
from flask_cors import CORS

# 创建蓝图
chat_module = Blueprint('chat_ai', __name__)
CORS(chat_module)
# 设置数据库路径
DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'chat.db')

# 数据库相关函数
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    with chat_module.app_context():
        db = get_db()
        with current_app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@chat_module.teardown_app_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# 设置 DeepSeek API 密钥
DEEPSEEK_API_KEY = 'sk-971fe5b4ee2748e4b88d697a7c98b319'

# 初始化 OpenAI 客户端
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

@chat_module.route('/ai/dialogue/record', methods=['POST'])
def record_dialogue():
    try:
        # 获取请求头中的 Authorization 令牌
        auth_token = request.headers.get('Authorization')
        
        # 检查令牌是否有效
        if auth_token != 'YOUR_ACCESS_TOKEN':
            return jsonify({"base": {"code": 401, "message": "Invalid access token"}}), 401

        # 获取请求体中的 JSON 数据
        data = request.json

        # 验证请求体中的字段
        required_fields = ["session_id", "input_text", "timestamp"]
        for field in required_fields:
            if field not in data:
                return jsonify({"base": {"code": 400, "message": f"Missing required field: {field}"}}), 400

        # 确保 user_id 字段存在
        data.setdefault('user_id', 0)

        # 获取输入文本
        input_text = data['input_text']
        
        # 调用 DeepSeek API 生成 AI 响应
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": input_text},
            ],
            stream=False
        )
        ai_response = response.choices[0].message.content.strip()

        # 将对话记录存入数据库
        db = get_db()
        cur = db.cursor()
        cur.execute('''
            INSERT INTO dialogue_records 
            (user_id, session_id, input_text, ai_response, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['user_id'], data['session_id'], input_text, ai_response, data['timestamp']))
        db.commit()
        record_id = cur.lastrowid

        return jsonify({
            "base": {"code": 200, "message": "success"},
            "record_id": record_id
        }), 200

    except Exception as e:
        current_app.logger.error(f"Failed to record dialogue: {str(e)}")
        return jsonify({"base": {"code": 500, "message": f"Failed to record dialogue: {str(e)}"}}), 200

@chat_module.route('/ai/dialogue/records', methods=['GET'])
def get_dialogue_records():
    try:
        records = query_db('SELECT * FROM dialogue_records ORDER BY timestamp DESC')
        return jsonify({
            "base": {"code": 200, "message": "success"},
            "records": [dict(record) for record in records]
        }), 200
    except Exception as e:
        current_app.logger.error(f"Failed to get dialogue records: {str(e)}")
        return jsonify({"base": {"code": 500, "message": str(e)}}), 200

@chat_module.route('/ai/dialogue/history', methods=['GET'])
def get_dialogue_history():
    try:
        # 获取查询参数
        user_id = request.args.get('user_id')
        session_id = request.args.get('session_id')
        limit = int(request.args.get('limit', '10'))
        offset = int(request.args.get('offset', '0'))

        # 构建查询条件
        query = 'SELECT * FROM dialogue_records WHERE 1=1'
        params = []
        
        if user_id:
            query += ' AND user_id = ?'
            params.append(user_id)
        if session_id:
            query += ' AND session_id = ?'
            params.append(session_id)

        query += ' ORDER BY timestamp DESC LIMIT ? OFFSET ?'
        params.extend([limit, offset])

        # 执行查询
        records = query_db(query, params)

        return jsonify({
            "base": {"code": 200, "message": "Dialogue history retrieved successfully"},
            "session_id": int(session_id) if session_id else None,
            "data": [dict(record) for record in records]
        }), 200

    except ValueError as e:
        return jsonify({"base": {"code": 400, "message": "Invalid limit or offset value"}}), 400
    except Exception as e:
        current_app.logger.error(f"Failed to get dialogue history: {str(e)}")
        return jsonify({"base": {"code": 500, "message": str(e)}}), 200

@chat_module.route('/ai/dialogue', methods=['POST'])
def send_question():
    try:
        data = request.json
        user_input = data.get('input_text')
        user_id = data.get('user_id', 0)

        if not user_input:
            return jsonify({
                "status": 400,
                "message": "输入文本不能为空"
            }), 400

        # 调用DeepSeek API获取回答
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": user_input},
            ],
            stream=False
        )
        
        answer = response.choices[0].message.content.strip()

        # 存储对话记录到数据库
        db = get_db()
        cur = db.cursor()
        timestamp = datetime.now().isoformat()
        cur.execute('''
            INSERT INTO dialogue_records (user_id, session_id, input_text, ai_response, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, 1, user_input, answer, timestamp))
        db.commit()

        return jsonify({
            "status": 200,
            "answer": answer
        })

    except Exception as e:
        current_app.logger.error(f"处理问题时发生错误: {str(e)}")
        return jsonify({
            "status": 500,
            "message": f"服务器错误: {str(e)}"
        }), 500

@chat_module.route('/api/detectLanguage', methods=['POST'])
def detect_language():
    """检测文本语言"""
    try:
        data = request.json
        text = data.get('text')
        
        if not text:
            return jsonify({
                "status": 400,
                "message": "文本不能为空"
            }), 400

        # 这里可以使用第三方服务或库来检测语言
        # 示例使用简单的规则判断
        def simple_detect(text):
            # 简单示例：检查是否包含中文字符
            if any('\u4e00' <= char <= '\u9fff' for char in text):
                return 'zh'
            return 'en'
        
        detected_lang = simple_detect(text)
        
        return jsonify({
            "status": 200,
            "language": detected_lang
        })

    except Exception as e:
        current_app.logger.error(f"语言检测时发生错误: {str(e)}")
        return jsonify({
            "status": 500,
            "message": f"服务器错误: {str(e)}"
        }), 500

@chat_module.route('/api/translate/polish', methods=['POST'])
def auto_polish():
    """处理自动润色请求"""
    try:
        data = request.json
        text = data.get('text')
        target = data.get('target', 'zh')  # 默认目标语言为中文
        
        if not text:
            return jsonify({
                "status": 400,
                "message": "文本不能为空"
            }), 400

        # 调用DeepSeek API进行润色
        prompt = f"请对以下文本进行润色和优化，目标语言为{'中文' if target == 'zh' else '英文'}：\n{text}"
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a professional text polishing assistant"},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )
        
        polished_text = response.choices[0].message.content.strip()

        return jsonify({
            "status": 200,
            "translation": polished_text
        })

    except Exception as e:
        current_app.logger.error(f"文本润色时发生错误: {str(e)}")
        return jsonify({
            "status": 500,
            "message": f"服务器错误: {str(e)}"
        }), 500


