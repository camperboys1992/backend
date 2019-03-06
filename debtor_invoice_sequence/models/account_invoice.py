# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
	_inherit = 'account.invoice'
	
	@api.multi
	def action_invoice_open(self):
		res = super(AccountInvoice, self).action_invoice_open()
		to_do = self.filtered(lambda r: not r.partner_id.debtor_nin)
		for inv in to_do:
			seq = self.env['ir.sequence'].next_by_code('res.partner') or ''
			if seq:
				inv.partner_id.write({
					'debtor_nin': str(seq) 
				})
		return res
	