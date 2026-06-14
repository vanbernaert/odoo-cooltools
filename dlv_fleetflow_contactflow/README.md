# dlv_fleetflow_contactflow

## Overview

`dlv_fleetflow_contactflow` is a generic contact sync feed addon. It provides
token-authenticated JSON endpoints consumed by the WordPress
`dlv-odoo-contactflow` plugin to keep an external contact list in sync with
Odoo.

The **customers** and **suppliers** endpoints (backed by `res.partner`) are
always available. The **drivers** endpoint requires the `busenco_custom` addon
(which provides the `trip.driver` model); when `busenco_custom` is not
installed, the drivers endpoint responds with a 404 JSON error and the FleetFlow
Settings tab shows a warning.

## Dependencies

- `base`
- `base_setup`
- `dlv_fleetflow_base`
- `busenco_custom` *(optional — only needed for the drivers endpoint)*

## Endpoints

| Endpoint | Requires |
|----------|----------|
| `GET /fleetflow/contactflow/customers` | always active |
| `GET /fleetflow/contactflow/suppliers` | always active |
| `GET /fleetflow/contactflow/drivers?location=X` | `busenco_custom` installed |

## Authentication

Bearer token using Odoo's native API keys:

```
Authorization: Bearer <your_api_key>
```

Generate a key via **Settings → Users → (user) → API Keys → New API Key**.

## Response format

`Content-Type: application/json;charset=utf-8`

```json
{
  "contacts": [
    {
      "id": "42",
      "first_name": "Jan",
      "last_name": "Peeters",
      "phone": "+3231234567",
      "mobile": "+32475123456",
      "email": "jan.peeters@example.com"
    }
  ]
}
```

## Name splitting

Contacts expose separate `first_name` / `last_name` fields, derived from a
single source name field:

- **People** (drivers, individual partners): the name is split on the **first
  space** — `"Jan Van den Berg"` → `first_name="Jan"`, `last_name="Van den Berg"`.
- **Companies** (`is_company = True`): `first_name` is empty and `last_name`
  holds the full company name.

## Settings

A **ContactFlow API** tab is available under **Settings → FleetFlow**. It shows
the live status of each endpoint, authentication instructions, and the response
format. When `busenco_custom` is installed the drivers endpoint is reported as
active; otherwise a warning explains how to enable it.

## Installation

1. Install `dlv_fleetflow_base` first (it owns the FleetFlow Settings entry).
2. Install `dlv_fleetflow_contactflow`.
3. *(Optional)* Install `busenco_custom` to enable the drivers endpoint.
4. Create an API key for the user that should own the feed
   (**Settings → Users → API Keys → New API Key**).

## WordPress setup

In the `dlv-odoo-contactflow` WordPress plugin, configure a sync profile with:

- the endpoint URL (e.g. `https://<odoo-host>/fleetflow/contactflow/customers`),
- the Bearer token generated above.

The plugin polls the endpoint and maps the returned `contacts` array into its
ContactFlow records.
