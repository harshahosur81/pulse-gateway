"""Telemetry event validation and batch ingestion for pulse-gateway."""

from typing import Any

REQUIRED_FIELDS = ("event_id", "source", "metric", "value", "timestamp")
STRING_FIELDS = ("event_id", "source", "metric", "timestamp")


def validate_event(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize a telemetry event against telemetry-event v1.

    Args:
        payload: Raw event dictionary containing telemetry fields.

    Returns:
        Normalized telemetry event dictionary.

    Raises:
        ValueError: If required fields are missing or field types are invalid.
    """
    if not isinstance(payload, dict):
        raise ValueError("Event payload must be a dict")

    for field in REQUIRED_FIELDS:
        if field not in payload or payload[field] is None:
            raise ValueError(f"Missing required field: '{field}'")

    normalized: dict[str, Any] = {}
    for field in STRING_FIELDS:
        raw_val = payload[field]
        if not isinstance(raw_val, str):
            raise ValueError(f"Field '{field}' must be a str")
        cleaned = raw_val.strip()
        if not cleaned:
            raise ValueError(f"Field '{field}' must be a non-empty str")
        normalized[field] = cleaned

    raw_value = payload["value"]
    if isinstance(raw_value, bool) or not isinstance(raw_value, (int, float)):
        raise ValueError("Field 'value' must be a float or int")
    normalized["value"] = float(raw_value)

    raw_tags = payload.get("tags")
    if raw_tags is None:
        normalized["tags"] = {}
    else:
        if not isinstance(raw_tags, dict):
            raise ValueError("Field 'tags' must be a dict[str, str]")
        normalized_tags: dict[str, str] = {}
        for key, val in raw_tags.items():
            if not isinstance(key, str) or not isinstance(val, str):
                raise ValueError("Field 'tags' keys and values must be str")
            normalized_tags[key] = val
        normalized["tags"] = normalized_tags

    return normalized


def ingest_batch(events: list[dict[str, Any]]) -> dict[str, list[Any]]:
    """Validate and partition a batch of telemetry events.

    Args:
        events: List of raw telemetry event dictionaries.

    Returns:
        Dictionary with 'accepted' normalized events and 'rejected' error entries.

    Raises:
        ValueError: If events is not a list.
    """
    if not isinstance(events, list):
        raise ValueError("Batch events must be a list")

    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []

    for index, event in enumerate(events):
        try:
            accepted.append(validate_event(event))
        except ValueError as err:
            rejected.append({"index": index, "error": str(err)})

    return {"accepted": accepted, "rejected": rejected}
