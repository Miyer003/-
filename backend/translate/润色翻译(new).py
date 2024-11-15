from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# 配置你的 OpenAI API Key 和基础 URL
api_key = "sk-nLVz8Tj5pgPhoU9Z095Mk6ngihkOqKCjr1Hqid68mtTAMEHj"  # 请替换为你的实际 API Key
base_url = "https://api.moonshot.cn/v1"

# 初始化 OpenAI 客户端
client = OpenAI(api_key=api_key, base_url=base_url)


@app.route('/api/translate/polish', methods=['POST'])
def translate_and_polish():
    # 从请求中获取用户输入
    data = request.get_json()
    user_id = data.get('userID')
    text = data.get('text')
    source = data.get('source')
    target = data.get('target')
    polish_style = data.get('polish_style')

    if not user_id or not text:
        return jsonify({'error': 'Missing required parameters'}), 400
    if polish_style == '':
        polish_style = "商务"
    # 调用 OpenAI API 进行对话生成

    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system",
             "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
            {"role": "user", "content": "可以帮我翻译后面这句话吗，" + "目标语言为"+target + "，翻译风格为"+polish_style +",只需要翻译结果就行：" + text  }
        ],
        temperature=0.3,
    )

    # 获取并返回 Kimi 的回复
    response_content = completion.choices[0].message.content
    return jsonify({"translation": response_content})


if __name__ == '__main__':
    app.run(debug=True)