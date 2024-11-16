from flask import Flask, request, jsonify
from openai import OpenAI
import time
from PyPDF2 import PdfReader
from docx import Document
from io import BytesIO
from PIL import Image
from paddleocr import PaddleOCR
import numpy as np


app = Flask(__name__)

# 配置 OpenAI API Key 和基础 URL
api_key = "sk-7s63CxEEh75mtgaktYAJAAM86VMY3FfJbr146AQ3NZkTz6rl"  # 请替换为你的实际 API Key
base_url = "https://api.moonshot.cn/v1"

# 初始化 OpenAI 客户端
client = OpenAI(api_key=api_key, base_url=base_url)

def chat_once(msgs):
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=msgs,
        temperature=0.3,
    )
    return completion.choices[0].message.content

def call_kimi_api(source_text, target_language, max_attempts=10) -> str:
    messages = [
        {"role": "system",
         "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
        {"role": "user",
         "content": f"请将以下内容翻译成{target_language}，只需给出译文，不要再加任何文字，如果原文内容与需翻译成的为同一语言，返回原文；若原文内容有误，请你根据上下文修改原文内容后再翻译。需要翻译的内容为：{source_text}"}
    ]

    for i in range(max_attempts):
        try:
            response = chat_once(messages)
            return response
        except Exception:
            time.sleep(1)
            continue

    return "无法连接大语言模型"

# 翻译文档
@app.route('/translate/document', methods=['POST'])
def translate_doc():
    # 检查文件是否为空
    if 'document' not in request.files or 'user_id' not in request.form or 'target_language' not in request.form:
        return jsonify({
            'base': {
                'code': 400,
                'message': 'No file found or invalid input'
            }
        }), 400

    # 获取请求数据
    user_id = request.form.get('user_id')
    target_language = request.form.get('target_language')
    # 获取上传的文件
    file = request.files.get('document')

    # 读取文件内容
    if file.filename.endswith('.pdf'):
        # 使用PyPDF2读取PDF文件内容
        content = ''
        with file.stream as f:
            reader = PdfReader(f)
            for page in reader.pages:
                content += page.extract_text() + '\n'
    elif file.filename.endswith('.docx'):
        # 使用python-docx读取DOCX文件内容
        file_stream = BytesIO(file.read())
        doc = Document(file_stream)
        content = ''
        for para in doc.paragraphs:
            content += para.text + '\n'
    elif file.filename.endswith('.txt'):
        # 直接读取TXT文件内容
        content = file.stream.read().decode('utf-8')
    else:
        return jsonify({
            'base': {
                'code': 500,
                'message': '不支持的文件格式或文件无法打开'
            }
        }), 500

    # 调用Kimi API的代码获取翻译结果
    translation_result = call_kimi_api(content, target_language)

    if translation_result != "无法连接大语言模型":
        # 返回翻译结果给前端
        return jsonify({
            'base': {
                'code': 200,
                'message': '翻译成功'
            },
            'translation': translation_result
        })
    else:
        return jsonify({
            'base': {
                'code': 400,
                'message': '翻译失败'
            },
            'translation': translation_result
        })

# 即时翻译
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
                'code': 200,
                'message': '翻译成功'
            },
            'translation': translation_result
        })
    else:
        return jsonify({
            'base': {
                'code': 400,
                'message': '翻译失败'
            },
            'translation': translation_result
        })

# 翻译OCR
@app.route('/translate/image', methods=['POST'])
def translate_ocr():
    # 检查文件是否为空
    if 'image' not in request.files or 'user_id' not in request.form or 'target_language' not in request.form:
        return jsonify({
            'base': {
                'code': 400,
                'message': 'No file found or invalid input'
            }
        }), 400

    # 获取请求数据
    user_id = request.form.get('user_id')
    target_language = request.form.get('target_language')
    # 获取上传的文件
    image_file = request.files.get('image')

    # 将图片文件转换为PIL Image对象
    try:
        image = Image.open(image_file.stream)
        image_array = np.array(image)
    except IOError:
        return jsonify({
            'base': {
                'code': 500,
                'message': 'Unable to read image file'
            }
        }), 500

    # 使用PaddleOCR识别图片中的文字
    ocr = PaddleOCR(use_angle_cls=True)  # 使用方向分类器
    results = ocr.ocr(image_array, cls=True)

    source_text = ""
    # 遍历识别结果，将每个结果的文本添加到source_text中，并用换行符隔开
    for line in results:
        for words in line:
            source_text += words[-1][0] + '\n'
    # 去掉最后多余的换行符
    source_text = source_text.strip()

    # 调用Kimi API的代码获取翻译结果
    translation_result = call_kimi_api(source_text, target_language)

    if translation_result != "无法连接大语言模型":
        # 返回翻译结果给前端
        return jsonify({
            'base': {
                'code': 200,
                'message': '翻译成功'
            },
            'source_text': source_text,
            'translation': translation_result
        })
    else:
        return jsonify({
            'base': {
                'code': 400,
                'message': '翻译失败'
            },
            'source_text': source_text,
            'translation': translation_result
        })

# 翻译校对
@app.route('/api/translate/proofread', methods=['POST'])
def translate_and_polish():
    # 从请求中获取用户输入
    data = request.get_json()
    user_id = data.get('userID')
    originalText = data.get('originalText')
    translatedText = data.get('translatedText')

    if not user_id or not originalText or not translatedText:
        return jsonify({'error': 'Missing required parameters'}), 400

    # 调用 OpenAI API 进行对话生成
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system",
             "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
            {"role": "user", "content": "请帮我进行对后面两个语句进行翻译校对" + "原文内容：" + originalText + "翻译内容：" + translatedText + "只需要返回 语法检查结果、内容一致性检查结果、术语校验结果、语言风格一致性检查结果、句式优化建议，这五个内容，换行输出，其他都不要出现！"}
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
    return jsonify({
        "grammarCheck": lines[0],
        "contentConsistency": lines[1],
        "terminologyValidation": lines[2],
        "languageStyle": lines[3],
        "sentenceStructure": lines[4]
    })
@app.route('/api/translate/personalized', methods=['POST'])
def personalized_translate():
# 从请求中获取用户输入
   data = request.get_json()
   user_id = data.get('userID')
   text = data.get('text')
   source = data.get('source')
   target = data.get('target')
   if not user_id or not text:
        return jsonify({'error': 'Missing required parameters'}), 400

# 调用 OpenAI API 进行对话生成
   completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
        {"role": "system",
         "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
        {"role": "user", "content": "可以帮我翻译后面这句话吗，" + "目标语言为" + target + ",只需要翻译结果就行：" + text}
        ],
    temperature=0.3,
)

# 获取并返回 Kimi 的回复
   response_content = completion.choices[0].message.content
   return jsonify({"translation": response_content})
@app.route('/api/translate/polish', methods=['POST'])
def polish_translate():
# 从请求中获取用户输入
   data = request.get_json()
   user_id = data.get('userID')
   text = data.get('text')
   source = data.get('source')
   target = data.get('target')
   polish_style = data.get('polish_style', "商务")
   if not user_id or not text:
      return jsonify({'error': 'Missing required parameters'}), 400

# 调用 OpenAI API 进行对话生成
   completion = client.chat.completions.create(
    model="moonshot-v1-8k",
       messages=[
        {"role": "system",
         "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
        {"role": "user", "content": "可以帮我翻译后面这句话吗，" + "目标语言为" + target + "，翻译风格为" + polish_style + ",只需要翻译结果就行：" + text}
       ],
    temperature=0.3,
)

# 获取并返回 Kimi 的回复
   response_content = completion.choices[0].message.content
   return jsonify({"translation": response_content})

if __name__ == '__main__':
    app.run(debug=True)