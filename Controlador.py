from modelo.Conexion import Conexion
from modelo.Mensaje import Mensaje
from modelo.Usuario import Usuario
from threading import Thread
from modelo.Paquete import *
from VistaTk import Vista
from socket import socket
from queue import Queue
from utils import *
import pickle

class Controlador:
    ''' Clase representativa del controlador el cual servira como proveedor
        de las acciones del usuario
    '''
    def __init__(self, usuario, salir):
        self.usuario = usuario
        self.salir_app = salir

    def iniciar_vista(self):
        ''' Función que creará e iniciará el objeto de la vista y le pasará el
            controlador para ser utilizado desde la vista
        '''
        vista = Vista(self)
        vista.iniciar()

    def salir(self):
        ''' Función para salir de la aplicación, se llama a una función
            estática de la Aplicación para cerrar la misma, es utilizada
            cuando el usuario no ha iniciado sesión
        '''
        self.salir_app()

    def cerrar_sesion(self):
        ''' Función para cerrar la sesión y finalizar el programa,
            es utilizada cuando la sesión ya ha sido iniciada
            la cual finaliza los hilos (notificaciones y conexion)
        '''
        if self.usuario.online is True:
            self.finalizar_hilos()
            self.usuario.cerrar_sesion()
        self.salir()

    def verificar_operacion(self, paquete):
        ''' Funcion que recibe un paquete de respuesta del servidor,
            dicha respuesta puede ser el resultado de agregar un contacto
            y envia la notificacion al hilo de notificaciones
        '''
        paquete = PaqueteNotificacion(paquete.referencia, paquete.respuesta)
        self.comunicador_notificaciones.put(paquete)

    def finalizar_hilos(self):
        ''' Método que envia a los hilos activos la orden de finalizarse
            para asi poder cerrar sesion y salir del programa
        '''
        paquete_notificacion = PaqueteNotificacion(NOTIF_SALIR)
        self.comunicador_notificaciones.put(paquete_notificacion)
        self.comunicador_conexion.put('salir')

    def iniciar_sesion(self, nick, password, datos_servidor):
        ''' Método para iniciar la sesión que recibe el nick, la contraseña
            y los datos del servidor, se inician los comunicadores Queue
            luego se procede a validar el usuario, retorna True si el usuario
            y la contraseña son correctos, en caso contrario retorna False
        '''
        self.comunicador_notificaciones = Queue()
        self.comunicador_conexion = Queue()

        self.datos_servidor = datos_servidor
        if self.validar_usuario(nick, password):
            self.usuario.iniciar_sesion(nick, password)
            return True
        else:
            return False

    def buscar_usuario(self, usuario):
        ''' Metodo que recibe el nick o el nombre y apellido del usuario,
            crea un paquete de busqueda, lo serializa y lo envia al hilo de la 7
            conexion para ser enviedo al servidor
        '''
        paquete_busqueda = PaqueteBusqueda(usuario)
        paquete_busqueda = pickle.dumps(paquete_busqueda)
        self.comunicador_conexion.put(paquete_busqueda)

    def recibir_busqueda(self, paquete):
        ''' Método que maneja la recepcion de las coincidencias de usuarios
            en la búsqueda, el cual envia al notificador el paquete de
            busqueda
        '''
        paquete_notificacion = PaqueteNotificacion(NOTIF_BUSQUEDA, paquete)
        self.comunicador_notificaciones.put(paquete_notificacion)

    def agregar_contacto(self, contacto):
        ''' Método que recibe un objeto de tipo contacto, crea un paquete
            con el contacto, lo serializa y lo envia al hilo de la conexión
            para ser enviado al servidor
        '''
        paquete_contacto = PaqueteContacto(contacto)
        paquete_contacto = pickle.dumps(paquete_contacto)
        self.comunicador_conexion.put(paquete_contacto)

    def cargar_historial(self, historial):
        ''' Método que recibe un paquete de tipo historial, y carga los
            datos al usuario
        '''
        self.historial = historial.historial_usuario
        self.usuario.nombre = self.historial.nombre
        self.usuario.apellido = self.historial.apellido
        self.usuario.fecha_nacimiento = self.historial.fecha_nacimiento
        self.usuario.sexo = self.historial.sexo
        self.usuario.historial_mensajes = self.historial.historial_mensajes
        self.usuario.lista_contactos = self.historial.lista_contactos

        paquete = PaqueteNotificacion(NOTIF_DATOS_REGISTRO)
        self.comunicador_notificaciones.put(paquete)

    def validar_usuario(self, nick, password):
        ''' Método que recibe un nick y un password, se conecta al servidor,
            envia un paquete de tipo conexion con los datos del usuario,
            espera una respuesta a la solicitud y en caso de error al iniciar
            sesion, retorna false y en caso contrario, crea el hilo de la
            conexión, inicia sesión y retorna True
        '''
        stream = socket()
        stream.connect((self.datos_servidor[0],\
            self.datos_servidor[1]))

        paquete_inicio = PaqueteConexion(nick, password)
        paquete_inicio = pickle.dumps(paquete_inicio)

        try:
            stream.send(paquete_inicio)
        except Exception as e:
            return False
        else:
            res = stream.recv(MAX_BYTES)
            res = pickle.loads(res)

            if res.respuesta is False:
                return False
            else:
                self.conexion = Conexion(stream, self)
                self.conexion.start()
                return True

    def registro_usuario(self, datos_usuario, datos_servidor):
        ''' Métod que recibe los datos del usuario y del servidor, crea
            el nuevo usuario, carga sus datos, lo empaqueta y lo envia al
            servidor como una solicitud de registro de usuario, luego
            espera una respuesta del servidor y la retorna ya sea
            true o false
        '''
        usuario_registrar = Usuario()
        usuario_registrar.nombre = datos_usuario[0]
        usuario_registrar.apellido = datos_usuario[1]
        usuario_registrar.sexo = datos_usuario[2]
        usuario_registrar.fecha_nacimiento = datos_usuario[3]
        usuario_registrar.nick = datos_usuario[4]
        usuario_registrar.passｗord = datos_usuario[5]
        paquete_registro = pickle.dumps(PaqueteRegistro(usuario_registrar))

        stream = socket()
        stream.connect((datos_servidor[0], datos_servidor[1]))

        try:
            stream.send(paquete_registro)
        except Exception as e:
            return False
        else:
            res = stream.recv(MAX_BYTES)
            res = pickle.loads(res)
            return res.respuesta

    def post_datos_perfil_usuario(self):
        ''' Método que retorna los datos del usuario '''
        return self.usuario

    def post_lista_contactos(self):
        ''' Método que retorna la lista de contactos del usuario '''
        return self.usuario.mostrar_contactos()

    def actualizar_datos_perfil_usuario(self, datos_nuevos):
        ''' Método que recibe los datos personales nuevos del usuario
            y los actualiza
        '''
        res = self.usuario.editar_perfil(datos_nuevos)
        if res is True:
            paquete_nuevos_datos = PaqueteActualizacion(datos_nuevos)
            paquete_nuevos_datos = pickle.dumps(paquete_nuevos_datos)
            self.comunicador_conexion.put(paquete_nuevos_datos)
        return res

    def recibir_mensaje(self, paquete):
        ''' Método utilizado para manejar la recepcion de una mensaje,
            se envia al comunicador de notificaciones, el evento de nuevo
            mensaje y luego el usuario lo recibe
        '''
        paquete_notificacion = PaqueteNotificacion(NOTIF_MENSAJE_RECIBIDO,
                                                    paquete.mensaje)
        self.comunicador_notificaciones.put(paquete_notificacion)
        self.usuario.recibir_mensajes(paquete.mensaje)

    def post_comunicador_notificaciones(self):
        ''' Retorna el comunicador de notificaciones '''
        return self.comunicador_notificaciones

    def enviar_mensaje(self, mensaje):
        ''' Recibe los datos del mensaje (contenido, receptor), lo empaqueta,
            serializa y lo envia al servidor
        '''

        mensaje_enviar = Mensaje(self.usuario.nick, mensaje[1], mensaje[0])
        paquete_mensaje = PaqueteMensaje(mensaje_enviar)
        paquete_pickle = pickle.dumps(paquete_mensaje)
        return self.usuario.enviar_mensaje(mensaje_enviar, paquete_pickle,
                                            self.comunicador_conexion)

    def listar_historial_mensajes(self):
        ''' Método que retorna la lista de mensajes del usuario '''
        return self.usuario.mostrar_mensajes()

    def listar_contactos(self):
        ''' Método que retorna la lista de contactos del usuario'''
        return self.usuario.mostrar_contactos()

    def listar_mensajes_contacto(self, nick_contacto):
        ''' Funcion que recibe el nick del contacto a buscar los mensajes
            y retorna una lista de sus mensajes
        '''
        mensajes = self.listar_historial_mensajes()
        mensajes_contacto = []
        for mensaje in mensajes:
            if mensaje.emisor == nick_contacto or \
                mensaje.receptor == nick_contacto:
                mensajes_contacto.append(mensaje)
        return mensajes_contacto

    def verificar_conexion_servidor(self, datos):
        ''' Método que verifica la conexion del servidor, recibe los datos
            del servidor e intenta conectarse enviando un Paquete de Test
            en caso de haber conexion retorna True, en caso contrario retorna
            False
        '''
        paquete = PaqueteTest()
        paquete = pickle.dumps(paquete)
        stream = socket()
        try:
            stream.connect((datos[0], int(datos[1])))
            stream.send(paquete)
        except Exception as e:
            return False
        else:
            return True
