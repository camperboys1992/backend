# -*- encoding: utf-8 -*-
import base64
import logging
import tempfile

try:
	import csv
except ImportError:
	raise ImportError('This module needs csv in order to automaticly write export to csv (sudo pip install csv)')

from odoo import models, fields, api, tools, _
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)

class ModelExport(models.Model):
	_name = 'model.export'
	_description = 'Model Export'

	name = fields.Char(string="Title", required=True)
	email = fields.Char(required=True)
	is_active = fields.Boolean(default=True, string="Active")
	export_id = fields.Many2one('ir.exports')
	user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user, copy=False)
	
	
	@api.multi
	def run_export(self):
		for rec in self:
			fields = rec.export_id.export_fields.mapped('name')
			all_object = self.env[rec.export_id.resource].search([]).export_data(fields)
			with tempfile.NamedTemporaryFile('w+t') as csv_export:
				writer = csv.writer(csv_export)
				writer.writerow(fields)
				if all_object['datas']:
					writer.writerows(all_object['datas'])
					csv_export.seek(0)
					rec.send_att_mail(csv_export)
					
	def export_auto_data(self):
		rec = self.search([('is_active','=',True)])
		rec.run_export()
		return True
		
	@api.multi
	def send_att_mail(self, csv_data):
		for rec in self:
			template = self.env.ref('auto_export.export_mail_csv')
			c_data = csv_data.read().encode("utf-8")
			if template:
				attachment = self.env['ir.attachment'].create({
					'datas_fname': 'Csv Export Mail.csv',
					'name': 'Csv Export Mail',
					'datas': base64.b64encode(c_data)
				})
				
				template.write({
					'attachment_ids': [(6, 0, [attachment.id])],
				})
					
				template.send_mail(rec.id, force_send=True)