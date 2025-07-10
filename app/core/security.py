from typing import Annotated

from fastapi import HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from core.settings import settings
import jwt
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL_PATH)

async def get_current_user_private(token: Annotated[str, Depends(oauth2_scheme)]):
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