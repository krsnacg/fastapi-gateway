from typing import Annotated

from fastapi import HTTPException, status, Depends, Request
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from .settings import settings
import jwt
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL_PATH)

async def get_current_user_private(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except InvalidTokenError:
        raise credentials_exception
    

async def verify_authentication(request: Request) -> str:
    try:
        token = request.headers.get("Authorization")
        if not token:
            print("Could not find Authorization header in request")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization token not provided",
                # headers={"X-Error": "AuthenticationRequired"}
            )
        token = token.replace("Bearer ", "")  # Remove "Bearer " prefix if present
        print(f"Authorization token provided: {token}")
        return await get_current_user_private(token=token)
        # print("Authentication required for this route")
    except HTTPException as e:
        print(f"Authentication failed: {e.detail}")
        raise e