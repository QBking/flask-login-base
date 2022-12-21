import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta

from RealProject.config import SECRET_KEY, TOKEN_EXP_DAY


def genToken(data):
    expInt = datetime.utcnow() + timedelta(days=TOKEN_EXP_DAY)
    payload = {
        'exp': expInt,
        'data': data
    }
    token = jwt.encode(payload, key=SECRET_KEY, algorithm='HS256')
    return bytes.decode(token)


def verifyToken(tokenStr):
    try:
        tokenBytes = tokenStr.encode('utf-8')
        payload = jwt.decode(tokenBytes, key=SECRET_KEY, algorithm='HS256')
        return payload
    except PyJWTError as e:
        print("jwt验证失败: %s" % e)
        return None
