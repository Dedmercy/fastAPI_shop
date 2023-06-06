from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scheme_name="JWT"
)


class AuthenticationHasher:
    @staticmethod
    def get_hashed_password(password: str) -> str:
        """
            Getting hash from password
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, input_password: str) -> bool:
        """
            Verifying the entered password
        """
        return pwd_context.verify(plain_password, input_password)
