"""Database module."""

from contextlib import asynccontextmanager, AbstractAsyncContextManager
from typing import Callable
import logging

from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    AsyncSession
)

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    def __init__(self, db_url) -> None:
        logger.debug(f"config url db: {db_url}")
        # current thread uses the connection, if set False connection will shared by multiple threads
        # and could leads to data corruption. User should then serialized writing operation to avoid data corruption
        self._engine: AsyncEngine = create_async_engine(
            url=db_url,
            echo=False,
            connect_args={"check_same_thread": True}
        )
        # scoped_session object: it represents a registry of Session objects. usefull for session management
        # A scoped_session is constructed by calling it, passing it a factory which can create new Session objects.
        # A factory is just something that produces a new object when called, and in the case of Session,
        # the most common factory is the sessionmaker
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                class_=AsyncSession,  # class to use in order to create new Session objects. Defaults to Session.
                autocommit=False,
                autoflush=False,  # autoflush setting to use with newly created Session objects.
                bind=self._engine  # an Engine or other Connectable with
                # which newly created Session objects will be associated.
            )
        )

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # When used as a decorator, a new generator instance is implicitly created on each function call.
    # This allows the otherwise “one-shot” context managers created by asynccontextmanager() to meet the requirement
    # that context managers support multiple invocations in order to be used as decorators.
    #
    # Frameworks expecting callback functions of specific signatures might be type hinted
    # using Callable[[Arg1Type, Arg2Type], ReturnType].
    #
    # It is possible to declare the return type of a callable without specifying
    # the call signature by substituting a literal ellipsis for the list
    # of arguments in the type hint: Callable[..., ReturnType].
    @asynccontextmanager
    async def session(self) -> Callable[..., AbstractAsyncContextManager[AsyncSession]]:
        # we w'll trhis to communicate with our database
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception as exc:
            logger.exception(f"Session rollback because of exception: {exc}")
            await session.rollback()
            raise
        finally:
            await session.close()
