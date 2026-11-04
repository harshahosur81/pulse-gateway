# CONTEXT — pulse-gateway

`pulse-gateway` is the HTTP/JSON event ingestion service for the Pulse observability platform.

## Responsibilities
- Validate incoming telemetry event payloads (`event_id`, `source`, `metric`, `value`, `timestamp`, `tags`).
- Normalize and batch valid events according to the `telemetry-event` contract (`v1` and `v2`).
- Reject malformed payloads with structured error codes.
