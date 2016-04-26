#!/usr/bin/env python3
#-.- encoding: utf-8 -.-

import odoorpc
import xlrd,sys,re

oerp = odoorpc.ODOO('nyhebekk', protocol='jsonrpc', port=8069)
#oerp = odoorpc.ODOO('erp.bringsvor.com', protocol='jsonrpc', port=8499)
oerp.login('hebekk', 'admin', 'Hebekk1406')


#medlemsfil = 'Medlemsliste 03.09.2015.xls'
medlemsfil = 'Medlemsliste 01.01.2016.xlsx'
wb = xlrd.open_workbook(medlemsfil)
sh = wb.sheet_by_index(0)
rownames = [x.value for x in sh.row(5)]
rownames = []
for x in sh.row(5):
	name = x.value
	while name in rownames:
		name += '1'
	rownames.append(name)




cat = oerp.env['res.partner.category'].search([])
p = dict([(x['complete_name'], x['id']) for x in oerp.env['res.partner.category'].read(cat, ['complete_name'])])
print('catgeoirs', p)

members = [x['name'] for x in oerp.env['res.partner'].read(
	oerp.env['res.partner'].search([
('membership_state', 'in', ['paid', 'invoiced', 'old', 'waiting']),
('active','=',True),
]), ['name'])]
print("MEM", members)

korps = ['Hovedkorps', 'Aspirant 1', 'Aspirant 2']
instrument = ['Kornett', 'Slagverk', 'Saksofon', u'Fløyte', 
	'Klarinett', 'Baryton', 'Trombone']
needed = korps + instrument

die = False
for c in needed:	
	if not c in p:
		print('Creating %s' % c)
		oerp.env['res.partner.category'].create({'name': c})
		die = True

if die:
	print("Dying. Revive me.")
	sys.exit(0)


klasse_til_dato = {'2' : '2. kl',
                        '3' : '3. kl',
                        '4' : '4. kl',
                        '5' : '5. kl',
                        '6' : '6. kl',
			'7' : '7. kl',
                        '8' : '8. kl',
                        '9' : '9. kl',
			'10' : '10. kl',
                        'VGS' : 'VGS'}


postnr_re = re.compile('(\d{4}) ')


def hent_postnr(postnr):
	if not postnr:
		return '1406 Ski'
	postnr = postnr_re.search(postnr).group(1)
	return postnr

def compare_and_update(model, newdat, olddat):
	print("NEWDAT", newdat.keys())
	info = {}
	for k in newdat.keys():
		if k == 'category_id':
			olddat[k] = [(6, 0, olddat[k])]
		print(k, olddat[k], newdat[k])
		if olddat[k]!=newdat[k]:
			info[k] = newdat[k]

	print("UPDATING", info, olddat['id'])
	if info != {}:
		model.write([olddat['id']], info)

def map_data(d):
	oerp = {}
	print('MAP_DATA', (d['Etternavn'].encode('utf-8')).decode('utf-8'), 'T', type(d['Etternavn']))
	oerp['name'] = ' '.join([d['Fornavn'], d['Etternavn']])
	oerp['street'] = d['Adresse 1']
	oerp['street2'] = d['Adresse 2']
	oerp['city'] = 'Ski'
	oerp['zip'] = hent_postnr(d['Postnr'])
	oerp['email'] = d['Epost']
	oerp['email2'] = d['Epost1']

	for x,y in (('mobile','Telefon'), ('mobile2', 'Telefon1')):
		if not d[y]:
			continue
		if type(d[y])==float:
			tlf = '%d' % d[y]
		else:
			tlf = d[y]

		oerp[x] = tlf

	# Startår
	joined = d[u'Startår']
	print("STARTÅR", joined, type(joined))
	oerp['join_date'] = '01-01-%s' % joined

	# Kl    
	oerp['birthdate'] = d[u'Født'] or klasse_til_dato.get(d['Kl'], '')
	oerp['instrument'] = d['Instrument']
	return oerp

found_members = []
for index in range(6, sh.nrows):
	row = dict(zip(rownames, [x.value for x in sh.row(index)]))
	if not row['Etternavn'] or not row['Instrument'] or row['Korps'].find('Dirigent')!=-1:
		continue
	print(row)
	if type(row['Kl']) == float:
		row['Kl'] = '%d' % row['Kl']
	if type(row[u'Startår']) == float:
		row[u'Startår'] = '%d' % row[u'Startår']

	ins = row['Instrument'].strip()
	if ins.find(',')!=-1:
		ins = ins.split(',')[0]
	orps = row['Korps'].strip()
	if orps == 'Aspirant':
		orps = 'Aspirant 1'
	
	assert orps in korps, 'Missing %s' % row['Korps']
	assert ins in instrument, 'Missing %s' % row['Instrument']
	categ1 = p[orps]
	categ2 = p[ins]
	print("CATEGS", categ1, categ2)
	dat = map_data(row)
	dat['category_id'] = [(6, 0, [categ1, categ2])]
	print('DAT', dat)
	thename = dat['name'] # bytes(dat['name'], 'utf-8')
	print('CREAT', not (thename in members), 'NAME', thename)
	print(thename, 'ALLE', members )
	found_members.append(thename)

	if not dat['name'] in members:
		oerp.env['res.partner'].create(dat)
	else:
		cid = oerp.env['res.partner'].search([('name','=',dat['name'])])
		assert len(cid) == 1
		dbdat = oerp.env['res.partner'].read(cid)[0]
		compare_and_update(oerp.env['res.partner'], dat, dbdat)

print('MISSING', set(members).difference(found_members))

sys.exit(0)



oerp = odoorpc.ODOO('erp.bringsvor.com', protocol='jsonrpc', port=8499)
#oerp = oerplib.OERP('erp.bringsvor.com', protocol='xmlrpc', port=8099)
#oerp = oerplib.OERP('localhost', protocol='xmlrpc', port=8069)

print(oerp.db.list())

user = oerp.login('hebekk9', 'admin', 'Hebekk1406')
#user = oerp.login('admin', 'Hebekk1406', 'hebekk8')
#user = oerp.login('admin', 'admin', 'korps')
print('%s ----------------------' % user)

cat = oerp.execute('res.partner.category', 'search', [])
p = oerp.execute('res.partner.category', 'read', cat, ['complete_name'])
categories = {}

for pp in p:
	compl = pp['complete_name'].split('/')[-1].strip()
	categories[compl] = pp['id']

create = False
print(categories)
partner = oerp.env['res.partner']

headings, members = parse_members.parse()
for member in parse_members.get_members(headings, members):
	# category_id
	print("MEMBER", member)
	m = categories[member['category_id']]
	print(m)
	member['category_id'] = [m]
	if create:
		ppp = oerp.execute('res.partner', 'create', member)
		print(ppp)
	else:
		id1 = oerp.execute('res.partner', 'search', [('name', '=', member['name'])])
		print("ID", id1, member['name'], m)

		partner.write(id1, {'category_id' : [(4, m)]})


		sjekk = partner.read(id1, ['category_id'])
		print("SJEKK", sjekk)
		#id2 = oerp.execute('res.partner', 'write', id1, 'category_id', m)
		#print "ID2", id2
