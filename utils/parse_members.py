#!/usr/bin/env python
#-.- encoding: utf-8 -.-

import csv,re

medlemsfil = 'medlemmer_20032014.csv'

def parse():
	f = open(medlemsfil)
	r = csv.reader(f)
	index = 0
	headings = None
	members = None
	category = None
	for row in r:
		if row[0] == 'Hjelpekorps':
			headings.append('category_id')
			return headings, members
		if row[0].find('korps')!=-1:
			category = row[0]

		if members != None:
			if category != None:
				row.append(category)
			members.append(row)
		if index == 8:
			headings = row
			members = []

		index += 1

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

def get_members(headings, members):
	for m in members:
		oerp = {}
		o = zip(headings, m)		
		d = {}
		for k,v in o:
			d[k] = v
		if not d['Etternavn'] or d['Etternavn']=='Etternavn' \
		or d['Etternavn'] == 'Aspirantkorps' or d['Etternavn'] == 'Juniorkorps':
			continue
		"""
		
{'Etternavn': 'Refsdal', 'Postnr': '1400 Ski', 'Postadresse': 'Lysneveien 8 A', 'Telefon': '97544646', 'Kl': '3', 'Instrument': 'Slagverk', 'Start\xc3\xa5r': '2012', 'Fornavn': 'Adrian Normann', 'Epost': 'mona@refsdal.org'}
		"""
		oerp['name'] = ' '.join([d['Fornavn'], d['Etternavn']])
		oerp['street'] = d['Postadresse']
		oerp['city'] = 'Ski'
		oerp['zip'] = hent_postnr(d['Postnr'])
		#oerp['email'] = d['Epost']
		epost = d['Epost'].split('/')
		oerp['email'] = epost[0]
		if len(epost)>1:
			oerp['email2'] = epost[1]

		tlf = d['Telefon'].split('/')
		print "TLF", d['Telefon'], tlf, d['Telefon'].split('/')

		oerp['mobile'] = tlf[0]
		if len(tlf)>1:
			oerp['mobile2'] = tlf[1]
		oerp['category_id'] = d['category_id']

		# Startår
		joined = d['Startår']
		print "STARTÅR", joined
		oerp['join_date'] = '01-01-%s' % joined

		# Kl	
		oerp['birthdate'] = klasse_til_dato[d['Kl']]
		oerp['instrument'] = d['Instrument']
		#print "OERP", oerp	
		yield oerp

if __name__=='__main__':
	headings, members = parse()

	#
	for mem in get_members(headings, members):
		print mem
