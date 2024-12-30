from flask import Flask, g
from chat.chat import chat_module, get_db
from translate.translate_cmp import translate_cmp
from translate.translate import translate_module
from translate.user_info import user_info
from translate.get_info import get_info
from user.user import user
from record.record import record
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app, supports_credentials=True, resources=r'/*')

def init_db():
    """初始化数据库，创建表"""
    print("Starting database initialization...")
    try:
        db = get_db()
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        print(f"Opening schema file at: {schema_path}")
        
        # 验证文件是否存在
        if not os.path.exists(schema_path):
            print(f"Schema file does not exist at: {schema_path}")
            return
            
        # 打印 schema.sql 的内容
        with open(schema_path, mode='r') as f:
            schema_content = f.read()
            print(f"Schema content:\n{schema_content}")
            
        # 执行 SQL 脚本
        db.cursor().executescript(schema_content)
        db.commit()
        
        # 验证表是否创建成功
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dialogue_records'")
        if cursor.fetchone():
            print("Table 'dialogue_records' created successfully!")
        else:
            print("Table 'dialogue_records' was not created!")
            
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise e

# 注册蓝图
app.register_blueprint(chat_module)
app.register_blueprint(translate_cmp)
app.register_blueprint(translate_module)
app.register_blueprint(user)
app.register_blueprint(record)
app.register_blueprint(user_info)
app.register_blueprint(get_info)

# 在应用上下文中初始化数据库
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
