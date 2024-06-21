from typing import Annotated

from fastapi import  HTTPException, Cookie, status
from fastapi.security import SecurityScopes
from jose import JWTError, jwt
from pydantic import ValidationError
import os

#from app.secrets import SECRET_KEY, fake_users_db
# to get a string like this run:
# openssl rand -hex 32

ALGORITHM = "HS512"
SECRET_KEY = os.environ['SECRET_KEY']

fake_user_db = {
    os.environ['ADMIN_EMAIL'] : {
        "scopes" : ["admin"]
    }
}

credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions"
            )

async def get_current_user(
    security_scopes: SecurityScopes, access_token: Annotated[str, Cookie()] = ""
):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # type: ignore
        if username is None:
            raise credentials_exception
        email: str = payload.get("email")  # type: ignore
    except (JWTError, ValidationError):
        raise credentials_exception
    user = fake_user_db.get(email)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in user["scopes"]:
            raise credentials_exception
    return user | {"token_payload" : payload}