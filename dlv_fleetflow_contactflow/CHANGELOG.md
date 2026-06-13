# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-14

### Added
- Initial release.
- `GET /fleetflow/contactflow/drivers` endpoint returning active trip drivers as JSON contacts.
- Bearer API key authentication via Odoo native API keys (`res.users.apikeys`, `rpc` scope).
- Optional `location` query parameter to filter drivers on `location_id.name`.
