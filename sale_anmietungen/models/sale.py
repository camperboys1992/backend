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
		
	@api.multi
	def write(self, vals):
		res = super(SaleOrder, self).write(vals)
		for rec in self:
			if vals.get('sale_type') == 'sale':
				x_m = self.env['x_mieter'].search([('x_studio_buchungsnummer','=', rec.id)])
				x_m.unlink()
				
			if vals.get('x_studio_von') and rec.sale_type == 'rental':
				x_m = self.env['x_mieter'].search([('x_studio_buchungsnummer','=', rec.id)])
				if x_m:
					x_m.write({
						'x_studio_beginin_der_reise_1': rec.x_studio_von
					})
				else:
					self.env['x_mieter'].create({
						'x_studio_buchungsnummer': rec.id,
						'x_name': rec.name,
						'x_studio_beginin_der_reise_1': rec.x_studio_von,
						'x_studio_ende_der_reise_1': rec.x_studio_bis
					})
			elif vals.get('x_studio_bis') and rec.sale_type == 'rental':
				x_m = self.env['x_mieter'].search([('x_studio_buchungsnummer','=', rec.id)])
				if x_m:
					x_m.write({
						'x_studio_ende_der_reise_1': rec.x_studio_bis
					})
				else:
					self.env['x_mieter'].create({
						'x_studio_buchungsnummer': rec.id,
						'x_name': rec.name,
						'x_studio_beginin_der_reise_1': rec.x_studio_von,
						'x_studio_ende_der_reise_1': rec.x_studio_bis
					})
		return res
