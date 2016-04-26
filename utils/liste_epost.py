#!/usr/bin/env python


import xlrd
from xlrd import open_workbook, cellname, xldate_as_tuple

fn = 'Medlemsliste 01.01.2016.xlsx'
book2 = open_workbook(fn)


sheets = book2.sheet_names()
sheet = book2.sheet_by_index(0)
#sheet = book2.sheet_by_name(sheetname)
columns = [x.value for x in sheet.row(0)]
print '-------------'
epostar = []
for r in range(1, sheet.nrows):
	rv = sheet.row_values(r)
	rt = sheet.row_types(r)
	epost = rv[11:13]

	print 'EPOSTAR', epost
	for e in epost:
		print 'ep', e
		if e.find('@')!=-1:
			epostar.append(e)

print 'EP'
print ', '.join(set(epostar))

