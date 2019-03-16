from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)
	
class FleetVehicle(models.Model):
	_inherit = 'fleet.vehicle.assignation.log'
	
	@api.multi
	def send_att_mail(self):
		for rec in self:
			template = self.env.ref('studio_customization.handover_mail')
			_logger.info('>>>>>>>>>>> %s', template)
			if template:
				attachment = self.env['ir.attachment'].create({
					'datas_fname': 'Driver Log.pdf',
					'name': 'Driver Log',
					'datas': rec.x_studio_field_Ru46t
				})
				_logger.info('>>>>>>>>>>> %s', attachment)
				
				template.write({
					'attachment_ids': [(6, 0, [attachment.id])],
				})
					
				template.send_mail(rec.id, force_send=True)
				#do a clean up
				template.attachment_ids.unlink()
				attachment.unlink()