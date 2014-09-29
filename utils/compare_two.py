#!/usr/bin/env python
import oerplib

new_oerp = oerplib.OERP('erp.bringsvor.com', protocol='xmlrpc', port=8099)
old_oerp = oerplib.OERP('erp.bringsvor.com', protocol='xmlrpc', port=80)


user_new = new_oerp.login('admin', 'Hebekk1406', 'hebekk8')
user_old = old_oerp.login('admin', 'Hebekk1406', 'hebekk7')


#partner = oerp.get('res.partner')

names = {'old' : [], 'new' : []}

for name, instance in (('old', old_oerp), ('new', new_oerp)):
	parent = instance.execute('res.partner.category', 'search', [('name', '=', 'Korpsmedlemmer')])
	print parent
	categories = instance.execute('res.partner.category', 'search', [('parent_id', 'in', parent)])
	partner = instance.get('res.partner')
	s = partner.search([('category_id', 'in', categories)])
	print s
	for zz in s:
		ss = partner.read(zz, ['name', 'category_id'])
		names[name].append(ss['name'])

print 'LENGTHS', len(names['old']), len(names['new'])
oldset = set(names['old'])
newset = set(names['new'])
print "DIFF O->N", oldset.difference(newset)
print "DIFF N->O", newset.difference(oldset)
invoices = {'old' : [], 'new' :  []}

for name, instance in (('old', old_oerp), ('new', new_oerp)):
	i = instance.get('account.invoice')
	s = i.search([])
	for invoice in s:
        	nn = i.read(invoice, ['amount_total', 'partner_id'])
		invoicedata = (nn['partner_id'][1], nn['amount_total'])

		invoices[name].append(invoicedata)
		print "NN", nn

oldset = set(invoices['old'])
newset = set(invoices['new'])

print "DIFF O->N", oldset.difference(newset)
