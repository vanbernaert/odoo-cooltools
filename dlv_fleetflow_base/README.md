# dlv_fleetflow_base

## Overview

`dlv_fleetflow_base` is the foundation addon for all FleetFlow-branded addons.
It permanently owns the **FleetFlow** entry in the Odoo Settings sidebar
(Settings → FleetFlow) and provides an empty settings block that feature addons
extend. It contains no models and no business logic — its only job is to give
every `dlv_fleetflow_*` addon a single, shared place to live in Settings.

## How it works

This addon inherits the standard configuration form
(`base_setup.res_config_settings_view_form`) and injects a FleetFlow
`app_settings_block` carrying `data-key="dlv_fleetflow_base"` and an empty
`<notebook/>`. It also creates the **FleetFlow** menu entry and the action that
opens Settings directly on that block.

Feature addons (`dlv_fleetflow_*`) never create their own Settings entry.
Instead, each one adds a tab by inheriting the same base configuration form and
targeting the shared notebook with an xpath:

```
//div[@data-key='dlv_fleetflow_base']//notebook
```

Because every feature addon depends on `dlv_fleetflow_base`, its view is loaded
first, so the notebook exists when the feature addon's xpath runs. The result is
one FleetFlow settings page with one tab per installed feature addon.

## Adding a new FleetFlow addon

1. Add `dlv_fleetflow_base` to your addon's `depends`.
2. Inherit the base configuration form and add a `<page>` to the shared
   notebook:

```xml
<record id="my_addon_config_settings_view_form" model="ir.ui.view">
    <field name="name">res.config.settings.view.form.inherit.my.addon</field>
    <field name="model">res.config.settings</field>
    <field name="inherit_id" ref="base_setup.res_config_settings_view_form"/>
    <field name="arch" type="xml">
        <xpath expr="//div[@data-key='dlv_fleetflow_base']//notebook" position="inside">
            <page string="My Addon">
                <!-- your settings content here -->
            </page>
        </xpath>
    </field>
</record>
```

3. That's it — your tab appears under Settings → FleetFlow alongside the others.

## Dependencies

- `base`
- `base_setup`

## Installation

Install `dlv_fleetflow_base` **first**, before any other `dlv_fleetflow_*`
addon. It is a permanent dependency: do **not** uninstall it while any FleetFlow
feature addon is still active, or those addons will lose their Settings tab and
fail to load their configuration views.
