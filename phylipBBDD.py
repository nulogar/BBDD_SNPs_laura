#!/usr/bin/python
"""
Para obtener archivo .phy de entrada para RAxML. Se necesita archivo con las rutas a todas las cepas a incluir y la BBDD de SNPs generada con exactamente esas cepas
"""

import sys, getopt, os.path


# Informacion de ayuda de uso del script  
def help() :  
	"""Ayuda sobre opciones del script en linea de comandos""" 
	print "Ayuda:"
	print "Para obtener archivo .phy de entrada para RAxML a partir de las rutas a las cepas a incluir y BBDD de SNPs de exactamente esas cepas." 
	print "usage:",sys.argv[0], "[options]"  
	print " -h this message."
	print " -r paths file. Archivo con las rutas de las cepas a incluir."
	print " -b database file. Archivo de la BBDD de SNPs. Generada con todas las cepas a incluir y ninguna mas."  
	print " -a ancestor. Si se activa se incluye una cepa ancestro (sin SNPs)"
	print " -o output file. Archivo de salida .phy."


# Definir las opciones posibles, y cuales de ellas llevan argumento(:)
try:
	opts, args = getopt.getopt(sys.argv[1:],"hr:b:ao:")
except getopt.GetoptError as err:
# Imprimir ayuda y salir si hay algun error o argumento incorrecto
	print str(err)
	help()
	sys.exit(2)


rutasfile = ''
BDfile = ''
outfile = ''
a=0

for opt, arg in opts:
	if opt == '-h':
		help()
		sys.exit()
	elif opt in ("-r"):
		rutasfile = arg
	elif opt in ("-b"):
		BDfile = arg
	elif opt in ("-a"):
		a = 1
	elif opt in ("-o"):
		outfile = arg
	else:  
		assert False, "unhandled option"




try:
	rutas = open(rutasfile)
except IOError:
	print("%s does not exist!!" % rutasfile)
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



#Funcion que realiza la comparacion de SNPs del archivo de la cepa con todos los de la BBDD e imprime su linea de presencia/ausencia en el archivo de salida. Se invoca con la ruta del archivo cepa
def comparar(cepaFile):
	try:
		cepa = open(cepaFile)
	except IOError:
		print("%s does not exist!!" % cepaFile)
		help()
		sys.exit(2)

	#Extraer los datos de los SNPs de la cepa
	ref=set()
	line=cepa.readline()
	for line in cepa:
		line=line.rstrip()
#		print line
		words=line.split()
#		print words[0]
		ref.add(int(words[0]))
	cepa.close()

	#Imprimir el nombre de la cepa seguido de la presencia/ausencia de los SNPs
	output.write(cepaFile+"\t")
	for i in bbdd:
		if i in ref:
			output.write("1")
		else:
			output.write("0")
	output.write("\n")




#Extraer los SNPs de la BBDD
bbdd = []
for line in BD:
	line=line.rstrip()
	bbdd.append(int(line))
BD.close()

#print bbdd

#Extraer las lineas de las rutas de las cepas
rutasList = rutas.readlines()
rutas.close()

#Generar la cabecera del archivo .phy de salida, teniendo en cuenta si se va a incluir o no ancestro
if a==1:
	output.write(str(len(rutasList)+1)+" "+str(len(bbdd))+"\n")
else:
	output.write(str(len(rutasList))+" "+str(len(bbdd))+"\n")

#Si se activa el argumento "a", generar la linea del ancestro, todo 0s
if a==1:
	output.write("ancestor"+"\t")
	for i in range(len(bbdd)):
		output.write("0")
	output.write("\n")

#Realizar la comparacion de SNPs de todas las cepas contra la bbdd e imprimir su presencia/ausencia en el archivo de salida
for i in rutasList:
	comparar(i.rstrip())

output.close()

print ("Snps en BBDD: "+str(len(bbdd)))
print ("Cepas en BBDD: "+str(len(rutasList)))
if a==1:
	print("Ancestro incluido en archivo de salida")
