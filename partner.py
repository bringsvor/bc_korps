#from osv import osv, fields
from openerp import models, fields, api

class res_partner(models.Model):
    #_name = "res.partner"
    _inherit = "res.partner"

    @api.one
    def create_membership_invoice(self, product_id=None, datas=None, context=None):
        orig_amount = datas['amount']
        invoice_ids = []
        amount = orig_amount
        amount -= (amount * self.discount/100.0)
        datas['amount'] = amount
        # cr, uid, ident,
        invo = super(res_partner, self).create_membership_invoice(product_id, datas, context)
        invoice_ids.append(invo)
        return invoice_ids


    mobile2 = fields.Char('Secondary mobile', size=64)
    join_date = fields.Char('Date joined', size=64)
    discount = fields.Integer('Discount (%)', default=0)
    instrument = fields.Char('Instrument', size=64)
    email2 = fields.Char('Secondary email', size=240)



res_partner()
