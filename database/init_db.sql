CREATE TABLE IF NOT EXISTS conjunctions (
  id UUID PRIMARY KEY,
  sat1_id INTEGER NOT NULL,
  sat1_name VARCHAR(255) NOT NULL,
  sat2_id INTEGER NOT NULL,
  sat2_name VARCHAR(255) NOT NULL,
  tca_utc TIMESTAMPTZ NOT NULL,
  miss_distance_km DOUBLE PRECISION NOT NULL,
  relative_velocity_km_s DOUBLE PRECISION NOT NULL,
  risk_score DOUBLE PRECISION NOT NULL CHECK (risk_score >= 0.0 AND risk_score <= 1.0),
  risk_level VARCHAR(16) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_conjunctions_sat1_id ON conjunctions (sat1_id);
CREATE INDEX IF NOT EXISTS ix_conjunctions_sat2_id ON conjunctions (sat2_id);
CREATE INDEX IF NOT EXISTS ix_conjunctions_tca_utc ON conjunctions (tca_utc);
CREATE INDEX IF NOT EXISTS ix_conjunctions_risk_score ON conjunctions (risk_score);
