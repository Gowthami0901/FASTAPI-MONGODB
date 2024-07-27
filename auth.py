from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from pydantic import BaseModel
import os
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["demo"]

def get_next_sequence_value(sequence_name: str) -> int:
    sequence_document = db["counters"].find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        return_document=True,
    )
    if sequence_document:
        return sequence_document["sequence_value"]
    else:
        db["counters"].insert_one({"_id": sequence_name, "sequence_value": 1})
        return 1


# Load the SECRET_KEY from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for JWT generation")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenData(BaseModel):
    username: str
    roles: list[str]

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create an access token with the given data and expiration time.

    Args:
        data (dict): The data to include in the token.
        expires_delta (Optional[timedelta]): The expiration time of the token. If None, uses the default.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    """
    Verify the token and return the token data if valid.

    Args:
        token (str): The JWT token to verify.

    Returns:
        TokenData: The data decoded from the token.

    Raises:
        JWTError: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        roles: list[str] = payload.get("roles", [])
        if username is None:
            raise JWTError("Token does not contain a username.")
        token_data = TokenData(username=username, roles=roles)
    except JWTError as e:
        raise JWTError(f"Could not validate credentials: {e}")
    return token_data
