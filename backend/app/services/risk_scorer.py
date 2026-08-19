import math

def calculate_conjunction_risk(miss_distance_km: float, rel_velocity_km_s: float, bstar1: float, bstar2: float) -> tuple[float, str]:
    """
    Calculates a normalized Risk Score [0.0, 1.0] and risk category.
    Incorporates miss distance, closing speed, and atmospheric drag uncertainty.
    """
    # 1. Distance Risk Component (Exponential decay)
    # Objects within 1 km have extreme geometric risk
    dist_factor = math.exp(-0.5 * max(0.0, miss_distance_km - 0.1))
    
    # 2. Velocity Severity Factor
    # Higher relative velocities cause kinetic catastrophic fragmentation
    vel_factor = min(1.0, rel_velocity_km_s / 15.0)
    
    # 3. Drag Uncertainty Penalty
    drag_uncertainty = abs(bstar1) + abs(bstar2)
    drag_factor = 1.0 + min(0.5, drag_uncertainty * 100.0)

    # Composite Probability/Risk Index
    raw_risk = dist_factor * (0.7 + 0.3 * vel_factor) * drag_factor
    risk_score = round(min(1.0, max(0.0, raw_risk)), 4)

    if risk_score >= 0.75 or miss_distance_km < 1.0:
        level = "CRITICAL"
    elif risk_score >= 0.45 or miss_distance_km < 5.0:
        level = "HIGH"
    elif risk_score >= 0.20 or miss_distance_km < 15.0:
        level = "MEDIUM"
    else:
        level = "LOW"

    return risk_score, level