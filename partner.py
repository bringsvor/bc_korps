#from osv import osv, fields
from openerp import models, fields, api

class res_partner(models.Model):
    _inherit = "res.partner"

    # No more discount here, use pricelists for that

    mobile2 = fields.Char('Secondary mobile', size=64)
    join_date = fields.Char('Date joined', size=64)
    #discount = fields.Integer('Discount (%)', default=0)
    instrument = fields.Char('Instrument', size=64)
    email2 = fields.Char('Secondary email', size=240)



