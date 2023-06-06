from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from jose import jwt

from src.schemas.auth import AccountBase
from src.config import config
from src.auth.auth import oauth2_scheme


class JWTRepository:

    @classmethod
    def create_access_token(cls, account: AccountBase):
        try:

            claims = jsonable_encoder(account)

            return jwt.encode(claims=claims, key=config.jwt_secret, algorithm=config.jwt_algorithm)

        except Exception as e:
            print(e)
            raise

    @classmethod
    def verify_access_token(cls, token: str = Depends(oauth2_scheme)):

        try:
            payload = jwt.decode(token, key=config.jwt_secret)
            return payload
        except Exception:
            raise

    @classmethod
    def check_admin(cls, auth: str = Depends(oauth2_scheme)):
        payload = cls.verify_access_token(auth)
        if payload.get("role_id") == "2":
            return payload
        else:
            raise HTTPException(
                status_code=403,
                detail=f"U have not enough rights"
            )
