from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Float, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Conjunction(Base):
    """Persisted result of one conjunction scan."""

    __tablename__ = "conjunctions"
    __table_args__ = (
        CheckConstraint("risk_score >= 0.0 AND risk_score <= 1.0", name="conjunctions_risk_score_range"),
    )

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    sat1_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    sat1_name: Mapped[str] = mapped_column(String(255), nullable=False)
    sat2_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    sat2_name: Mapped[str] = mapped_column(String(255), nullable=False)
    tca_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    miss_distance_km: Mapped[float] = mapped_column(Float, nullable=False)
    relative_velocity_km_s: Mapped[float] = mapped_column(Float, nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    risk_level: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
