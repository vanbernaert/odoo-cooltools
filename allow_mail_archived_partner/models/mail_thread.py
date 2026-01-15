from odoo import models, api

class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        """Override to add context before calling parent method"""
        if self._name in ("sale.order", "account.move"):
            # Add context flags for partner searches
            self = self.with_context(
                mail_notification=True, 
                active_test=False,
                include_archived_partners=True
            )
        
        return super()._notify_thread(message, msg_vals=msg_vals, **kwargs)

    def _notify_get_recipients(self, message, msg_vals, **kwargs):
        """Ensure archived partners are included as recipients"""
        # Get recipients normally
        recipients = super()._notify_get_recipients(message, msg_vals, **kwargs)
        
        # Only process for sales orders and invoices
        if self._name in ("sale.order", "account.move"):
            # Ensure context is set
            self = self.with_context(active_test=False)
            
            # Process each recipient
            for recipient in recipients:
                partner_id = recipient.get('partner_id')
                if partner_id:
                    # Re-fetch partner without active filter
                    partner = self.env['res.partner'].with_context(
                        active_test=False
                    ).browse(partner_id)
                    
                    if partner.exists():
                        # Update recipient data
                        recipient.update({
                            'partner': partner,
                            'active_partner': partner,
                            'shared_partner': partner,
                            'is_partner': True,
                        })
                        
                        # Ensure email is set
                        if not recipient.get('email') and partner.email:
                            recipient['email'] = partner.email
                            
                        # Ensure notifications are enabled
                        recipient['notifications'] = 'email'
        
        return recipients

    def _message_get_default_recipients(self):
        """Include archived partners in default recipients"""
        res = super()._message_get_default_recipients()
        
        if self._name in ("sale.order", "account.move"):
            # Re-process with active_test=False
            for record in self:
                if record.id in res:
                    recipients = res[record.id]
                    new_recipients = {}
                    
                    for partner_id, recipient_data in recipients.items():
                        partner = self.env['res.partner'].with_context(
                            active_test=False
                        ).browse(partner_id)
                        
                        if partner.exists():
                            new_recipients[partner_id] = {
                                'partner_id': partner.id,
                                'email': partner.email,
                                'name': partner.name,
                            }
                    
                    res[record.id] = new_recipients
        
        return res