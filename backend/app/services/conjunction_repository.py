"""Persistence operations for conjunction scan results."""

from typing import Sequence

from sqlalchemy import select

from app.database import SessionLocal
from app.models.conjunction import Conjunction
from app.models.schemas import ConjunctionAlert


def save_conjunction_alerts(alerts: Sequence[ConjunctionAlert]) -> None:
    """Store all alerts from a completed scan in one transaction."""
    if not alerts:
        return

    with SessionLocal.begin() as session:
        session.add_all(
            [
                Conjunction(
                    id=alert.id,
                    sat1_id=alert.sat1_id,
                    sat1_name=alert.sat1_name,
                    sat2_id=alert.sat2_id,
                    sat2_name=alert.sat2_name,
                    tca_utc=alert.tca_utc,
                    miss_distance_km=alert.miss_distance_km,
                    relative_velocity_km_s=alert.relative_velocity_km_s,
                    risk_score=alert.risk_score,
                    risk_level=alert.risk_level,
                )
                for alert in alerts
            ]
        )


def list_recent_conjunction_alerts(limit: int) -> list[ConjunctionAlert]:
    """Return the newest persisted conjunction alerts."""
    statement = select(Conjunction).order_by(Conjunction.created_at.desc()).limit(limit)

    with SessionLocal() as session:
        records = session.scalars(statement).all()

    return [
        ConjunctionAlert(
            id=record.id,
            sat1_id=record.sat1_id,
            sat1_name=record.sat1_name,
            sat2_id=record.sat2_id,
            sat2_name=record.sat2_name,
            tca_utc=record.tca_utc,
            miss_distance_km=record.miss_distance_km,
            relative_velocity_km_s=record.relative_velocity_km_s,
            risk_score=record.risk_score,
            risk_level=record.risk_level,
        )
        for record in records
    ]
