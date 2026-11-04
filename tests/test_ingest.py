"""Unit tests for pulse_gateway.ingest."""

import unittest

from pulse_gateway import ingest_batch, validate_event


class TestIngest(unittest.TestCase):
    """Tests for telemetry-event v1 validation and batch ingestion."""

    def setUp(self) -> None:
        self.valid_event = {
            "event_id": "evt-001",
            "source": "api-edge-1",
            "metric": "cpu.utilization",
            "value": 72.5,
            "timestamp": "2026-11-04T00:00:00Z",
        }

    def test_validate_event_minimal_valid(self) -> None:
        result = validate_event(self.valid_event)
        self.assertEqual(result["event_id"], "evt-001")
        self.assertEqual(result["source"], "api-edge-1")
        self.assertEqual(result["metric"], "cpu.utilization")
        self.assertEqual(result["value"], 72.5)
        self.assertEqual(result["timestamp"], "2026-11-04T00:00:00Z")
        self.assertEqual(result["tags"], {})

    def test_validate_event_with_optional_tags_and_int_value(self) -> None:
        payload = {
            **self.valid_event,
            "value": 85,
            "tags": {"region": "us-east1", "env": "prod"},
        }
        result = validate_event(payload)
        self.assertEqual(result["value"], 85.0)
        self.assertIsInstance(result["value"], float)
        self.assertEqual(result["tags"], {"region": "us-east1", "env": "prod"})

    def test_validate_event_missing_required_field(self) -> None:
        for field in ("event_id", "source", "metric", "value", "timestamp"):
            payload = dict(self.valid_event)
            del payload[field]
            with self.assertRaises(ValueError):
                validate_event(payload)

    def test_validate_event_invalid_value_types(self) -> None:
        for bad_value in ("72.5", True, False, None, [1], {"v": 1}):
            payload = {**self.valid_event, "value": bad_value}
            with self.assertRaises(ValueError):
                validate_event(payload)

    def test_validate_event_invalid_tags_types(self) -> None:
        with self.assertRaises(ValueError):
            validate_event({**self.valid_event, "tags": ["env:prod"]})
        with self.assertRaises(ValueError):
            validate_event({**self.valid_event, "tags": {"port": 8080}})

    def test_validate_event_invalid_string_fields(self) -> None:
        with self.assertRaises(ValueError):
            validate_event({**self.valid_event, "event_id": "   "})
        with self.assertRaises(ValueError):
            validate_event({**self.valid_event, "source": 123})

    def test_ingest_batch_mixed_events(self) -> None:
        batch = [
            self.valid_event,
            {"event_id": "evt-002", "source": "db-1"},  # missing metric, value, timestamp
            {
                **self.valid_event,
                "event_id": "evt-003",
                "tags": {"tier": "backend"},
            },
            {
                **self.valid_event,
                "event_id": "evt-004",
                "value": "not-a-number",
            },
        ]
        result = ingest_batch(batch)
        self.assertEqual(len(result["accepted"]), 2)
        self.assertEqual(result["accepted"][0]["event_id"], "evt-001")
        self.assertEqual(result["accepted"][1]["event_id"], "evt-003")
        self.assertEqual(len(result["rejected"]), 2)
        self.assertEqual(result["rejected"][0]["index"], 1)
        self.assertIn("metric", result["rejected"][0]["error"])
        self.assertEqual(result["rejected"][1]["index"], 3)
        self.assertIn("value", result["rejected"][1]["error"])


if __name__ == "__main__":
    unittest.main()
