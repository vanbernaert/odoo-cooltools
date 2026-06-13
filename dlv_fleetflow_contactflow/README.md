# dlv_fleetflow_contactflow

## Overview

FleetFlow ContactFlow API exposes the active trip drivers managed by the
`busenco_custom` addon (`trip.driver`) over a token-authenticated HTTP endpoint
that returns JSON contacts. It is designed to feed external systems — such as a
WordPress ContactFlow integration — with an always-current driver contact list,
optionally filtered by office location.

Driver names are stored as a single `name` field on `trip.driver`. The endpoint
splits `trip.driver.name` on the **first space** into `first_name` and
`last_name`:

- `"Jan Peeters"` → `first_name="Jan"`, `last_name="Peeters"`
- `"Jan Van den Berg"` → `first_name="Jan"`, `last_name="Van den Berg"`
- `"Jan"` (no space) → `first_name="Jan"`, `last_name=""`

## Dependencies

- `base`
- `busenco_custom` (provides the `trip.driver` model)

## Endpoint

### URL

```
GET /fleetflow/contactflow/drivers
```

Optional query parameter:

| Param | Description |
|-------|-------------|
| `location` | Filter drivers on `location_id.name` (exact match) |

Example:

```
GET /fleetflow/contactflow/drivers?location=Antwerpen
```

### Authentication

Bearer token using Odoo's **native API keys**.

```
Authorization: Bearer <your_api_key>
```

The key is validated against `res.users.apikeys` with the `rpc` scope. A missing,
malformed, or invalid key returns **401 Unauthorized**.

Create a key in Odoo: **Settings → Users → (select user) → Account Security →
API Keys → New API Key**.

### Response format

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

On error the endpoint returns **500** with:

```json
{ "error": "<message>" }
```

### Field mapping

| JSON field   | Source (`trip.driver`)        | Notes |
|--------------|-------------------------------|-------|
| `id`         | `id`                          | Cast to string |
| `first_name` | `name` (before first space)   | Split on first space |
| `last_name`  | `name` (after first space)    | Remainder after first space; `""` if none |
| `phone`      | `phone_number`                | `""` if empty |
| `mobile`     | `phone_number2`               | `""` if empty |
| `email`      | `email`                       | `""` if empty |

Only drivers with `active = True` are returned, ordered by `name` ascending.

## WordPress setup

1. Store the Odoo base URL and the API key in your WordPress configuration
   (e.g. as constants in `wp-config.php` or via your integration plugin's
   settings), never hard-coded in templates.
2. Make a server-side `GET` request to
   `https://<odoo-host>/fleetflow/contactflow/drivers` with the header
   `Authorization: Bearer <your_api_key>`.
3. Add the `location` query parameter if you only want drivers for a specific
   office location.
4. Parse the `contacts` array from the JSON response and render it through your
   ContactFlow templates.
5. Cache the response (e.g. a transient) to avoid polling Odoo on every page
   load.

## Installation steps

1. Copy the `dlv_fleetflow_contactflow` directory into your Odoo addons path
   (alongside `busenco_custom`).
2. Restart the Odoo server.
3. Enable **Developer Mode** and update the apps list
   (**Apps → Update Apps List**).
4. Search for **FleetFlow ContactFlow API** and click **Install**.
5. Create an API key for the user that should own the feed
   (**Settings → Users → Account Security → API Keys → New API Key**).
6. Test the endpoint:

   ```bash
   curl -H "Authorization: Bearer <your_api_key>" \
     "https://<odoo-host>/fleetflow/contactflow/drivers"
   ```
