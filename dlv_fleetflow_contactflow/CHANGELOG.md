# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-06-14

### Added
- `GET /fleetflow/contactflow/customers` endpoint (`res.partner`, `customer_rank > 0`, requires phone or mobile).
- `GET /fleetflow/contactflow/suppliers` endpoint (`res.partner`, `supplier_rank > 0`, requires phone or mobile).
- FleetFlow Settings tab (ContactFlow API) showing endpoint status, authentication instructions, and response format.
- Live `busenco_custom` install check — a warning is shown in Settings when the drivers endpoint is unavailable.

### Changed
- Removed `busenco_custom` from hard `depends` — it is now optional at runtime.
- Added `dlv_fleetflow_base` to `depends`.
- Drivers endpoint returns a 404 JSON error when `busenco_custom` is not installed.

## [1.0.0] - 2026-06-14

### Added
- Initial release.
- `GET /fleetflow/contactflow/drivers?location=<location>` endpoint.
- Bearer token authentication via Odoo native API keys.
- Optional `location` filter on the drivers endpoint.
