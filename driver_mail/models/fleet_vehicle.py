from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)
	
class FleetVehicle(models.Model):
	_inherit = 'fleet.vehicle.assignation.log'
	
	@api.multi
	def send_att_mail(self):
		for rec in self:
			template = self.env.ref('studio_customization.handover_mail')
			if template:
				attachment = self.env['ir.attachment'].create({
					'datas_fname': 'Handover Protocol.pdf',
					'name': 'Handover Protocol',
					'datas': rec.x_studio_field_Ru46t
				})
				
				template.write({
					'attachment_ids': [(6, 0, [attachment.id])],
				})
					
				template.send_mail(rec.id, force_send=True)
				
	@api.multi
	def send_return_mail(self):
		for rec in self:
			template = self.env.ref('studio_customization.returnprotocol')
			if template:
				attachment = self.env['ir.attachment'].create({
					'datas_fname': 'Return Protocol.pdf',
					'name': 'Return Protocol',
					'datas': rec.x_studio_return_protocol_1
				})
				
				template.write({
					'attachment_ids': [(6, 0, [attachment.id])],
				})
					
				template.send_mail(rec.id, force_send=True)
