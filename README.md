# pulse-gateway

HTTP/JSON telemetry event ingestion package for the Pulse observability platform.

## Overview

`pulse-gateway` validates and normalizes incoming telemetry events against the `telemetry-event` v1 contract before forwarding accepted batches to downstream consumers.

## Modules

- `pulse_gateway/ingest.py`: Implements `validate_event` and `ingest_batch`.
- `tests/test_ingest.py`: Unit test suite covering event validation and batch ingestion.

## Testing

Run the test suite from the repository root:

```bash
python3 -m unittest discover -s tests -t . -v
```
