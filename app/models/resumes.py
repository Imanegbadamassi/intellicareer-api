from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import SkillCategory, SkillLevel


class Resume(Base):
    """Un candidat peut avoir plusieurs CV."""

    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(150))
    file_url: Mapped[str] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    candidate: Mapped["Candidate"] = relationship(back_populates="resumes")
    skills: Mapped[list["ResumeSkill"]] = relationship(back_populates="resume", cascade="all, delete-orphan")


class Skill(Base):
    """Référentiel normalisé des compétences."""

    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    category: Mapped[SkillCategory] = mapped_column(Enum(SkillCategory, name="skill_category"))


class ResumeSkill(Base):
    __tablename__ = "resume_skills"
    __table_args__ = (UniqueConstraint("resume_id", "skill_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"))
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))
    level: Mapped[SkillLevel | None] = mapped_column(Enum(SkillLevel, name="skill_level"))

    resume: Mapped["Resume"] = relationship(back_populates="skills")
    skill: Mapped["Skill"] = relationship()
