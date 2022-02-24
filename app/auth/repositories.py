"""Repositories auth module."""
import logging
from contextlib import AbstractAsyncContextManager
from typing import Callable, Optional


from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select

from app.user.schemas import (
    UserLogin,
    UserCreate
)
from app.user.models import User


logger = logging.getLogger(__name__)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


new_session_factory: Optional[Callable[..., AbstractAsyncContextManager[AsyncSession]]] = None


class AuthRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory
        global new_session_factory
        new_session_factory = session_factory

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # @staticmethod
    # def create_access_token(*, data: dict) -> str:
    #     to_encode = data.copy()
    #     expire = datetime.utcnow() + config.ACCESS_TOKEN_EXPIRE_MINUTES
    #     to_encode.update({"exp": expire})
    #
    #     encoded_jwt = jwt.encode(claims=to_encode, key=config.JWT_SECRET_KEY, algorithm=config.ALGORITHM)
    #     return encoded_jwt

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        async with new_session_factory() as session:
            query = select(User).filter(User.email == email)
            logger.debug(f"query: {query}")
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if not user:
                return None
                # raise HTTPException(status_code=404, detail="User not found")
            return user

    # @staticmethod
    # async def get_current_user(token: str = Depends(oauth2_schema)) -> Optional[User]:
    #     credentials_exception = HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="could not validate credentials",
    #         headers={"WWW-Authenticate": "Bearer"}
    #     )
    #     try:
    #         payload = jwt.decode(token=token, key=config.JWT_SECRET_KEY, algorithms=config.ALGORITHM)
    #         email: str = payload.get("sub")
    #         if email is None:
    #             raise credentials_exception
    #         token_data = TokenData(email=email)
    #     except PyJWTError as err:
    #         raise credentials_exception
    #     user = await AuthRepository.get_user_by_email(token_data.email)
    #     if user is None:
    #         raise credentials_exception
    #     return user

    # @staticmethod
    # async def get_current_active_user(
    #         current_user: User = Depends(get_current_user),
    # ) -> User:
    #     if not current_user.is_active:
    #         raise HTTPException(status_code=400, detail="Inactive user")
    #     return current_user

    @staticmethod
    async def login_user(user_login: UserLogin) -> Optional[User]:
        user = await AuthRepository.get_user_by_email(user_login.email)
        logger.debug(f"user from db: {user}")
        if not user:
            return None
        if not AuthRepository.verify_password(user_login.password, user.hash_password):
            return None
        return user

    async def create_account(self, user_create: UserCreate) -> Optional[User]:
        user = await AuthRepository.get_user_by_email(user_create.email)
        if user:
            return None  # User already exists

        user = User()
        user.email = user_create.email
        user.name = user_create.name
        hashed_password = AuthRepository.get_password_hash(user_create.password)
        user.hash_password = hashed_password

        async with self.session_factory() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)

        return user
