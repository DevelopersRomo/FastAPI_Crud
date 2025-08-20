import jwt
from datetime import datetime, timedelta

SECRET_KEY = "mi_secreto"

def create_jwt_token(data: dict, expires_in: int = 60):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expires_in)
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
