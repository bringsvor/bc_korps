__author__ = 'tbri'


import time
from report import report_sxw
from osv import osv

class report_webkit_html(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_webkit_html, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr':cr,
            'uid': uid,
        })

report_sxw.report_sxw('report.webkitaccount.korps.invoice',
                       'account.invoice',
                       'korps/report/report_webkit_html.mako',
                       #'addons/report_webkit_sample/report/report_webkit_html.mako',
                       parser=report_webkit_html)

