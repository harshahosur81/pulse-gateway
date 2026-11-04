"""Pulse Gateway telemetry ingestion package."""

from .ingest import ingest_batch, validate_event

__all__ = ["validate_event", "ingest_batch"]
