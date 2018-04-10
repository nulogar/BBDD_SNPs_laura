#!/usr/bin/python
"""
Para filtrar de un archivo de SNPs detectados aquellos que ya se encuentran en una BBDD propia. En cada linea de la BBDD esta la posicion del SNP. La BBDD se crea con crearBBDD.py.
"""

import sys, getopt

# Informacion de ayuda de uso del script  
def help() :  
	"""Ayuda sobre opciones del script en linea de comandos""" 
	print "Ayuda:"
	print "Para filtrar de un archivo de SNPs detectados aquellos que ya se encuentran en una BBDD propia." 
	print "usage:",sys.argv[0], "[options]"  
	print " -h this message."
	print " -i input file. Archivo de SNPs a filtrar (strain_comparison_result.txt con el resultado de Strain_comparison.R, o .snp.final)."
	print " -b database file. Archivo de BBDD de SNPs."  
	print " -o output file. Archivo de salida con los SNPs filtrados (Mismo formato que el de entrada)."

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
	ref.add(line)

#print ref

BD.close()


count=0
count2=0
for line in txt:
	line=line.rstrip()
#	print line
	words=line.split()
#	print words[0]
	if words[0] not in ref:
		output.write(line+"\n")
		count+=1 #contador de cuantos SNPs pasan
	else:
		count2+=1
		

txt.close()

#print refList


output.close()

print "SNPs filtrados: "+str(count2)
print "SNPs supervivientes: "+str(count-1)
