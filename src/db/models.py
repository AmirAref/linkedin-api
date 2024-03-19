from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, func
from src.db.database import Base


class DownloadRequest(Base):
    __tablename__ = "downloads_requests"

    id = Column("id", Integer, primary_key=True)
    url = Column("url", String)
    data = Column("data", JSON)
    ip_address = Column("ip_address", String)
    created_at = Column("created_at", TIMESTAMP, server_default=func.now())

    def __init__(
        self,
        url: str,
        data: list | dict,
        ip_address: str,
    ):
        self.url = url
        self.data = data
        self.ip_address = ip_address

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.id!r}, {self.url!r}, {self.ip_address!r})"
        )
