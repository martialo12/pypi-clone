"""release models module."""

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    ForeignKey,
    DateTime
)
import sqlalchemy.orm as orm

from app.db.database import Base


class Release(Base):
    __tablename__ = 'releases'

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    major_ver: int = Column(BigInteger, index=True)
    minor_ver: int = Column(BigInteger, index=True)
    build_ver: int = Column(BigInteger, index=True)

    created_date: datetime = Column(DateTime,
                                    default=datetime.now,
                                    index=True)
    comment: str = Column(String)
    url: str = Column(String)
    size: int = Column(BigInteger)

    # Package relationship
    package_id: str = Column(String, ForeignKey("packages.id"))
    packagce = orm.relation('Package')

    @property
    def version_text(self):
        return '{}.{}.{}'.format(self.major_ver, self.minor_ver, self.build_ver)
