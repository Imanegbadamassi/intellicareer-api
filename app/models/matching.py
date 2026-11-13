from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ApplicationStatus


class Analysis(Base):
    """Résultat du matching CV + offre.

    Créée AVANT la candidature (simulation) : le candidat voit le score,
    puis peut postuler en réutilisant cette analyse.
    """

    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"), index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"))
    job_offer_id: Mapped[int] = mapped_column(ForeignKey("job_offers.id", ondelete="CASCADE"), index=True)
    overall_score: Mapped[float] = mapped_column(Float)
    required_score: Mapped[float] = mapped_column(Float)
    preferred_score: Mapped[float] = mapped_column(Float)
    missing_skills: Mapped[list | None] = mapped_column(JSONB)
    ai_appreciation: Mapped[str | None] = mapped_column(Text)  # texte destiné au recruteur
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    candidate: Mapped["Candidate"] = relationship(back_populates="analyses")
    resume: Mapped["Resume"] = relationship()
    job_offer: Mapped["JobOffer"] = relationship()
    recommendations: Mapped[list["AnalysisRecommendation"]] = relationship(
        back_populates="analysis", cascade="all, delete-orphan"
    )


class AnalysisRecommendation(Base):
    """Offres alternatives proposées quand le score est bas."""

    __tablename__ = "analysis_recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    analysis_id: Mapped[int] = mapped_column(ForeignKey("analyses.id", ondelete="CASCADE"))
    job_offer_id: Mapped[int] = mapped_column(ForeignKey("job_offers.id", ondelete="CASCADE"))
    compatibility_score: Mapped[float] = mapped_column(Float)

    analysis: Mapped["Analysis"] = relationship(back_populates="recommendations")
    job_offer: Mapped["JobOffer"] = relationship()


class Application(Base):
    """Candidature réelle. Référence une analyse déjà calculée."""

    __tablename__ = "applications"
    __table_args__ = (UniqueConstraint("candidate_id", "job_offer_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"), index=True)
    job_offer_id: Mapped[int] = mapped_column(ForeignKey("job_offers.id", ondelete="CASCADE"), index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"))
    analysis_id: Mapped[int] = mapped_column(ForeignKey("analyses.id"))  # non nullable
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, name="application_status"), default=ApplicationStatus.EN_ATTENTE
    )
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    candidate: Mapped["Candidate"] = relationship(back_populates="applications")
    job_offer: Mapped["JobOffer"] = relationship()
    resume: Mapped["Resume"] = relationship()
    analysis: Mapped["Analysis"] = relationship()
