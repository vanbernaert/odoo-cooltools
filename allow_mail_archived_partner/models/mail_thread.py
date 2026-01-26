import logging
_logger = logging.getLogger(__name__)

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    _logger.info("=== MAILTHREAD CLASS LOADED (allow_mail_archived_partner) ===")

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        """
        Keep the method to avoid TypeError, but keep it simple.
        """
        return super()._notify_thread(message, msg_vals=msg_vals, **kwargs)

    def _notify_get_recipients(self, message, msg_vals, **kwargs):
        """
        Force inclusion of archived partners for manual sends ONLY.
        """
        _logger.error("🔥🔥🔥🔥🔥 MailThread._notify_get_recipients CALLED 🔥🔥🔥🔥🔥")
        
        # CRITICAL: Check if this is a SYSTEM NOTIFICATION
        is_system_message = (
            getattr(message, "message_type", None) == "notification" or
            getattr(message, "author_id", False) and 
            message.author_id == self.env.ref("base.partner_root", raise_if_not_found=False) or
            (msg_vals and msg_vals.get("message_type") == "notification")
        )
        
        if is_system_message:
            _logger.error("🔥 SYSTEM MESSAGE - returning parent result unchanged")
            return super()._notify_get_recipients(message, msg_vals, **kwargs)
        
        # Check if this is a manual send
        is_manual_send = (
            self.env.context.get("mail_notify_force") or
            self.env.context.get("include_archived_partners") or
            self.env.context.get("force_email") or
            self.env.context.get("mark_invoice_as_sent")
        )
        
        _logger.error(f"🔥 Is manual send? {is_manual_send}")
        _logger.error(f"🔥 Message partner_ids: {getattr(message, 'partner_ids', None)}")
        
        # For manual sends, we need to handle archived partners
        if is_manual_send and hasattr(message, 'partner_ids') and message.partner_ids:
            _logger.error("🔥🔥🔥 MANUAL SEND WITH PARTNERS - Handling archived partners 🔥🔥🔥")
            
            # Get the partner IDs from the message
            partner_ids = message.partner_ids.ids
            _logger.error(f"🔥 Message has partners: {partner_ids}")
            
            # Call parent with context that allows archived partners
            recipients = super(
                MailThread,
                self.with_context(
                    active_test=False,
                    include_archived_partners=True,
                    mail_notify_force=True,
                )
            )._notify_get_recipients(message, msg_vals, **kwargs)
            
            # Ensure recipients is always a list
            if recipients is None:
                recipients = []
            
            _logger.error(f"🔥 Number of recipients found: {len(recipients)}")
            
            # If no recipients found, create them manually
            if len(recipients) == 0 and partner_ids:
                _logger.error("🔥 No recipients found, creating manually")
                for partner_id in partner_ids:
                    partner = self.env['res.partner'].with_context(
                        active_test=False
                    ).browse(partner_id)
                    
                    if partner.exists() and partner.email:
                        recipients.append({
                            'id': partner.id,
                            'partner_id': partner.id,
                            'email': partner.email,
                            'name': partner.name,
                            'notif': 'email',  # Force email notification
                            'lang': partner.lang or 'en_US',
                            'type': 'customer',
                            'is_follower': False,
                            'groups': [],
                            'notifications': [],
                        })
                        _logger.error(f"🔥 Created recipient for archived partner: {partner.id} - {partner.email}")
            
            for i, recipient in enumerate(recipients):
                _logger.error(f"🔥 Recipient {i}: partner_id={recipient.get('partner_id')}, "
                        f"notif={recipient.get('notif')}, email={recipient.get('email')}")
            
            return recipients
        
        # For non-manual sends, return parent result
        _logger.error("🔥 Not a manual send - returning parent result")
        return super()._notify_get_recipients(message, msg_vals, **kwargs)

    # Remove _message_post and message_post methods to avoid conflicts
    # Keep only the essential methods