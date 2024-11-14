from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 假设的Kimi API配置（请替换为实际的API URL和密钥）
KIMI_API_URL = ' https://api.moonshot.cn/v1/chat/completions'
KIMI_API_KEY = 'sk-nLVz8Tj5pgPhoU9Z095Mk6ngihkOqKCjr1Hqid68mtTAMEHj'


# 定义翻译和润色的函数
def translate_and_polish(text, source=None, target=None, polish_style=None):
    headers = {
        'Authorization': f'Bearer {KIMI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'text': text,
        'source': source,
        'target': target,
        'polish_style': polish_style
    }

    try:
        response = requests.post(KIMI_API_URL, headers=headers, json=data)
        response.raise_for_status()

        # 假设Kimi API返回JSON格式的数据，并且翻译和润色结果在'translated_and_polished_text'字段中
        kimi_response = response.json()
        translated_and_polished_text = kimi_response.get('translated_and_polished_text',
                                                         'Translation and polishing not found')

        return translated_and_polished_text
    except requests.RequestException as e:
        return f'Error calling Kimi API: {e}', 500


# 定义API端点
@app.route('/api/translate/polish', methods=['POST'])
def translate_polish_endpoint():
    data = request.get_json()

    user_id = data.get('userID')
    text = data.get('text')
    source = data.get('source')
    target = data.get('target')
    polish_style = data.get('polish_style')

    if not user_id or not text:
        return jsonify({'error': 'Missing required parameters'}), 400

    # 调用翻译和润色函数
    result, status_code = translate_and_polish(text, source, target, polish_style)

    if isinstance(result, tuple):
        # 如果返回的是一个元组，说明发生了错误
        return jsonify({'error': result[0]}), result[1]

    # 返回翻译和润色后的文本
    return jsonify({'translated_and_polished_text': result}), 200


# 运行Flask应用
if __name__ == '__main__':
    app.run(debug=True)
