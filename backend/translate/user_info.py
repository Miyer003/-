from flask import Flask, request, jsonify, Blueprint,current_app
from flask_cors import CORS
import database as db

user_info = Blueprint('get_info', __name__)

CORS(user_info)

@user_info.route('/users/update', methods=['POST'])
def update_info():
    # 从请求体中获取user_id和fields参数
    data = request.get_json()
    user_id = data.get('user_id')
    username = data.get('username')
    mobile = data.get('mobile')
    location = data.get('location')
    email = data.get('email')

    if not user_id or not username or not mobile or not location or not email:
        return jsonify({
            'base': {
                'code': 400,
                'message': '缺少参数信息'
            }
        }), 400

    query = f"update users SET username = ?, mobile = ?, location = ?, email = ? WHERE user_id = ?"
    args = (username,mobile,location,email,user_id)

    result = db.query_db(query,args,one=True)

    if result:
        return jsonify({
            'base': {
                'code': 200,  # 表示成功
                'message': '修改成功'
            },
        })
    else:
        return jsonify({
            'base': {
                'code': 404,  # 表示失败
                'message': '修改失败'
            },
        })



@user_info.route('/users/info', methods=['GET'])
def get_info():
    # 从请求体中获取user_id和fields参数
    data = request.get_json()
    user_id = data.get('user_id')
    fields = data.get('fields', '').split(',')  # 默认返回全部字段

    if not user_id or not fields:
        return jsonify({
            'base': {
                'code': 400,
                'message': '缺少参数信息'
            }
        }), 400

    query = f"SELECT {', '.join(fields)} FROM users WHERE user_id = ?"
    args = (user_id)

    result = db.query_db(query,args,one=True)

    if result:

        info = {field: result[idx] for idx, field in enumerate(fields) if result[idx] is not None}

        return jsonify({
            'base': {
                'code': 200,  # 表示成功
                'message': '成功'
            },
            'user_id':user_id
            **info
        })
    else:
        return jsonify({
            'base': {
                'code': 400,  # 表示失败
                'message': '查询失败'
            },
        })