#!/usr/bin/python
"""
"""

import sys, getopt




# Definir las opciones posibles, y cuales de ellas llevan argumento(:)
try:
	opts, args = getopt.getopt(sys.argv[1:],"i:b:o:")
except getopt.GetoptError as err:
# Imprimir ayuda y salir si hay algun error o argumento incorrecto
	print str(err)
	help()
	sys.exit(2)

infile = ''
BDfile = ''
outfile = ''

for opt, arg in opts:
#	if opt == '-h':
#		help()
#		sys.exit()
	if opt in ("-i"):
		infile = arg
	elif opt in ("-b"):
		BDfile = arg
	elif opt in ("-o"):
		outfile = arg
	else:  
		assert False, "unhandled option"

print 'Input file is ',infile
print 'Database file is ',BDfile
print 'Output file is ',outfile


try:
	txt = open(infile)
except IOError:
	print("%s does not exist!!" % infile)
	help()
	sys.exit(2)

try:
	BD = open(BDfile)
except IOError:
	print("%s does not exist!!" % BDfile)
	help()
	sys.exit(2)

try:
	output = open(outfile,'w')
except IOError:
	print("File %s cannot be created!!" % outfile)
	help()
	sys.exit(2)


query=set()
line=txt.readline()
for line in txt:
	line=line.rstrip()
#	print line
	words=line.split()
#	print words[0]
	query.add(int(words[0]))
txt.close()



ref=set()
line=BD.readline()
for line in BD:
	line=line.rstrip()
#	print line
	words=line.split()
#	print words[0]
	ref.add(int(words[0]))
BD.close()

print query
print ref

a=len(query.difference(ref))
b=len(ref.difference(query))

if a+b <= 13:
	posIntersec= list(query.intersection(ref))
	posQuery= list(query.difference(ref))
	posRef= list(ref.difference(query))

	posIntersec.sort()
	posQuery.sort()
	posRef.sort()

	output.write("SNPs comunes: "+ str(len(posIntersec)) +"\n")
	output.write("SNPs diferenciales: "+ str(a+b) +"\n")
	output.write("SNPs solo en query: "+ str(a) +"\n")
	output.write("SNPs solo en reference: "+ str(b) +"\n")
	output.write("\n")
	output.write("Lista de SNPs solo en query:\n")
	for i in posQuery:
		output.write(str(i)+"\n")
	output.write("\n")
	output.write("Lista de SNPs solo en reference:\n")
	for i in posRef:
		output.write(str(i)+"\n")
	output.write("\n")
	output.write("Lista de SNPs comunes:\n")
	for i in posIntersec:
		output.write(str(i)+"\n")

print posIntersec
print posQuery
print posRef

output.close()
