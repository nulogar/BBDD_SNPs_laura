#!/usr/bin/python
"""
Para crear la BBDD inicial con todos los SNPs alguna vez encontrados. Se alimenta de los archivos strain_comparison_result.txt, que se obtienen al ejecutar Strain_comparison.R, o los snp.final. Los SNPs solo apareceran una vez en la BBDD.
"""

import sys, getopt


# Informacion de ayuda de uso del script  
def help() :  
	"""Ayuda sobre opciones del script en linea de comandos""" 
	print "Ayuda:"
	print "Para crear la BBDD inicial con todos los SNPs alguna vez encontrados." 
	print "usage:",sys.argv[0], "[options]"  
	print " -h this message."
	print " -i input file. Archivo con las rutas a los archivos a tratar. Pueden ser snp.final o los strain_comparison_result.txt resultado de Strain_comparison.R. En cada linea una ruta."
	print " -o output file. Base de Datos a crear con los SNPs."

# Definir las opciones posibles, y cuales de ellas llevan argumento(:)
try:
	opts, args = getopt.getopt(sys.argv[1:],"hi:o:")
except getopt.GetoptError as err:
# Imprimir ayuda y salir si hay algun error o argumento incorrecto
	print str(err)
	help()
	sys.exit(2)

infile = ''
outfile = ''

for opt, arg in opts:
	if opt == '-h':
		help()
		sys.exit()
	elif opt in ("-i"):
		infile = arg
	elif opt in ("-o"):
		outfile = arg
	else:  
		assert False, "unhandled option"

print 'Input file is ',infile
print 'Output file is ',outfile


try:
	rutas = open(infile)
except IOError:
	print("%s does not exist!!" % infile)
	help()
	sys.exit(2)

try:
	output = open(outfile,'w')
except IOError:
	print("File %s cannot be created!!" % outfile)
	help()
	sys.exit(2)


pos=set()
count=0

for ruta in rutas:
#	print ruta
	ruta=ruta.rstrip()
        print ruta

	try:
		txt = open(ruta) #archivo .txt con el resultado de Strain_comparison.R
	except IOError:
		print("%s does not exist!!" % ruta)
		help()
		sys.exit(2)


	line=txt.readline()

	for line in txt:
		line=line.rstrip()
#		print line
		line=line.replace(",","\t") #para tratar los casos en que sin querer se han sobreescrito los archivos, guardandolos con el delimitador ","
		words=line.split()
#		print words[0]
		pos.add(int(words[0]))
		count+=1 #contador de cuantas lineas se han tratado, para luego comprobar

	txt.close()


posList=list(pos)
#print len(posList)
posList.sort()
#print posList


for i in posList:
	output.write(str(i)+"\n")

print "Lineas tratadas: "+str(count)

rutas.close()

output.close()


