from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_get_recipients(self, message, msg_vals, **kwargs):
        """
        Ensure archived recipients are included for manual email sends.
        """
        # Get normal recipients first
        recipients = super()._notify_get_recipients(message, msg_vals, **kwargs)
        
        # Check if this is a manual email send (invoice or sales order)
        is_manual_email = (
            self.env.context.get("force_email") or  # Invoice wizard
            self.env.context.get("mark_invoice_as_sent") or  # Invoice wizard
            self.env.context.get("mail_notify_force") or  # Manual compose
            self.env.context.get("default_composition_mode") == "comment"  # Email composer
        )
        
        # If manual email AND message has partner_ids, ensure they're in recipients
        if is_manual_email and hasattr(message, 'partner_ids') and message.partner_ids:
            for partner in message.partner_ids:
                # Check if partner is already in recipients
                partner_found = False
                for recipient in recipients:
                    if recipient.get('partner_id') == partner.id:
                        partner_found = True
                        # Ensure email notification is enabled
                        if recipient.get('notif') != 'email':
                            recipient['notif'] = 'email'
                        break
                
                # If partner not found, add them (even if archived!)
                if not partner_found and partner.email:
                    recipients.append({
                        'id': partner.id,
                        'partner_id': partner.id,
                        'email': partner.email,
                        'name': partner.name,
                        'notif': 'email',  # Force email
                        'lang': partner.lang or 'en_US',
                        'type': 'customer',
                        'is_follower': False,
                        'groups': [],
                        'notifications': [],
                    })
        
        return recipients