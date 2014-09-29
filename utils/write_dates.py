#!/usr/bin/env python


import oerplib

oerp = oerplib.OERP('erp.bringsvor.com', protocol='xmlrpc', port=8099)
user = oerp.login('admin', 'Hebekk1406', 'hebekk8')

invoices = oerp.get('account.invoice')
print "I", invoices
for n in invoices.search([]):
	nn = invoices.read(n, ['ref', 'amount_total', 'partner_id', 'date_invoice'])
	print nn
	nnn = invoices.write(n, {'date_invoice' : '2014-04-24'})
	print nnn
	

