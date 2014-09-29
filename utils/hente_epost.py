#!/usr/bin/env python


import oerplib

import parse_members

oerp = oerplib.OERP('erp.bringsvor.com', protocol='xmlrpc', port=8069)

user = oerp.login('admin', 'Hebekk1406', 'hebekk7')

part = oerp.execute('res.partner', 'search', [])

p = oerp.execute('res.partner', 'read', part, ['email', 'email2'])

for ep in p:
	em1 = ep['email']
	em2 = ep['email2']
	if not em1:
		continue
	if not em2:
		print '%s,'% em1 ,
	else:
		print '%s,%s,'% (em1, em2), 




