from flask import Flask, request, jsonify
from openai import OpenAI
import time

app = Flask(__name__)


client = OpenAI(
    api_key="sk-7s63CxEEh75mtgaktYAJAAM86VMY3FfJbr146AQ3NZkTz6rl",#到时候替换成统一的api key
    base_url="https://api.moonshot.cn/v1",
)

def chat_once(msgs):
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",#model="moonshot-v1-auto"
        messages=msgs,
        temperature=0.3,
    )
    return completion.choices[0].message.content

def call_kimi_api(source_text, target_language, max_attempts = 10) -> str:
    messages = [
        {"role": "system",
         "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
    ]

    # 我们将用户最新的问题构造成一个 message（role=user），并添加到 messages 的尾部
    messages.append({"role": "user",
                     "content": f"请将以下内容翻译成{target_language}，只需给出译文，不要再加任何文字，如果原文内容与需翻译成的为同一语言，返回原文；若原文内容有误，请你根据上下文修改原文内容后再翻译。需要翻译的内容为：{source_text}"
                     })

    for i in range(max_attempts):
        try:
            response = chat_once(messages)
            return response
        except Exception:
            time.sleep(1)
            continue

    return "无法连接大语言模型"


@app.route('/translate/instant', methods=['POST'])
def translate_instant():
    # 获取请求数据
    data = request.get_json()
    user_id = data.get('user_id')
    source_text = data.get('source_text')
    source_language = data.get('source_language')
    target_language = data.get('target_language')

    # 检查必要的参数是否存在
    if not data or 'user_id' not in data or 'source_text' not in data or 'source_language' not in data or 'target_language' not in data:
        # 参数不正确，返回400状态码
        return jsonify({
            'base': {
                'code': 400,
                'message': 'Invalid input'
            }
        }), 400

    # 调用Kimi API的代码获取翻译结果
    translation_result = call_kimi_api(source_text, target_language)

    if translation_result != "无法连接大语言模型":
        # 返回翻译结果给前端
        return jsonify({
            'base': {
                'code': 200,  # 表示成功
                'message': '翻译成功'
            },
            'translation': translation_result
        })
    else:
        return jsonify({
            'base': {
                'code': 400,  # 表示失败
                'message': '翻译失败'
            },
            'translation': translation_result
        })

if __name__ == '__main__':
    app.run()