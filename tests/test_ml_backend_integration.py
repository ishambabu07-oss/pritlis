import sys
import unittest
import os
from unittest.mock import patch


PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
BACKEND_ROOT = os.path.join(PROJECT_ROOT, "backend")
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, BACKEND_ROOT)

from backend.app.api.routes import health_check
from backend.app.main import startup_event
from backend.app.services.risk_scorer import calculate_conjunction_risk


class RiskScorerIntegrationTest(unittest.TestCase):
    def test_health_does_not_expose_model_path(self):
        response = health_check()

        self.assertEqual(response["status"], "ok")
        self.assertNotIn("model_path", response)

    def test_startup_rejects_missing_risk_model(self):
        with patch("app.main.is_model_loaded", return_value=False):
            with self.assertRaisesRegex(RuntimeError, "Risk model is unavailable"):
                startup_event()

    def test_backend_accepts_pipeline_feature_contract(self):
        score, level = calculate_conjunction_risk(
            miss_distance_km=2.0,
            rel_velocity_km_s=10.0,
            bstar1=0.0001,
            bstar2=0.0001,
        )

        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
        self.assertIn(level, {"LOW", "MEDIUM", "HIGH", "CRITICAL"})
