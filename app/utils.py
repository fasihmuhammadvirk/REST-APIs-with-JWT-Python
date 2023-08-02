# block of code for hashing the password

from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


# block of code for generating the jwt token
import os
from datetime import datetime, timedelta
from typing import Union, Any

## pip3 install python-jose 
from jose import jwt, ExpiredSignatureError, JWTError
from datetime import datetime

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = str(os.environ.get('JWT_SECRET_KEY'))  # should be kept secret
JWT_REFRESH_SECRET_KEY = str(os.environ.get('JWT_REFRESH_SECRET_KEY'))    # should be kept secret


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt, expires_delta


def decode_access_token(token: str, user_name: str):
    is_user = False
    is_exp = True

    try:
        # Decode the JWT token using the provided secret key and algorithm
        decoded_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        # Extract the user ID (subject) from the payload
        user_id = decoded_payload.get('sub')
        exp_time = datetime.fromtimestamp(decoded_payload.get('exp'))

        if user_name == user_id:
            is_user = True

        current_time = datetime.utcnow()
        if exp_time > current_time:
            is_exp = False

    except ExpiredSignatureError:
        # Token has expired
        is_exp = True
    except JWTError:
        # Invalid token
        is_user = False
        is_exp = False

    return is_user, is_exp