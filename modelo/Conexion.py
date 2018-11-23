from threading import Thread
from modelo.Paquete import *
from socket import socket
from Vista import *
from utils import *
import pickle

class Conexion(Thread):
    '''Clase que corresponde a la conexion, es decir a la sesión del
        usuario, el cual debe enviar y recibir paquetes, es decir
        debe comunicarse bilateralmente con el servidor,
        identificamos los paquetes recibidos segun su codigo y lo
        manejamos con un diccionario de funciones las cuales corresponden
        a funciones del servidor, la forma en la cual recibe los datos
        es por partes, ya que para conexiones lentas o historiales de
        usuario muy grandes, no es posible realizar el envio de una sola
        vez.
    '''
    def __init__(self, stream, controlador):
        ''' se inicializa el hilo, recibimos el socket y el controlador
            ademas creamos el diccionario de funciones manejadoras
        '''
        Thread.__init__(self)
        self.controlador = controlador
        self.stream = stream
        self.manejador_paquetes_recibidos = {
            PAQ_MENSAJE: self.controlador.recibir_mensaje,\
            PAQ_HISTORIAL: self.controlador.cargar_historial,\
            PAQ_RESPUESTA: self.controlador.verificar_operacion,\
            PAQ_BUSQUEDA: self.controlador.recibir_busqueda\
        }

    def run(self):
        ''' Creamos un hilo adicional que servirá exclusivamente para la
            recepcion y manejo de paquetes ya este hilo principal (sesion)
            se encargara de escuchar al comunicador de conexion
            (acciones del usuario) para enviar los paqutes que se requieran
        '''
        self.receptor_paquetes = Thread(target=self.recibir_comunicacion)
        self.receptor_paquetes.start()

        try:
            while True:
                paquete = self.controlador.comunicador_conexion.get()
                if paquete == 'salir':
                    break
                else:
                    self.stream.send(paquete)
            try:
                self.stream.shutdown(0)
                self.stream.close()
            except OSError as e:
                paquete_notificacion = PaqueteNotificacion(NOTIF_CONEXION_ERROR)
                self.controlador.comunicador_notificaciones.put(paquete_notificacion)
            except Exception as e:
                raise
        except Exception as e:
            exit()

    def recibir_comunicacion(self):
        ''' Funcion manipuladora del hilo de recepcion, la cual se encargara
            de recibir y manejar los paquetes recibidos, los paquetes se
            reciben por partes para evitar perdidas de informacion,
            por conexiones lentas o por paquetes muy grandes, el maximo que
            puede recibir a la vez es 1024 bytes
        '''
        while True:
            try:
                fragmentos = []
                while(True):
                    paquete = self.stream.recv(MAX_BYTES)
                    fragmentos.append(paquete)
                    try:
                        input_data = pickle.loads(b"".join(fragmentos))
                    except Exception as e:
                        continue
                    else:
                        break
            except Exception as e:
               break
            else:
                codigo = input_data.codigo
                self.manejador_paquetes_recibidos[codigo](input_data)
