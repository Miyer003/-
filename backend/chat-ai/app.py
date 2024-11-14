from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

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

@app.route('/ai/dialogue/record', methods=['POST'])
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
        app.logger.error(f"Failed to generate AI response: {str(e)}")
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

@app.route('/ai/dialogue/records', methods=['GET'])
def get_dialogue_records():
    # 返回所有对话记录
    return jsonify({
        "base": {"code": 200, "message": "success"},
        "records": dialogue_records
    }), 200

@app.route('/ai/dialogue/history', methods=['GET'])
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

if __name__ == '__main__':
    app.run(debug=True)