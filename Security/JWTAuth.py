import jwt
import os
from datetime import datetime,timedelta, timezone
from fastapi import Cookie,HTTPException



secret_key = os.getenv("JWT_SECRET")
Algorithm = os.getenv("ALGORITHM")
exp_minutes = int(os.getenv("TOKEN_EXPIRATION"))  
user_instance = {}

def create_jwt_token(userid,user_role):
    exp_time = datetime.now(timezone.utc) + timedelta(minutes=exp_minutes)
    payload = {
        "userid": userid,
        "user_role": user_role,
        "iat": datetime.now(timezone.utc),
        "exp": exp_time.timestamp()
    }

    token = jwt.encode(payload, secret_key, algorithm=Algorithm)
    print("Generated JWT Token:", token)
    return token

def decode_jwt_token(token):
    try:
        decoded_payload = jwt.decode(token, secret_key, algorithms=[Algorithm])
        user_instance["userid"] = decoded_payload["userid"]
        user_instance["user_role"] = decoded_payload["user_role"]
        return user_instance
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    


def get_user_id( token: str = Cookie(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    try:
        decoded_user = decode_jwt_token(token)
        return int(decoded_user["userid"])
    except HTTPException as e:
        raise HTTPException(status_code=401, detail=f" {e.detail}")


def get_current_user(token: str):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    try:
        return decode_jwt_token(token)
    except HTTPException as e:
        raise HTTPException(status_code=401, detail=f" {e.detail}")


def is_valid_user(required_role: list , token: str = Cookie(None)):
    
    user_data = get_current_user(token) 
    if user_data["user_role"] not in required_role:
        raise HTTPException(status_code=403, detail="User does not have the required role")
    return user_data["userid"]