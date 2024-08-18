from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKeyConstraint, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB, UUID
import uuid
from typing import Optional, List

from app.db import Base


class WSData(Base):

    __tablename__ = 'ws_data'

    id = mapped_column(UUID(as_uuid=False), default=uuid.uuid4, nullable=False, primary_key=True, index=True)
    workspace_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey('workspaces.id'))
    pid: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False, index=True)
    process_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), default=None)
    form_id: Mapped[str] = mapped_column(UUID(as_uuid=False))
    form_code: Mapped[str] = mapped_column(String, default=None)
    data_: Mapped[dict] = mapped_column(JSONB, default=None)
    comp_data_: Mapped[Optional[dict]] = mapped_column(JSONB, default=None)
    created_by: Mapped[Optional[int]] = mapped_column(Integer)
    modified_by: Mapped[Optional[int]] = mapped_column(Integer)
    created_date: Mapped[Optional[str]] = mapped_column(DateTime(timezone=False), server_default=func.now())
    modified_date: Mapped[Optional[str]] = mapped_column(DateTime, onupdate=func.now())



