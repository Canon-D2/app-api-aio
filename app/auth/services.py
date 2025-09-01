from jose import jwt
from app.mongo.base import BaseCRUD
from app.utils.helper import Helper
from app.mongo.engine import engine_aio
from bcrypt import checkpw, gensalt, hashpw

from .config import ACCESS_TOKEN_EXPIRE_DAY, ALGORITHM, REMEMBER_TOKEN_DAY, SECRET_KEY


class AuthServices():
    def __init__(self, crud, service_name: str, owner_type: str = None):
        self.crud = crud
        self.service_name = service_name
        self.owner_type = owner_type

    async def hash_password(self, password):
        return hashpw(password.encode("utf8"), gensalt())

    def check_password(self, user_login_password, password):
        if not checkpw(user_login_password.encode("utf-8"), password):
            return False
        return True

    async def create_access_token(self, data):
        to_encode = data.copy()
        expire_days = (
            REMEMBER_TOKEN_DAY if data.get("remember_me") else ACCESS_TOKEN_EXPIRE_DAY
        )
        expire = Helper.get_future_timestamp(days_to_add=expire_days)
        to_encode.update({"expire": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


auth_crud = BaseCRUD("auth", engine_aio)
auth_services = AuthServices(crud=auth_crud, service_name="auth services")
