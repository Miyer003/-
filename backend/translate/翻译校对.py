from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# 配置你的 OpenAI API Key 和基础 URL
api_key = "sk-nLVz8Tj5pgPhoU9Z095Mk6ngihkOqKCjr1Hqid68mtTAMEHj"  # 请替换为你的实际 API Key
base_url = "https://api.moonshot.cn/v1"

# 初始化 OpenAI 客户端
client = OpenAI(api_key=api_key, base_url=base_url)


@app.route('/api/translate/proofread', methods=['POST'])
def translate_and_polish():
    # 从请求中获取用户输入
    data = request.get_json()
    user_id = data.get('userID')
    originalText = data.get('originalText')
    translatedText = data.get('translatedText')


    if not user_id or not originalText or not translatedText :
        return jsonify({'error': 'Missing required parameters'}), 400
    # 调用 OpenAI API 进行对话生成

    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system",
             "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
            {"role": "user", "content": "请帮我进行对后面两个语句进行翻译校对" + "原文内容：" + originalText + "翻译内容：" + translatedText + "只需要返回 语法检查结果、内容一致性检查结果、术语校验结果、语言风格一致性检查结果、句式优化建议，这五个内容，换行输出" }
        ],
        temperature=0.3,
    )

    # 获取并返回 Kimi 的回复
    response_content = completion.choices[0].message.content
    lines = response_content.splitlines()
    grammarCheck = lines[0]
    contentConsistency = lines[1]
    terminologyValidation = lines[2]
    languageStyle = lines[3]
    sentenceStructure = lines[4]
    return jsonify({ "grammarCheck" : lines[0],
    "contentConsistency" : lines[1],
    "terminologyValidation" : lines[2],
    "languageStyle" : lines[3],
    "sentenceStructure" : lines[4]})


if __name__ == '__main__':
    app.run(debug=True)