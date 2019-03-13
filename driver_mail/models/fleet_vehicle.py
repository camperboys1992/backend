from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)
	
class FleetVehicle(models.Model):
	_inherit = 'fleet.vehicle.assignation.log'
	
	@api.multi
	def send_att_mail(self):
		for rec in self:
			template = self.env['mail.template'].search([('name','=','übergabe')], limit=1)
				
			attachment = self.env['ir.attachment'].create({
				'datas_fname': 'Driver Log',
				'name': 'Driver Log',
				'datas': rec.x_studio_field_Ru46t
			})
			
			template.attachment_ids = [(6, 0, [attachment.id])]
				
			template.send_mail(rec.id, force_send=True)			