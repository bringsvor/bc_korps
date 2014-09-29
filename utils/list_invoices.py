#!/usr/bin/env python


import oerplib

oerp = oerplib.OERP('erp.bringsvor.com', protocol='xmlrpc', port=80)
user = oerp.login('admin', 'Hebekk1406', 'hebekk7')

invoices = oerp.get('account.invoice')
print "I", invoices
for n in invoices.search([]):
	nn = invoices.read(n, ['ref', 'amount_total', 'partner_id'])
	print nn

