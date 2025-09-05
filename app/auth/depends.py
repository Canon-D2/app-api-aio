from fastapi import Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from .config import SECRET_KEY, ALGORITHM
from .permissions import PERMISSIONS
from app.utils.helper import Helper
from .exception import ErrorCode

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expire = payload.get("expire")
        if expire and Helper.get_timestamp() > expire:
            raise ErrorCode.TokenExpired()
        return payload
    except JWTError:
        raise ErrorCode.InvalidToken()

def require_permission():
    async def dependency(request: Request, user: dict = Depends(get_current_user)):
        path = request.url.path
        permission = user.get("permission")

        if not permission:
            raise ErrorCode.PermissionDenied()

        allowed_routes = PERMISSIONS.get(permission, [])
        if path not in allowed_routes:
            raise ErrorCode.PermissionDenied()
        return user
    return Depends(dependency)