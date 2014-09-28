from osv import osv, fields

class res_partner(osv.osv):
    _name = "res.partner"
    _inherit = "res.partner"

    def create_membership_invoice(self, cr, uid, ids, product_id=None, datas=None, context=None):
	orig_amount = datas['amount']
	invoice_ids = []
	for ident in ids:
        	discount = self.browse(cr, uid, ident).discount
		if not discount:
			print "Partner", ident, "has no discount"
			discount = 0.0
	        amount = orig_amount
	        amount -= (amount * discount/100.0)
	        datas['amount'] = amount
        	invo = super(res_partner, self).create_membership_invoice(cr, uid, ident, product_id, datas, context)
		invoice_ids.append(invo)
	return invoice_ids

    _columns = {
         'email2': fields.char('Secondary email', size=240),
         'mobile2' : fields.char('Secondary mobile', size=64),
         'join_date' : fields.char('Date joined', size=64),
         'discount' : fields.integer('Discount (%)'),
         'instrument' : fields.char('Instrument', size=64),
    }



res_partner()
