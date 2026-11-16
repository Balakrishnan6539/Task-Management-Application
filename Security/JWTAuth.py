import jwt
import os
from datetime import datetime,timedelta, timezone
from fastapi import Cookie,HTTPException,Depends
from dotenv import load_dotenv
from fastapi import Response


load_dotenv()

secret_key = os.getenv("SECRET_KEY")
Algorithm = os.getenv("ALGORITHM")
exp_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))  

if not secret_key:
    raise RuntimeError("secret key is missing or not loaded")



def create_jwt_token(userid,user_role):
    exp_time = datetime.now(timezone.utc) + timedelta(minutes=exp_minutes)
    print(user_role)
    print(userid)
    payload = {
        "userid": userid,
        "user_role": user_role,
        "iat": datetime.now(timezone.utc),
        "exp": exp_time.timestamp()
    }

    token = jwt.encode(payload, secret_key, algorithm=Algorithm)


    return token

def decode_jwt_token(token):
    try:
        decoded_payload = jwt.decode(token, secret_key, algorithms=[Algorithm])

        return decoded_payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    


def get_current_user(token : str = Cookie(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")

    return decode_jwt_token(token)
    

def get_user_id( user_data : dict = Depends(get_current_user)):
    if not user_data:
        raise HTTPException(status_code=401, detail="user data is not present in token")

    return int(user_data["userid"])


def is_valid_user(required_role: list):

    def role_checker(user_data: dict = Depends(get_current_user)):
        print(user_data["user_role"])
        print(required_role)
        if user_data["user_role"] not in required_role:
            raise HTTPException(status_code=403, detail="you dont have the required role to access")
        return int(user_data["userid"])
    
    return role_checker