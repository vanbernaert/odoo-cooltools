# Roadmap

Planned extensions to the FleetFlow ContactFlow API addon. Items are grouped by
target release and are subject to change.

## v1.1 — Additional feed types (buses, locations)

- Add `GET /fleetflow/contactflow/buses` exposing `trip.bus` records.
- Add `GET /fleetflow/contactflow/locations` exposing `office.trip.location` records.
- Share the authentication and JSON-response plumbing across all feed types.

## v1.2 — Per-category field selection

- Support a `fields` query parameter so callers receive only the fields they
  request (e.g. `?fields=first_name,last_name,email`).
- Reduce payload size and decouple consumers from the full schema.

## v2.0 — Rename busenco_custom to fleetflow

- Migrate the dependency from `busenco_custom` to the renamed `fleetflow` addon.
- Update model references and the manifest `depends` accordingly.
- Provide a migration path for existing installations.

## Future — Webhook push on driver change

- Emit a webhook to subscribed endpoints when a driver record changes, instead
  of relying on consumers polling the feed.
- Allow registration and management of webhook subscriptions.
