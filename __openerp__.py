# -*- coding: utf-8 -*-

{
    'name' : 'BC Korps',
    'version' : '1.0',
    'category' :  'Association',
    'description' : """
    BC Korps

    An extension to the Membership module.
    """,
    'depends' : [
        #'report_webkit',
        'membership',
        'board',
        'base'
    ],
    'data' : ['views/partner_view.xml',
              'views/korps_view.xml',
              'views/korps_view2.xml',
         #     'report/korps_reports.xml'
	 ],
    'auto_install':False, # Install automatically
    'installable':True,   # Visible in module list
}
