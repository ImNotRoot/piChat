# -*- coding: utf-8 -*-

from Tkinter import *
import string
from ftplib import FTP
import time
import commands
import piCripter

turno = True

def ventanaerror(ventana,mensaje,titulo):
	error=Toplevel(ventana)
	error.geometry("300x80")
	error.title(titulo)
	lerror=Label(error,text=mensaje)
	lerror.pack()
	boton=Button(error,text="aceptar",command=lambda: error.destroy())
	boton.pack()

def validacion(servidor,ventana):
	archivos=servidor.nlst()
	if "usuario_1" not in archivos:
		print 1
		ventana.destroy()
		archivo=open("usuario_1","wr")
		archivo=open("usuario_1","rb")
		servidor.storbinary("STOR usuario_1",archivo)
		inputname=Tk()
		varUser=StringVar()
		inputname.geometry("300x200")
		inputname.title("Nombre de usuario")
		l3=Label(inputname,text="introduce tu usuario")
		l3.pack()
		user=Entry(inputname,textvar=varUser)
		user.pack()
		boton=Button(inputname,text="ingresar",command=lambda:ingresarUsuario(servidor,inputname,user.get(),1))
		boton.pack()
	elif "usuario_2" not in archivos:
		print 2
		ventana.destroy()
		archivo=open("usuario_2","wr")
		archivo=open("usuario_2","rb")
		servidor.storbinary("STOR usuario_2",archivo)
		inputname=Tk()
		varUser=StringVar()
		inputname.geometry("300x200")
		inputname.title("Nombre de usuario")
		l3=Label(inputname,text="introduce tu usuario")
		l3.pack()
		user=Entry(inputname,textvar=varUser)
		user.pack()
		boton=Button(inputname,text="ingresar",command=lambda:ingresarUsuario(servidor,inputname,user.get(),2))
		boton.pack()
	else:
		ventanaerror(ventana,"Ya existen 2 usuarios en este chat","Chat completo")
		servidor.delete("usuario_1")
		servidor.delete("usuario_2")
	
def ingresarUsuario(servidor,ventana,usuario,numUsuario):
	usuario1=""
	usuario2=""
	if numUsuario==1:
		usuario1=usuario
		numUsuario="usuario_"+str(numUsuario)
		servidor.delete(numUsuario)
		archivo=open(numUsuario,"wr")
		archivo.write(usuario)
		archivo.close()
		archivo=open(numUsuario,"rb")
		servidor.storbinary("STOR "+numUsuario,archivo)
		commands.getoutput("rm "+numUsuario)
		archivo.close()
		ventana.destroy()
		usuarios=servidor.nlst()
		print "Esperando un 2do usuario"
		while "usuario_2" not in usuarios:
			usuarios=servidor.nlst()
			time.sleep(2)
		servidor.retrbinary("RETR usuario_2" ,open("usuario_2", 'wb').write)
		usuario2=open("usuario_2","r")
		usuario2=usuario2.read()
		commands.getoutput("rm usuario_2")
		while usuario2=="":
			time.sleep(2)
			servidor.retrbinary("RETR usuario_2" ,open("usuario_2", 'wb').write)
			usuario2=open("usuario_2","r")
			usuario2=usuario2.read()
			commands.getoutput("rm usuario_2")
		print "usuario 1 - "+usuario1
		print "usuario 2 - "+usuario2
		chat(servidor,usuario1,usuario2,1)
	else:
		servidor.retrbinary("RETR usuario_1" ,open("usuario_1", 'wb').write)
		usuario1=open("usuario_1","r")
		usuario1=usuario1.read()
		commands.getoutput("rm usuario_1")
		usuario2=usuario
		numUsuario="usuario_"+str(numUsuario)
		servidor.delete(numUsuario)
		archivo=open(numUsuario,"wr")
		archivo.write(usuario)
		archivo.close()
		archivo=open(numUsuario,"rb")
		servidor.storbinary("STOR "+numUsuario,archivo)
		archivo.close()
		ventana.destroy()
		commands.getoutput("rm "+numUsuario)
		print "usuario 1 - "+usuario1
		print "usuario 2 - "+usuario2
		chat(servidor,usuario1,usuario2,2)
	
def chat(servidor, usuario1, usuario2,tu):
	if tu == 1:
		turno=True
	else:
		turno=False
	ventana=Tk()
	ventana.geometry("500x500")
	ventana.title("Sala de chat abierta")
	varConversacion=StringVar()
	varEntrada=StringVar()
	conversacion=Label(ventana,text=varConversacion.get())
	entrada=Entry(ventana,textvar=varEntrada)
	boton=Button(ventana,text="Enviar",command=lambda:enviar(ventana,servidor,varEntrada.get(),tu,[usuario1,usuario2]))
	boton.pack(side=BOTTOM)
	entrada.pack(side=BOTTOM)
	conversacion.pack(side=TOP)
	if turno == False:
		recibir(servidor,ventana,tu,[usuario1,usuario2])
		turno = True

def enviar(ventana,servidor,mensaje,usuario,nombres):
	print "estoy en el metodo de enviar..."
	print "estoy cifrando"
	l1=Label(ventana,text=nombres[usuario-1]+" - "+mensaje)
	l1.pack(side=TOP)
	comando="./piCripter.py -c '"+mensaje+"' "+"mensaje_"+str(usuario)
	print comando
	commands.getoutput(comando)
	print "termine de cifrar"
	print "estoy abriendo el archivo"
	archivo=open("mensaje_"+str(usuario)+".pi","rb")
	print "ya abri el archivo"
	print "lo estoy subiendo al servidor"
	servidor.storbinary("STOR mensaje_"+str(usuario)+".pi",archivo)
	print "archivo cifrado en el servidor"
	print "abriendo clave"
	archivo=open("mensaje_"+str(usuario)+".ppk","rb")
	print "clave abierta"
	print "estoy subiendo la clave"
	servidor.storbinary("STOR mensaje_"+str(usuario)+".ppk",archivo)
	print "clave en el servidor"
	commands.getoutput("rm mensaje_"+str(usuario)+".pi")
	commands.getoutput("rm mensaje_"+str(usuario)+".ppk")	
	print "sali del metodo de enviar, entrando al de recibir"
	recibir(servidor,ventana,usuario,nombres)

def recibir(servidor,ventana,usuario,nombres):
	print "entre al metodo de recibir"
	if(usuario==1):
		usuario=2
	else:
		usuario=1
	cifrado="mensaje_"+str(usuario)+".pi"
	clave="mensaje_"+str(usuario)+".ppk"
	usuarios=servidor.nlst()
	print cifrado
	print clave
	while (cifrado not in usuarios)&(clave not in usuarios):
			print "Estoy dentro del while..."
			print usuarios
			usuarios=servidor.nlst()
			time.sleep(2)
	print "sali del while"
	print "descargando archivo cifrado"
	servidor.retrbinary('RETR '+cifrado,open(cifrado, 'wb').write)
	print "descargue el archivo cifrado"
	print "descargando clave"
	servidor.retrbinary('RETR '+clave,open(clave, 'wb').write)
	print "descargue clave"
	print "desencriptando texto"
	comando="./piCripter.py -d "+cifrado+" "+clave
	print comando
	commands.getoutput(comando)
	print "texto desencriptado"
	print "abriendo mensaje"
	texto=open("mensaje_"+str(usuario)+".txt","r")
	print "mensaje abierto"
	print "leyendo mensaje"
	texto=texto.read()
	print "mensaje leido"
	print "eliminado residuos"
	print commands.getoutput("rm "+clave)
	print commands.getoutput("rm "+cifrado)
	print commands.getoutput("rm mensaje_"+str(usuario)+".txt")
	print servidor.delete(cifrado)
	print servidor.delete(clave)
	if(usuario==1):
		usuario=2
	else:
		usuario=1
	print "generando nueva label"
	conversacion=Label(ventana,text=nombres[usuario-1]+" - "+texto)
	conversacion.pack(side=TOP)
	print "nueva label generada"
	print "residuos eliminados"
	print "sali del metodo de recibir"

def connect(ip,usuario,contrasena,ventana):
	ftp=FTP()
	bandera=True
	try:
		ftp.connect(ip)
	except:
		bandera=False
		ventanaerror(ventana,"IP incorrecta","Error")
	try:
		ftp.login(usuario,contrasena)
	except: 
		bandera=False
		ventanaerror(ventana,"nombre de usuario o contraseña incorrecta","Error")
	if bandera:
		print "estas conectado"
		validacion(ftp,ventana)

def main():
	login=Tk()
	varUser=StringVar()
	varPass=StringVar()
	varIP=StringVar()
	login.geometry("300x300")
	login.title("inicio del chat")
	entryUser=Entry(login,textvar=varUser)
	entryIP=Entry(login,textvar=varIP)
	entryPass=Entry(login,textvar=varPass)
	varUser.set("")
	varIP.set("187.205.105.91")
	varPass.set("")
	boton=Button(login,text="iniciar",command=lambda: connect(varIP.get(), varUser.get(), varPass.get(), login))
	boton.pack()
	entryUser.pack()
	entryIP.pack()
	entryPass.pack()
	login.mainloop()
	return 0
if __name__ == '__main__':
	 main()
