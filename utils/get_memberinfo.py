#!/usr/bin/env python
#-.- coding: utf-8 -.-
import re
import xlrd
import oerplib


oerp = oerplib.OERP('erp.bringsvor.com', protocol='xmlrpc', port=8079)
user_new = oerp.login('admin', 'Hebekk1406', 'hebekk8')
po = oerp.get('res.partner')
co = oerp.get('res.partner.category')
cat = co.search([])
categories = {}
p = co.read(cat, ['complete_name'])
for c in p:
	categories[c['complete_name'].split('/')[-1].strip()] = c['id']
print "CAT", categories


postnr_re = re.compile('(\d{4}) ')

klasse_til_dato = {'2' : '2. kl',
                        '3' : '3. kl',
                        '4' : '4. kl',
                        '5' : '5. kl',
                        '6' : '6. kl',
                        '8' : '8. kl',
                        '9' : '9. kl',
                        'VGS' : 'VGS'}


def hent_postnr(postnr):
	if not postnr:
		return '1406 Ski'
	postnr = postnr_re.search(postnr).group(1)
	return postnr


def zipit(names, values):
	vv = zip(names, values)
	rv = {}
	for k,v in vv:
		rv[k] = v
	return rv

def make_oerp(heading, row):
	print "MAKE_OERP", heading, row
	oerp = {}
	d = zipit(heading, row)
	print "D", d
	oerp['name'] = ' '.join([d['Fornavn'], d['Etternavn']])
	oerp['street'] = d['Postadresse']
	oerp['city'] = 'Ski'
	oerp['zip'] = hent_postnr(d['Postnr'])
	oerp['email'] = d['Epost'].strip()
	oerp['email2'] = d['Epost1'].strip()
	if d['Telefon']:
		oerp['mobile'] = '%d' % d['Telefon']
	else:
		oerp['mobile'] = None
	if d['Telefon1']:
		oerp['mobile2'] = '%d' % d['Telefon1']
	else:
		oerp['mobile2'] = None

	print "D_CATEG", d['Korps']
	oerp['category_id'] = categories[d['Korps'].strip().replace('Aspirant', 'Aspirantkorps').replace('Aspirant 2', 'Aspirantkorps 2')]

	# Startår
	joined = '%d' % d['Startår'.decode('utf-8')]
	print "STARTÅR", joined
	oerp['join_date'] = '01-01-%s' % joined

	# Kl    
	klasse = d['Kl']
	if type(klasse)==int:
		oerp['birthdate'] = '%d' % d['Kl'] #klasse_til_dato['%d' % d['Kl']]
	else:
		oerp['birthdate'] = klasse

	oerp['instrument'] = d['Instrument']
        print "OERP", oerp     
	return oerp

def massage_heading(values):
	v =  [u'Etternavn', u'Fornavn', u'Korps', u'Postadresse', u'Postnr', u'Instrument', u'Kl', u'Start\xe5r', u'F\xf8dt', u'Epost', u'Epost', u'Foresatt', u'Telefon', u'Foresatt', u'Telefon', u'Individuell musikk instrukt\xf8r', u'epost adresse', u'Tlf']
	assert values == v
	print "HEAD", values
	heading = []
	for v in values:
		if not v in heading:
			heading.append(v)
		elif not v+'1' in heading:
			heading.append(v+'1')
		else:
			assert False
	return heading

def compare_and_update(new_values):
	print "COMPARING", new_values['name'].encode('utf-8')
	new_new = {}
	print "COMP", new_values
	partner_id = po.search([('name','=',new_values['name'])])	
	print "ID", partner_id
	if partner_id==[]:
		print "NEW?", new_values['name']
		new_values['category_id'] = [(4, new_values['category_id'])]
		po.create(new_values)
		return
	partner = po.read(partner_id)[0]
	for k,v in new_values.items():
		if k=='category_id':
			print "CTA", k, v, partner[k][0], v==partner[k][0]
			assert v==partner[k][0]
		else:
			if v!=partner[k]:
				new_new[k] = v
	print "VALUES TO UPDATE", new_new
	po.write(partner_id, new_new)


medlemsfil = 'Medlemsliste 08.03.2015.xls'
wb = xlrd.open_workbook(medlemsfil)
sheet = wb.sheet_by_index(0)
headings = []
for row in range(sheet.nrows):
	values = []
	row_val = sheet.row(row)
	if row_val[0].value.find('informasjon')!=-1:
		print "---------------"
		break
	#print row_val[0], row_val[0].value, row_val[0].ctype, row_val[0].ctype == xlrd.XL_CELL_EMPTY
	if row_val[0].value=='Etternavn':
		headings = massage_heading([x.value for x in row_val])
		continue
	if not headings or row_val[0].ctype==xlrd.XL_CELL_EMPTY:
		continue
	print "ROWW", row_val
	vv = make_oerp(headings, [x.value for x in row_val])
	compare_and_update(vv)
	#vv = zip(headings, [x.value for x in row_val])
	print "VV", vv
