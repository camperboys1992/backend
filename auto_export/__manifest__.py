# -*- encoding: utf-8 -*-
{
    'name' : 'Record Auto Export',
    'version' : '10.0',
    'author' : 'Joseph Oladipupo',
    'category' : 'Generic Modules',
    'summary': 'Backups',
    'description': """The Record Auto-Export module enables the user to make configurations for the automatic export of records e.g sales record in the database. The exported record is then mailed to the provided email address in the configuration.

Automatic backup for all such configured databases can then be scheduled as follows:  
                      
1) Go to Settings / Technical / Automation / Scheduled actions.
2) Search the action 'Export scheduler'.
3) Set it active and choose how often you wish to take backups.
""",
    'depends' : ['base', 'mail'],
    'data': [
	  'security/ir.model.access.csv',
      'views/model_export_view.xml',
      'data/export_data.xml',
      'data/mail_data.xml',
    ],
    'auto_install': False,
    'installable': True
}
