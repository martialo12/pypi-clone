"""release models module."""

from datetime import datetime
from typing import List

from sqlalchemy import (
    Column,
    String,
    DateTime
)
import sqlalchemy.orm as orm

from app.db.database import Base
from app.release.models import Release


class Package(Base):
    __tablename__ = 'packages'

    id: str = Column(String, primary_key=True)
    created_date: datetime = Column(DateTime, default=datetime.now, index=True)
    last_updated: datetime = Column(DateTime, default=datetime.now, index=True)
    summary: str = Column(String, nullable=False)
    description: str = Column(String, nullable=True)

    home_page: str = Column(String)
    docs_url: str = Column(String)
    package_url: str = Column(String)

    author_name: str = Column(String)
    author_email: str = Column(String, index=True)

    license: str = Column(String, index=True)

    # releases relationship
    releases: List[Release] = orm.relation("Release", order_by=[
        Release.major_ver.desc(),
        Release.minor_ver.desc(),
        Release.build_ver.desc(),
    ], back_populates='package')

    def __repr__(self):
        return '<Package {}>'.format(self.id)
