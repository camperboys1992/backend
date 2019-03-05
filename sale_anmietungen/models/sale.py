# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	sale_type = fields.Selection([
		('rental', 'Rental'),
		('sale', 'Sale')
	], default='sale', required=True)
	
	
	@api.model
	def create(self, vals):
		res = super(SaleOrder, self).create(vals)
		if res.sale_type == 'rental':
			self.env['x_mieter'].create({
				'x_studio_buchungsnummer': res.id,
				'x_name': res.name,
				'x_studio_beginin_der_reise_1': res.x_studio_von,
				'x_studio_ende_der_reise_1': res.x_studio_bis
			})
		return res
