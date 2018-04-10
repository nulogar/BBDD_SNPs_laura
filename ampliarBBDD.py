#!/usr/bin/python
"""
Para ampliar una BBDD propia con todos los SNPs alguna vez encontrados. Se alimenta de los archivos strain_comparison_result.txt, que se obtienen al ejecutar Strain_comparison.R, o los snp.final. Los SNPs solo apareceran una vez en la BBDD.
"""

import sys, getopt

# Informacion de ayuda de uso del script  
def help() :  
	"""Ayuda sobre opciones del script en linea de comandos""" 
	print "Ayuda:"
	print "Para ampliar una BBDD propia de SNPs alguna vez detectados." 
	print "usage:",sys.argv[0], "[options]"  
	print " -h this message."
	print " -i input file. Archivo con los SNPs a incluir (strain_comparison_result.txt con el resultado de Strain_comparison.R, o .snp.final)."
	print " -b database file. Archivo de BBDD de SNPs a actualizar."  
	print " -o output file. Archivo de salida con la nueva BBDD."

# Definir las opciones posibles, y cuales de ellas llevan argumento(:)
try:
	opts, args = getopt.getopt(sys.argv[1:],"hi:b:o:")
except getopt.GetoptError as err:
# Imprimir ayuda y salir si hay algun error o argumento incorrecto
	print str(err)
	help()
	sys.exit(2)

infile = ''
BDfile = ''
outfile = ''

for opt, arg in opts:
	if opt == '-h':
		help()
		sys.exit()
	elif opt in ("-i"):
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

ref=set()
for line in BD:
	line=line.rstrip()
	ref.add(int(line))

#print ref

BD.close()

line=txt.readline()

count=0
for line in txt:
	line=line.rstrip()
#	print line
	words=line.split()
#	print words[0]
	ref.add(int(words[0]))
	count+=1 #contador de cuantas lineas se han tratado, para luego comprobar

txt.close()

refList=list(ref)
#print len(refList)
refList.sort()

#print refList


for i in refList:
	output.write(str(i)+"\n")


output.close()

print "Lineas tratadas: "+str(count)
