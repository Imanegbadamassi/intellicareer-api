from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ContractType, JobOfferStatus, SkillImportance


class JobOffer(Base):
    __tablename__ = "job_offers"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    contract_type: Mapped[ContractType] = mapped_column(Enum(ContractType, name="contract_type"))
    location: Mapped[str | None] = mapped_column(String(150))
    salary_min: Mapped[int | None] = mapped_column(Integer)
    salary_max: Mapped[int | None] = mapped_column(Integer)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status: Mapped[JobOfferStatus] = mapped_column(
        Enum(JobOfferStatus, name="job_offer_status"), default=JobOfferStatus.ACTIVE
    )

    company: Mapped["Company"] = relationship(back_populates="job_offers")
    skills: Mapped[list["JobOfferSkill"]] = relationship(back_populates="job_offer", cascade="all, delete-orphan")


class JobOfferSkill(Base):
    """Compétences d'une offre, avec distinction obligatoire / souhaitée."""

    __tablename__ = "job_offer_skills"
    __table_args__ = (UniqueConstraint("job_offer_id", "skill_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    job_offer_id: Mapped[int] = mapped_column(ForeignKey("job_offers.id", ondelete="CASCADE"))
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))
    importance: Mapped[SkillImportance] = mapped_column(Enum(SkillImportance, name="skill_importance"))

    job_offer: Mapped["JobOffer"] = relationship(back_populates="skills")
    skill: Mapped["Skill"] = relationship()
