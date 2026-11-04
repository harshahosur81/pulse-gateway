<!-- generated-from: sha256:74cc187eb1aa9d57 -->
<!-- shim-body-sha256: sha256:3a703da8103d47cd -->
# Generated shim for pulse-gateway (metabrain:pulse-platform)

Do not edit by hand; edit `CONTEXT.md` and re-run `metabrain init --brain`.

# CONTEXT — pulse-gateway

`pulse-gateway` is the HTTP/JSON event ingestion service for the Pulse observability platform.

## Responsibilities
- Validate incoming telemetry event payloads (`event_id`, `source`, `metric`, `value`, `timestamp`, `tags`).
- Normalize and batch valid events according to the `telemetry-event` contract (`v1` and `v2`).
- Reject malformed payloads with structured error codes.
