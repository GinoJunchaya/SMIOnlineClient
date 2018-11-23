from persistent import Persistent
from .Persona import Persona
from .Mensaje import Mensaje
from threading import Thread
import os
os.chdir("..")

class Usuario (Persona, Persistent):
    ''' Clase que corresponde a los datos correpondientes de cada usuario y sus
        acciones
    '''
    def __init__(self, nombre="", apellido="", sexo="", fecha_nacimiento=""):
        Persona.__init__(self, nombre, apellido, sexo, fecha_nacimiento)
        self.nick = ""
        self.online = False
        self.password = ""
        self.historial_mensajes = []
        self.lista_contactos = []

    def enviar_mensaje(self, mensaje, paquete_pickle, comunicacion_conexion):
        ''' Metodo que recibe el objeto mensaje y lo envia a través de la
            conexion al servidor, tambien agrega ese mensaje a su historial
        '''
        comunicacion_conexion.put(paquete_pickle)
        self.historial_mensajes.append(mensaje)

    def recibir_mensajes(self, mensaje):
        ''' Metodo que recibe el mensaje y lo inserta dentro de su historial '''
        self.historial_mensajes.append(mensaje)

    def iniciar_sesion(self, nick, password):
        ''' Cambia el estado del usuario a conectado '''
        self.online = True
        self.nick = nick
        self.password = password

    def cerrar_sesion(self):
        ''' Cambia el estado del usuario a desconectado '''
        self.online = False

    def editar_perfil(self, nuevos_datos):
        ''' Cambia los datos del perfil del usuario '''
        self.nombre = nuevos_datos[0]
        self.apellido = nuevos_datos[1]
        self.sexo = nuevos_datos[2]
        self.fecha_nacimiento = nuevos_datos[3]
        return True

    def ver_perfil(self):
        ''' Retorna los datos personales del usuario '''
        return self

    def mostrar_mensajes(self):
        ''' Retorna el historial de mensajes del usuario '''
        return self.historial_mensajes

    def mostrar_contactos(self):
        ''' Retorna la lista de contactos del usuario '''
        return self.lista_contactos

    def __str__(self):
        ''' toString del usuario '''
        return "Nombre y Apellido: " + self.nombre + " " + self.apellido +\
                "\nSexo: " + self.sexo +\
                "\nFecha de nacimiento: " + self.fecha_nacimiento +\
                "\nNombre de usuario: " + self.nick+\
                "\nOnline: " + str(self.online) + "\n"
