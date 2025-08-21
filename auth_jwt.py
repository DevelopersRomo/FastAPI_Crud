from fastapi import HTTPException
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "mi_secreto"

def create_jwt_token(data: dict, expires_in: int = 60):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expires_in)
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def validateToken(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")