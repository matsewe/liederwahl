from typing import Annotated

from fastapi import  HTTPException, Cookie, status, Request
from fastapi.security import SecurityScopes
from jose import JWTError, jwt
from pydantic import ValidationError
import os

#from app.secrets import SECRET_KEY, fake_users_db
# to get a string like this run:
# openssl rand -hex 32

scopes_db = {
    os.environ['ADMIN_EMAIL'] : ["admin"]
}

credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions"
            )

async def get_current_user(
    security_scopes: SecurityScopes, request: Request
    ):
    try:
        username: str = request.headers.get("x-auth-request-user")  # type: ignore
        if username is None:
            raise credentials_exception
        email: str = request.headers.get("x-auth-request-email")  # type: ignore
    except (JWTError, ValidationError):
        raise credentials_exception
    scopes = scopes_db.get(email)
    for scope in security_scopes.scopes:
        if scope not in scopes:
            raise credentials_exception
    return {"sub" : username, "email" : email, "internal_scopes" : scopes}