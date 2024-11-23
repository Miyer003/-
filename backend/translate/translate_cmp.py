from flask import Flask, request, jsonify,Blueprint
from openai import OpenAI
from flask_cors import CORS

translate_cmp = Blueprint('translate_cmp', __name__)
#app = Flask(__name__)
CORS(translate_cmp)  # 允许所有域名访问
# 配置你的 OpenAI API Key 和基础 URL
api_key = "sk-7s63CxEEh75mtgaktYAJAAM86VMY3FfJbr146AQ3NZkTz6rl"  # 请替换为你的实际 API Key
base_url = "https://api.moonshot.cn/v1"

# 初始化 OpenAI 客户端
client = OpenAI(api_key=api_key, base_url=base_url)


@translate_cmp.route('/translate/proofread', methods=['POST'])
def translate_and_polish():
    # 从请求中获取用户输入（从 JSON 中）
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid JSON input'}), 400

    user_id = data.get('user_id')
    originalText = data.get('originalText')
    translatedText = data.get('translatedText')

    # 验证输入参数
    if not user_id or not originalText or not translatedText:
        return jsonify({'error': 'Missing required parameters'}), 400

    # 调用 OpenAI API 进行对话生成
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system",
             "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
            {"role": "user",
             "content": "请帮我进行对后面两个语句进行翻译校对,点评一下翻译有没有问题，" + "原文语句：‘" + originalText + "’，我的翻译结果：‘" + translatedText + "’。只需要返回 语法检查结果、内容一致性检查结果、术语校验结果、语言风格一致性检查结果、句式优化建议（如果我的翻译太差，可以给出你的翻译结果进行参考，如果我翻译的差不多，则回复我大致符合，给点小修改就行）、翻译打分（只需要分数，且是整数），这六个个内容，每个内容回复一行，希望不要回答得太简略"}
        ],
        temperature=0.3,
    )

    # 获取并返回 Kimi 的回复
    response_content = completion.choices[0].message.content
    lines = response_content.splitlines()

    # 确保有足够的行数来避免 IndexError
    if len(lines) < 6:
        return jsonify({'error': 'Unexpected response format from OpenAI'}), 500

    grammarCheck = lines[0]
    contentConsistency = lines[1]
    terminologyValidation = lines[2]
    languageStyle = lines[3]
    sentenceStructure = lines[4]
    per_score = lines[5]
    text = per_score.split('：')
    score = int(text[1].strip())  # 确保去掉前后空格

    return jsonify({
        "grammarCheck": grammarCheck,
        "contentConsistency": contentConsistency,
        "terminologyValidation": terminologyValidation,
        "languageStyle": languageStyle,
        "sentenceStructure": sentenceStructure,
        "score": score
    })

#if __name__ == '__main__':
#    app.run(debug=True)
