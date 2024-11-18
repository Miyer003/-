from flask import Flask
from chat.chat import chat_module

app = Flask(__name__)
# 注册blueprint
app.register_blueprint(chat_module)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)