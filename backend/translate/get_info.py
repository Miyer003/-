from flask import Flask, request, jsonify, Blueprint,current_app
from flask_cors import CORS
import database as db

get_info = Blueprint('get_info', __name__)

CORS(get_info)

@get_info.route('/v1/weekly-data', methods=['GET'])
def get_info():
    # 从请求体中获取user_id和fields参数
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({
            'base': {
                'code': 400,
                'message': '缺少参数信息'
            }
        }), 400

    nums = 0
    query1 = f"SELECT COUNT(*) AS nums FROM translations WHERE user_id = ?"
    args1 = (user_id)
    nums = db.query_db(query1,args1,one=True)

    query2 = f"SELECT target_language, COUNT(*) AS count FROM translations WHERE user_id = ? GROUP BY target_language ORDER BY count DESC LIMIT 3"
    args2 = (user_id)
    top_languages = db.query_db(query2, args2, one=True)

    top_languages = [{'target_language': lang[0], 'count': lang[1]} for lang in top_languages]

    return jsonify({
        'base': {
            'code': 200,  # 表示成功
            'message': '成功'
        },
        'nums':nums,
        'top_3_languages': top_languages
    })