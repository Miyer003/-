from fastapi import FastAPI, HTTPException, Query
#from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import traceback
import logging
import os

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
recor = Blueprint('record', __name__)

#app = Flask(__name__)  # 初始化Flask应用
CORS(record)  # 允许所有来源的跨域请求
#app = FastAPI()

#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=["*"],
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#)


class ProofreadRequest(BaseModel):
    user_id: int
    originalText: str
    translatedText: str
    score: int
    grammarCheck: str
    terminologyValidation: str
    contentConsistency: str
    languageStyle: str
    sentenceStructure: str


def get_db_connection():
    # SQLite 数据库文件路径，可以是相对路径或绝对路径
    db_path = os.path.join(os.getcwd(), "First.db")
    print("Database path:", db_path)
    conn = sqlite3.connect(db_path)
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # 检查表是否存在
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='translationProof_history'")
    tables = cursor.fetchall()

    if not tables:
        # 创建表
        create_table_query = '''
        CREATE TABLE translationProof_history (
            user_id INTEGER,
            originalText TEXT,
            translatedText TEXT,
            score INTEGER,
            grammarCheck TEXT,
            terminologyValidation TEXT,
            contentConsistency TEXT,
            languageStyle TEXT,
            sentenceStructure TEXT
        )
        '''
        cursor.execute(create_table_query)
        conn.commit()
        logger.info("Table 'translationProof_history' created.")

    cursor.close()
    conn.close()


# 初始化数据库（在应用启动时调用）
init_db()


# 上传翻译校对的记录
@app.post("/translate/upproofread")
async def save_proofread_result(request: ProofreadRequest):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO translationProof_history (user_id, originalText, translatedText, score, grammarCheck, terminologyValidation, contentConsistency, languageStyle, sentenceStructure)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            request.user_id,
            request.originalText,
            request.translatedText,
            request.score,
            request.grammarCheck,
            request.terminologyValidation,
            request.contentConsistency,
            request.languageStyle,
            request.sentenceStructure
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success", "message": "Proofread result saved successfully"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# 查看翻译校对的历史记录
@app.get("/translate/history")
async def get_history(user_id: int = Query(..., description="User ID")):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM translationProof_history WHERE user_id = ?"
        cursor.execute(query, (user_id,))
        records = cursor.fetchall()
        cursor.close()
        conn.close()

        # 记录查询到的记录数
        print("查询结果:", records)

        # 返回查询到的记录
        return {"status": "success", "data": records,
                "message": f"Retrieved {len(records)} records for user_id {user_id}"}
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


#if __name__ == "__main__":
#    import uvicorn

#    uvicorn.run(app, host='127.0.0.1', port=5000)
