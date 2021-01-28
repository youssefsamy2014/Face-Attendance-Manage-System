from flask import request,jsonify
import jwt
from functools import wraps
from App.MainAbstract.index import app,Entity_list_Attendance,Entity_list_user


def token_required(f):
    @wraps(f)
    def decorater(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'The token has missing !!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Entity_list_user.query.filter_by(NationalID=data['nationalid']).first()
        except:
            return jsonify({'message': 'Token is invalid !!!'}), 401
        return f(current_user, *args, **kwargs)

    return decorater

def token_required_stu(f):
    @wraps(f)
    def decorater(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'The token has missing !!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Entity_list_Attendance.query.filter_by(NationalID=data['nationalid']).first()
        except:
            return jsonify({'message': 'Token is invalid !!!'}), 401
        return f(current_user, *args, **kwargs)

    return decorater
