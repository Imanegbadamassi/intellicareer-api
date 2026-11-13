from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Certification(Base):
    __tablename__ = "certifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(150))
    issuer: Mapped[str | None] = mapped_column(String(150))
    obtained_date: Mapped[date | None] = mapped_column(Date)

    candidate: Mapped["Candidate"] = relationship(back_populates="certifications")