#!/usr/bin/env python
import oerplib

import parse_members

#oerp = oerplib.OERP('erp.bringsvor.com', protocol='xmlrpc', port=8079)
oerp = oerplib.OERP('localhost', protocol='xmlrpc', port=8069)

print oerp.db.list()

user = oerp.login('admin', 'Hebekk1406', 'hebekk')
print user.name
print user.company_id.name
print '----------------------'

cat = oerp.execute('res.partner.category', 'search', [])
p = oerp.execute('res.partner.category', 'read', cat, ['complete_name'])
categories = {}

for pp in p:
	compl = pp['complete_name'].split('/')[-1].strip()
	categories[compl] = pp['id']

create = True
print categories
partner = oerp.get('res.partner')

headings, members = parse_members.parse()
for member in parse_members.get_members(headings, members):
	# category_id
	print "MEMBER", member
	m = categories[member['category_id']]
	print m
	member['category_id'] = [m]
	if create:
		ppp = oerp.execute('res.partner', 'create', member)
		print ppp
	else:
		id1 = oerp.execute('res.partner', 'search', [('name', '=', member['name'])])
		print "ID", id1, member['name'], m

		partner.write(id1, {'category_id' : (0, m)})


		sjekk = partner.read(id1, ['category_id'])
		print "SJEKK", sjekk
		#id2 = oerp.execute('res.partner', 'write', id1, 'category_id', m)
		#print "ID2", id2
