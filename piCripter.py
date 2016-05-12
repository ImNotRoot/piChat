#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands
import os
from time import time
import sys

ordenLetras=""

def printHelp():
	print "Modo de empleo: piCripter.py [OPCIÓN]... [FICHERO]...\n"
	print "-c, --crypt          Encripta un texto"
	print "-cf, --cryptFile     Encripta un archivo"
	print "-d, --decrypt        Desencripta un texto"
	print "-df, --decryptFile   Desencripta un archivo"
	print "-h, --help           Muestra esta información\n"
	print "Ejemplo de encriptación de texto:"
	print "python2 piCripter.py -c \"texto a encriptar con piCripter\" \"nombreArchivoResultante\"\n"
	print "Ejemplo de encriptación de un archivo:"
	print "python2 piCripter.py -cf \"archivo.pdf\" \"nombreArchivoAEncriptar\"\n"
	print "Ejemplo de desencriptación de texto:"
	print "python2 piCripter.py -d \"nombreArchivo.pi\" \"llamePrivada.ppk\"\n"
	print "Ejemplo de desencriptación de un archivo:"
	print "python2 piCripter.py -df \"nombreArchivo.pi\" \"llamePrivada.ppk\"\n"

def getTerminalSize():
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])

'''def progress(c,total,porcen):
	column,row=getTerminalSize()
	porcenew=(c*column)/total
	bandera=porcen!=porcenew
	if bandera==True:
		porcen=porcenew
	for f in range(barras):
		sys.stdout.write("-")
	return porcen'''

def getPi(dec):
	piVar=commands.getoutput("./pi "+str(dec))
	piVar=piVar[:len(piVar)-2]
	return piVar

def debugText(texto):
	depurado=""
	for c in texto:
		if(c not in depurado):
			depurado=depurado+c

	return depurado

def getNumber(texto):
	array=[]
	for c in texto:
		array.append(c)
	return array

def getNumArray(array,texto):
	numeros=""
	global ordenLetras
	porcen=-1
	for c in range(len(texto)):
		pos=array.index(texto[c])
		numeros=numeros+str(pos)
		ordenLetras=ordenLetras+str(len(str(pos)))
	return numeros

def dividir(texto,num):
	flag=True
	array=[]
	temp=""
	cont=0
	while(flag):
		for f in range(num):
			if(cont<len(texto)):
				temp=temp+texto[cont]
				cont=cont+1
			else:
				flag=False
		array.append(temp)
		temp=""
	for c in range(len(array)):
		if(array[c]==""):
			array.pop(c)
	return array

def crypt(texto,nomFile,tipo):
	extension=".pi"
	tiempo=time()
	if(tipo):
		nomFile=texto
		try:
			texto=open(texto,"rw")
			texto=texto.read()
		except:
			return 202
	clave=""
	gpk=""
	numCant=""
	cont=10
	array = getNumber(debugText(texto))
	numero = getNumArray(array,texto)
	palabras=dividir(numero,5)
	print palabras
	piVar=getPi(cont)
	for c in range(len(palabras)):
		flag = True
		while (flag):
			if(palabras[c] in piVar):
				flag = False
				print palabras[c]
				print piVar
				clave=clave+str(piVar.find(palabras[c]))+"#"
				
			else:
				cont=cont*10
				piVar=getPi(cont)
	for c in range(len(array)):
		flag=True
		while(flag):
			if(str(ord(array[c])) in piVar):
				flag=False
				gpk=gpk+str(piVar.find(str(ord(array[c]))))+"-"
				numCant=numCant+str(len(str(ord(array[c]))))+"-"
			else:
				cont=cont*10
				piVar=getPi(cont)
	gpk=gpk[:len(gpk)-1]
	clave=clave[:len(clave)-1]
	numCant=numCant[:len(numCant)-1]
	realKey=""
	temp=numCant.split("-")
	temp2=gpk.split("-")
	for c in range(len(temp)):
		realKey=realKey+temp[c]+"-"+temp2[c]+"-"
	realKey=realKey[:len(realKey)-1]
	k=open(nomFile+".ppk","w")
	k.write(realKey)
	k.close()
	f=open(nomFile+extension,"w")
	f.write(clave+"\n")
	f.write(ordenLetras)
	print "Time lapse: "+str(time()-tiempo)+" seg."
	f.close()
	return 0

def decrypt(nomFile,pkey,tipo):
	if(tipo):
		nombFile=nomFile[:nomFile.find(".pi")]
	else:
		nombFile=nomFile[:nomFile.find(".pi")]+".txt"
	tiempo=time()
	f=open(nomFile,"rw")
	g=open(pkey,"rw")
	temp=f.read()
	temp=temp.split("\n")
	temp2=g.read()
	direcciones=temp[0].split("#")
	letras=temp2.split("-")
	maxdir=direcciones[0]
	for c in direcciones:
		if(int(maxdir)<int(c)):
			maxdir=c
	for c in letras:
		if(int(maxdir)<int(c)):
			maxdir=c
	piVar=getPi(int(maxdir)+5)
	numero=""
	for c in direcciones:
		puntero=int(c)
		print puntero
		print len(piVar)
		for c in range(5):
			numero=numero+piVar[puntero+c]
	array=[]
	contTemp=0
	while(contTemp<len(letras)):
		letra=""
		numCont=int(letras[contTemp])
		contTemp=contTemp+1
		dirLetra=int(letras[contTemp])
		contTemp=contTemp+1
		for f in range(numCont):
			letra=letra+piVar[dirLetra]
			dirLetra=dirLetra+1
		array.append(chr(int(letra)))
	print array
	clave=""
	contLetras=0
	print int(numero[contLetras])
	print numero
	print contLetras
	for c in temp[1]:
		if(c=="1"):
			clave=clave+array[int(numero[contLetras])]
			contLetras=contLetras+1
		elif(c=="2"):
			clave=clave+array[int(numero[contLetras]+numero[contLetras+1])]
			contLetras=contLetras+2
		else:
			clave=clave+array[int(numero[contLetras]+numero[contLetras+1]+numero[contLetras+2])]
			contLetras=contLetras+3
	arch=open(nombFile,"w")
	arch.write(clave)
	print "Time lapse: "+str(time()-tiempo)+" seg."
	arch.close()

def main(args):
	if(len(args)>1):
		if(((args[1]=="-c")|(args[1]=="--crypt"))):
			if(len(args)==4):
				crypt(args[2],args[3],False)
			else:
				printHelp()
		elif((args[1]=="-d")|(args[1]=="--decrypt")):
			if(len(args)==4):
				decrypt(args[2],args[3],False)
			else:
				printHelp()
		elif((args[1]=="-cf")|(args[1]=="--cryptFile")):
			if(len(args)==3):
				crypt(args[2],"",True)
			else:
				printHelp()
		elif((args[1]=="-df")|(args[1]=="--decryptFile")):
			if(len(args)==4):
				decrypt(args[2],args[3],True)
			else:
				printHelp()
		else:
			printHelp()
	else:
		printHelp()

if __name__ == '__main__':
	main(sys.argv)
