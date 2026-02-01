def action_send_and_print(self):
    # _logger.error("🔥 ACCOUNT.INVOICE.SEND action_send_and_print CALLED")
    # _logger.error("🔥 Wizard partner_ids: %s", self.partner_ids.ids)

    ctx = dict(self.env.context)

    if self.partner_ids:
        ctx.update(
            {
                # 🔥 THIS is what mail.compose.message actually reads
                "default_partner_ids": [(6, 0, self.partner_ids.ids)],
            }
        )

    return super(
        AccountInvoiceSend,
        self.with_context(
            ctx,
            active_test=False,
            include_archived_partners=True,
            mail_notify_force=True,
            force_email=True,
            mark_invoice_as_sent=True,
        ),
    ).action_send_and_print()
