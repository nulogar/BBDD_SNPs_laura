#!/usr/bin/python
"""
Para comprobar si un archivo de SNPs (.snp.final o cualquiera con una linea de cabecera y las posiciones de los SNPs en la primera columna) tiene un numero de SNPs diferenciales menor o igual a un cierto valor con respecto a todas las cepas listadas en un archivo de creacion de BBDD de SNPs (el mismo que se le da a crearBBDD.py). En el archivo de salida se detallan en los SNPs diferenciales con respecto a cada cepa que cumple con el cutoff. Se genera un .log con los detalles
"""

import sys, getopt, os.path

# Informacion de ayuda de uso del script  
def help() :  
	"""Ayuda sobre opciones del script en linea de comandos""" 
	print "Ayuda:"
	print "Para comprobar si un archivo de SNPs (.snp.final o similar) tiene un numero de SNPs diferenciales menor o igual a un cierto valor con respecto a todas las cepas listadas en un archivo de creacion de BBDD de SNPs (el mismo que se le da a crearBBDD.py)." 
	print "usage:",sys.argv[0], "[options]"  
	print " -h this message."
	print " -i input file. Archivo de SNPs a comprobar, o .snp.final."
	print " -b database file. Archivo con las rutas de todas las cepas."  
	print " -o output file. Archivo de salida con los detalles de los SNPs diferenciales de las cepas que cumplen con el cutoff."
	print " -c cutoff. Valor numerico con el umbral de SNPs diferenciales (por defecto 12)."


# Definir las opciones posibles, y cuales de ellas llevan argumento(:)
try:
	opts, args = getopt.getopt(sys.argv[1:],"hi:b:o:c:")
except getopt.GetoptError as err:
# Imprimir ayuda y salir si hay algun error o argumento incorrecto
	print str(err)
	help()
	sys.exit(2)

infile = ''
BDfile = ''
outfile = ''
cutoff = 12

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
	elif opt in ("-c"):
		cutoff = int(arg)
	else:  
		assert False, "unhandled option"

if os.path.exists(outfile):
	print "El archivo indicado como salida " + outfile +" existe. Quieres sobreescribirlo? (s/n)"
	respuesta = raw_input()
	if respuesta == 's':
		print "ejecutando"
	elif respuesta == 'si':
		print "ejecutando"
	else:
		print "saliendo"
		sys.exit(2)

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

try:
	log = open(outfile +".log",'w')
except IOError:
	print("File %s cannot be created!!" % outfile +".log")
	help()
	sys.exit(2)

log.write('Input file is '+ infile +"\n")
log.write('Database file is '+ BDfile +"\n")
log.write('Output file is '+ outfile +"\n")
log.write('Cutoff is '+ str(cutoff) +"\n")


#Funcion que realiza la comparacion de SNPs del archivo consulta con uno de las cepas de la BBDD. Se invoca con la ruta del archivo cepa
def comparar(cepaFile):
	try:
		cepa = open(cepaFile)
	except IOError:
		print("%s does not exist!!" % cepaFile)
		help()
		sys.exit(2)

	#Contador de cepas que cumplen el cutoff
	global count

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

#	print query
#	print ref

	#Ver SNPs diferenciales
	a=len(query.difference(ref))
	b=len(ref.difference(query))

	log.write("Diferencias con "+ cepaFile+": " +str(a+b)+"\n")

	#Si el numero de SNPs diferenciales es menor o igual que el cutoff, aumentar el contador de cepas e imprimir los datos de SNPs en el archivo de salida
	if a+b <= cutoff:
		count+=1
		log.write("Cumple con cutoff. Datos de SNPs en "+ outfile +"\n")
		posIntersec= list(query.intersection(ref))
		posQuery= list(query.difference(ref))
		posRef= list(ref.difference(query))

		posIntersec.sort()
		posQuery.sort()
		posRef.sort()

		output.write("Archivo consulta: "+ infile +"\n")
		output.write("Archivo cepa: "+ cepaFile +"\n")
		output.write("SNPs comunes: "+ str(len(posIntersec)) +"\n")
		output.write("SNPs diferenciales: "+ str(a+b) +"\n")
		output.write("SNPs solo en consulta: "+ str(a) +"\n")
		output.write("SNPs solo en cepa: "+ str(b) +"\n")
		output.write("\n")
		output.write("Lista de SNPs solo en consulta:\n")
		for i in posQuery:
			output.write(str(i)+"\n")
		output.write("\n")
		output.write("Lista de SNPs solo en cepa:\n")
		for i in posRef:
			output.write(str(i)+"\n")
#Si queremos que en el archivo de salida aparezcan los SNPs comunes, desmarcar las 4 lineas siguientes
#		output.write("\n")
#		output.write("Lista de SNPs comunes:\n")
#		for i in posIntersec:
#			output.write(str(i)+"\n")
		output.write("\n")
		output.write("\n")
#		print posIntersec
#		print posQuery
#		print posRef




#Extraer los datos de los SNPs del archivo consulta
query=set()
line=txt.readline()
for line in txt:
	line=line.rstrip()
#	print line
	words=line.split()
#	print words[0]
	query.add(int(words[0]))
txt.close()

#Inicializar contador de cepas
count=0

#Realizar la comparacion de SNPs de la consulta contra todas las cepas
for line in BD:
	line=line.rstrip()
	comparar(line)
BD.close()
log.write("Cepas con numero de diferencias menor o igual que "+ str(cutoff)+": " +str(count)+"\n")

output.close()

