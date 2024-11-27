from flask import Flask
from chat.chat import chat_module
from translate.translate_cmp import translate_cmp
from translate.translate import translate_module
app = Flask(__name__)
# 注册blueprint
app.register_blueprint(chat_module)
app.register_blueprint(translate_cmp)
app.register_blueprint(translate_module)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
