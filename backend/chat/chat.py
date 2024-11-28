from flask import Flask, request, jsonify, Blueprint, current_app
from openai import OpenAI
import requests
from datetime import datetime
from flask_cors import CORS

# 创建蓝图
chat_module = Blueprint('chat_ai', __name__)

# 设置 DeepSeek API 密钥
DEEPSEEK_API_KEY = 'sk-971fe5b4ee2748e4b88d697a7c98b319'

# 初始化 OpenAI 客户端
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

# 假设我们有一个简单的对话记录存储
dialogue_records = [
    {
        "record_id": 1,
        "user_id": 1,
        "session_id": 1,
        "input_text": "Hello",
        "ai_response": "Hi there!",
        "timestamp": "2023-10-01T12:00:00Z"
    },
    {
        "record_id": 2,
        "user_id": 1,
        "session_id": 1,
        "input_text": "How are you?",
        "ai_response": "I'm good, thanks!",
        "timestamp": "2023-10-01T12:05:00Z"
    },
    {
        "record_id": 3,
        "user_id": 2,
        "session_id": 2,
        "input_text": "What's the weather like?",
        "ai_response": "It's sunny today!",
        "timestamp": "2023-10-01T12:10:00Z"
    }
]

@chat_module.route('/ai/dialogue/record', methods=['POST'])
def record_dialogue():
    # 获取请求头中的 Authorization 令牌
    auth_token = request.headers.get('Authorization')
    
    # 检查令牌是否有效（这里简单地检查是否为 'YOUR_ACCESS_TOKEN'）
    if auth_token != 'YOUR_ACCESS_TOKEN':
        return jsonify({"base": {"code": 401, "message": "Invalid access token"}}), 401

    # 获取请求体中的 JSON 数据
    data = request.json

    # 验证请求体中的字段
    required_fields = ["session_id", "input_text", "timestamp"]
    for field in required_fields:
        if field not in data:
            return jsonify({"base": {"code": 400, "message": f"Missing required field: {field}"}}), 400

    # 确保 user_id 字段存在，如果不存在则设置为默认值 0
    data.setdefault('user_id', 0)

    # 获取输入文本
    input_text = data['input_text']
    
    # 调用 DeepSeek API 生成 AI 响应
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": input_text},
            ],
            stream=False
        )
        ai_response = response.choices[0].message.content.strip()
    except Exception as e:
        # 记录错误日志
        # 其中 blueprint 没有集成 logger
        current_app.logger.error(f"Failed to generate AI response: {str(e)}")
        # 返回一个包含错误信息的 JSON 响应，状态码为 200
        return jsonify({"base": {"code": 500, "message": f"Failed to generate AI response: {str(e)}"}}), 200

    # 将 AI 响应存入对话记录
    data['ai_response'] = ai_response

    # 将对话记录存储到数据库中（这里只是存储在内存中的列表）
    dialogue_records.append(data)

    # 返回成功的响应
    return jsonify({
        "base": {"code": 200, "message": "success"},
        "record_id": len(dialogue_records)
    }), 200

@chat_module.route('/ai/dialogue/records', methods=['GET'])
def get_dialogue_records():
    # 返回所有对话记录
    return jsonify({
        "base": {"code": 200, "message": "success"},
        "records": dialogue_records
    }), 200

@chat_module.route('/ai/dialogue/history', methods=['GET'])
def get_dialogue_history():
    # 获取查询参数
    user_id = request.args.get('user_id')
    session_id = request.args.get('session_id')
    limit_str = request.args.get('limit', '10')  # 默认返回10条记录
    offset_str = request.args.get('offset', '0')  # 默认从第0条记录开始

    # 检查 limit 和 offset 是否为有效的整数
    try:
        limit = int(limit_str)
        offset = int(offset_str)
    except ValueError:
        return jsonify({"base": {"code": 400, "message": "Invalid limit or offset value"}}), 400

    # 过滤对话记录
    filtered_records = [
        record for record in dialogue_records
        if (not user_id or str(record.get('user_id', 0)) == user_id) and
           (not session_id or str(record.get('session_id', 0)) == session_id)
    ]

    # 分页处理
    paginated_records = filtered_records[offset:offset + limit]

    # 返回结果
    return jsonify({
        "base": {"code": 200, "message": "Dialogue history retrieved successfully"},
        "session_id": int(session_id) if session_id else None,
        "data": paginated_records
    }), 200

@chat_module.route('/ai/dialogue', methods=['POST'])
def send_question():
    """处理信息检索部分的问题"""
    try:
        data = request.json
        user_input = data.get('input_text')
        user_id = data.get('user_id')

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

        # 存储对话记录
        dialogue_records.append({
            "user_id": user_id,
            "sender": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        dialogue_records.append({
            "user_id": user_id,
            "sender": "ai",
            "content": answer,
            "timestamp": datetime.now().isoformat()
        })

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

# 只在直接运行此文件时创建应用
if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(chat_module)
    app.run(debug=True, host='0.0.0.0', port=5000)
