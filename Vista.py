import os
import getpass
from threading import Thread
from utils import *
from datetime import datetime

class Vista:
    ''' Clase para armar e imprimir mensajes, leer los valores y manejar
        las acciones
    '''
    def __init__(self, controlador):
        '''Inicializador que limpia la pantalla, recibe el controlador
            y crea los diccionarios para el manejo de opciones (programacion
            funcional)
        '''
        self.Controlador = controlador
        Vista.limpiar_pantalla()

        self.manejador_opciones_principal = {\
            1: self.iniciar_sesion,\
            2: self.registro_usuario,\
            3: self.salir
        }

        self.manejador_opciones_menu_usuario = {\
            1: self.enviar_mensaje,\
            2: self.ver_mensajes,\
            3: self.buscar_usuario,\
            4: self.listar_contactos,\
            5: self.agregar_contactos,\
            6: self.editar_perfil,\
            7: self.ver_perfil,\
            8: self.cerrar_sesion
        }

    def iniciar(self):
        ''' Funcion que pide los datos del servidor a conectarse, lo valida
            mediante el controlador y de haber conexion entre el cliente
            y el servidor, inicia el sistema mostrando el menu principal
            (iniciar sesion, registrarse, salir), es capaz de manejar las
            opciones de todos los menus, si no hay conexion, se muestra
            el mensaje de error y el final del programa.

            Se manejan dos estados segun la variable estado, que significa
            en False que el usuario no inició sesión, por lo cual se le
            mostrará el menu principal (iniciar sesion, registrarse, salir)
            y el estado True que es cuando el usuario inició sesión
            por lo cual se le mostrará el menu de usuario
            (Enviar mensaje, Ver mensaje, etc)
        '''
        estado = False
        try:
            self.datos_servidor = Entrada.solicitar_datos_servidor()
            if self.Controlador.verificar_conexion_servidor(self.datos_servidor):
                Notificacion.mostrar_correcta_conexion()
                # Bucle infinito correspondiente al menu principal #
                while(estado is False):
                    Menu.mostrar_menu_principal()
                    opcion = Entrada.solicitar_opcion_menu()
                    try:
                        estado = self.manejador_opciones_principal[opcion]()
                    except KeyError as e:
                        Notificacion.mostrar_error_opcion_invalida()
                        estado = False
                    except Exception as e:
                        Notificacion.mostrar_error_operacion()
                        estado = False
                Vista.limpiar_pantalla()
                Notificacion.mostrar_bienvenida()
                # Bucle infinito correspondiente al menu del usuario #
                while(True):
                    Menu.mostrar_menu_usuario_p()
                    opcion = Entrada.solicitar_opcion_menu()
                    try:
                        self.manejador_opciones_menu_usuario[opcion]()
                    except KeyError as e:
                        Notificacion.mostrar_error_opcion_invalida()
                    except Exception as e:
                        Notificacion.mostrar_error_operacion()
            else:
                Notificacion.mostrar_error_conexion()
                Notificacion.mostrar_fin_programa()
                self.Controlador.cerrar_sesion()
        # Excepcion para al interrupción (Ctrl+C)
        except KeyboardInterrupt:
            if estado is False:
                self.salir()
            else:
                self.cerrar_sesion()

    def enviar_mensaje(self):
        ''' Funcion interna de la vista que sirve como manejadora en cuanto a
            las acciones del usuario, la cual pide al controlador la lista
            de contactos del usuario para asi hacerle elegir al usuario a que
            contacto quiere enviarle el mensaje, pide por teclado el mensaje y
            lo envia al controlador para realizar la accion
        '''
        Vista.limpiar_pantalla()
        contactos = self.Controlador.post_lista_contactos()
        datos_mensaje = Entrada.solicitar_datos_mensaje(contactos)
        if datos_mensaje is not None:
            return self.Controlador.enviar_mensaje(datos_mensaje)

    def ver_mensajes(self):
        ''' Funcion interna de la vista que sirve como manejadora en cuanto a
            las acciones del usuario, la cual pide al controlador el historial
            de mensajes del usuario y luego lo imprime
        '''
        Vista.limpiar_pantalla()
        mensajes = self.Controlador.listar_historial_mensajes()
        Lista.listar_mensajes(mensajes)
        return True

    def buscar_usuario(self):
        '''Funcion interna de la vista que sirve como manejadora en cuanto a
            las acciones del usuario, la cual pide al usuario al menos el nombre
            de usuario del contacto o su nombre y apellido el cual lo pasa a una
            funcion del controlador para que realice la busqueda
        '''
        Vista.limpiar_pantalla()
        usuario = Entrada.solicitar_datos_contacto()
        self.Controlador.buscar_usuario(usuario)

    def listar_contactos(self):
        ''' Funcion interna de la vista que sirve como manejadora en cuanto a
            las acciones del usuario, la cual pide al servidor la lista de
            contactos y luego la imprime
        '''
        Vista.limpiar_pantalla()
        contactos = []
        contactos = self.Controlador.listar_contactos()
        Lista.listar_contactos(contactos)

    def agregar_contactos(self):
        ''' Funcion interna de la vista que sirve como manejadora en cuanto a
            las acciones del usuario, la cual pide los datos del nuevo contacto
            a agregar y los envia al controlador para que realice la acción
        '''
        Vista.limpiar_pantalla()
        contacto = Entrada.solicitar_nombre_usuario_contacto()
        self.Controlador.agregar_contacto(contacto)

    def editar_perfil(self):
        ''' funcion que pide al usuario los datos nuevos del perfil
            y los envia al controlador
        '''
        Vista.limpiar_pantalla()
        datos_actuales = self.Controlador.post_datos_perfil_usuario()
        datos_nuevos = Entrada.solicitar_datos_perfil(datos_actuales)
        self.Controlador.actualizar_datos_perfil_usuario(datos_nuevos)
        Notificacion.mostrar_edicion_perfil()
        return True

    def ver_perfil(self):
        ''' funcion que limpia la pantalla, recoge los datos del perfil desde
            una funcion del controlador y luego imprime el perfil con una funcion
            llamada listar perfil de la clase Lista
        '''
        Vista.limpiar_pantalla()
        datos_actuales = self.Controlador.post_datos_perfil_usuario()
        Lista.listar_perfil(datos_actuales)
        return True

    def cerrar_sesion(self):
        ''' Funcion que muestra el mensaje de fin de programa y
            llama a la funcion cerrar sesion del controladro
        '''
        Notificacion.mostrar_fin_programa()
        self.Controlador.cerrar_sesion()

    def salir(self):
        ''' Funcion que muestra el mensaje de fin de programa y
            llama a la funcion salir del controladro
        '''
        Notificacion.mostrar_fin_programa()
        self.Controlador.salir()

    def iniciar_sesion(self):
        ''' Funcion interna de la vista que sirve como manejadora en cuanto a
            las acciones del usuario, la cual pide los datos de la cuenta a
            iniciar sesion y se lo pasa a una funcion del controlador encargada
            de iniciar la sesion, retornando su respuesta en una variable
            y de acuerdo a la respuesta se inicia el hilo de notificaciones,
        '''
        self.datos_sesion = Entrada.solicitar_datos_cuenta()
        res = self.Controlador.iniciar_sesion(self.datos_sesion[0],\
        self.datos_sesion[1], self.datos_servidor)

        if res is True:
            comunicador = self.Controlador.post_comunicador_notificaciones()
            self.notificador = Notificacion(comunicador)
            self.notificador.start()
        else:
            Notificacion.mostrar_sesion_error()
        return res

    def registro_usuario(self):
        ''' Funcion interna de la vista que sirve como manejadora en cuanto a
            las acciones del usuario, la cual pide los datos del registro para
            un usuario nuevo y los envia a una funcion del Controlador encargada
            del registro
        '''
        datos = Entrada.solicitar_datos_registro()
        res = self.Controlador.registro_usuario(datos, self.datos_servidor)
        if res is True:
            Notificacion.mostrar_registro_ok()
        else:
            Notificacion.mostrar_registro_error()
        return False

    @staticmethod
    def limpiar_pantalla():
        '''funcion que limpia la pantalla'''
        os.system('cls' if os.name =='nt' else 'clear')

    @staticmethod
    def imprimir(mensaje):
        '''Imprime lo que se le envia por parametro'''
        Vista.imprimir(mensaje)

    @staticmethod
    def input_numero(etiqueta_entrada):
        '''Funcion que lee un numero, validando que el valor leido
            se realmente un numero, mientras que el usuario no ingrese
            un numero, se le seguirá pidiendo el valor, la funcion retorna
            el numero leido
        '''
        while(True):
            try:
                entrada = int(input(etiqueta_entrada))
            except ValueError as e:
                Vista.imprimir("# Error: El valor leido debe ser numérico")
            else:
                break
        return entrada

    @staticmethod
    def input_cadena(etiqueta_entrada, req=False):
        '''Funcion que recibe una cadena a ser mostrada al momento de
            la lectura y retornará la cadena leida,
            se diferencia una entrada si es o no requerida, con la variable req
        '''
        if req is True:
            while(True):
                entrada = input(etiqueta_entrada)
                try:
                    if not(entrada and entrada.strip()):
                        raise Exception("CadenaVacia")
                except Exception:
                    Vista.imprimir("# Error: Por favor, complete el campo")
                else:
                    break
        else:
            entrada = input(etiqueta_entrada)

        return entrada

    @staticmethod
    def input_fecha(etiqueta_entrada):
        '''Funcion que recibe una cadena que será mostrada
            al usuario al querer ingresar una fecha,
            dicha funcion validará que el dato sea una fecha
            dd/mm/yy, mientras que no sea una fecha, se le volverá a
            pedir al usuario, la funcion retorna la fecha leida
        '''
        while(True):
            entrada = input(etiqueta_entrada)
            try:
                datetime.strptime(entrada, "%d/%m/%Y")
            except ValueError:
                Vista.imprimir("# Error: El valor leido no es una fecha")
            else:
                break
        return entrada

    @staticmethod
    def input_password(etiqueta_entrada, req=False):
        '''Funcion que lee y retorna una contraseña ocultando los
            valores al estilo linux, la cual recibe una cadena que será
            mostrada al querer ingresar la contraseña
        '''
        if req is True:
            while(True):
                entrada = getpass.getpass(etiqueta_entrada)
                try:
                    if not(entrada and entrada.strip()):
                        raise Exception("PasswordVacio")
                except Exception:
                    Vista.imprimir("# Error: Por favor, ingrese la contraseña")
                else:
                    break
        else:
            entrada = getpass.getpass(etiqueta_entrada)
        return entrada

class Entrada:
    ''' Clase para manejar las entradas de datos '''

    @staticmethod
    def solicitar_nombre_usuario_contacto():
        ''' Funcion estatica que solicita el nombre de usuario del contacto
            y lo retorna
        '''
        nombre = Vista.input_cadena("Nombre de usuario de contacto: ")
        return nombre

    @staticmethod
    def solicitar_datos_contacto():
        ''' Funcion estatica que solicita el nombre de usuario del cotnacto
            a buscar o el nombre y apellido y los retorna
        '''
        datos = Vista.input_cadena("Nombre de usuario o nickname: ", True)
        return datos

    @staticmethod
    def solicitar_datos_servidor():
        ''' Funcion que solicita los datos del servidor al usuario y lo retorna
        '''
        datos = []
        datos.append(Vista.input_cadena("IP: ", True))
        datos.append(Vista.input_numero("PUERTO: "))
        return datos

    @staticmethod
    def solicitar_datos_cuenta():
        ''' Funcion estatica que pide los datos de la cuenta del usuario
            y los marca como datos requeridos, los retorna al final
        '''
        datos = []
        datos.append(Vista.input_cadena("\nUsername: ", True))
        datos.append(Vista.input_password("Password: ", True))
        return datos

    @staticmethod
    def solicitar_opcion_menu():
        ''' Funcion que solicita y retorna la opción del menu mostrado '''
        opcion = Vista.input_numero("¿Que desea?: ")
        return opcion

    @staticmethod
    def solicitar_datos_perfil(actual):
        ''' Funcion estatica que solicita al usuario los datos de su perfil y
            luego lo retorna
        '''
        datos = []
        if actual != []:
            datos.append(Vista.input_cadena("\nNombre ["+actual.nombre+"]: "))
            datos.append(Vista.input_cadena("Apellido ["+actual.apellido+"]: "))
            datos.append(Vista.input_cadena("Sexo ["+actual.sexo+"]: "))
            datos.append(Vista.input_fecha("Fecha de nacimiento (DD/MM/AAAA)\
                                            ["+actual.fecha_nacimiento+"]: "))
        else:
            datos.append(Vista.input_cadena("\nNombre: "))
            datos.append(Vista.input_cadena("Apellido: "))
            datos.append(Vista.input_cadena("Sexo: "))
            datos.append(Vista.input_fecha("Fecha de nacimiento (DD/MM/AAAA): "))
        return datos

    def solicitar_datos_registro():
        ''' Funcion estatica que solicita al usuario los datos de su perfil
            para registrarse y luego lo retorna
        '''
        datos = []
        datos.append(Vista.input_cadena("\nNombre: "))
        datos.append(Vista.input_cadena("Apellido: "))
        datos.append(Vista.input_cadena("Sexo: "))
        datos.append(Vista.input_fecha("Fecha de nacimiento (DD/MM/AAAA): "))
        datos.append(Vista.input_cadena("Nombre de usuario: "))
        datos.append(Vista.input_password("Contraseña: "))
        return datos

    @staticmethod
    def solicitar_datos_mensaje(contactos):
        ''' Aca para el destinatario vamos a listar su lista de contactos
            y de ahi que elija uno para enviarle el mensaje
            si no tiene contactos entonces no puede ser capaz de enviar un
            mensaje
        '''
        if Lista.listar_contactos(contactos):
            datos = []
            destinatario = Vista.input_numero ("Seleccione el contacto: ")
            try:
                if destinatario <= 0:
                    raise Exception("DestinatarioInvalido")
                else:
                    try:
                        datos.append(contactos[destinatario-1].nick)
                    except IndexError as e:
                        raise
            except Exception as e:
                Notificacion.mostrar_error_seleccion_usuario()
                raise
            else:
                datos.append(Vista.input_cadena("Mensaje: "))
            return datos
        return None

class Menu:
    ''' Clase para mostrar los diferentes menus '''

    @staticmethod
    def mostrar_menu_principal():
        ''' Muestra el menu principal '''
        Vista.imprimir("\n(1) Iniciar sesión")
        Vista.imprimir("(2) Registrarse")
        Vista.imprimir("(3) Salir\n")


    @staticmethod
    def mostrar_menu_usuario_p():
        ''' Muestra el menu de usuario '''
        Vista.imprimir("\n(1) Enviar mensaje")
        Vista.imprimir("(2) Ver mensajes")
        Vista.imprimir("(3) Buscar usuario")
        Vista.imprimir("(4) Listar contactos")
        Vista.imprimir("(5) Agregar contacto")
        Vista.imprimir("(6) Editar perfil")
        Vista.imprimir("(7) Ver perfil")
        Vista.imprimir("(8) Cerrar sesión\n")

class Notificacion(Thread):
    ''' Clase para mostrar las notificaciones del sistema '''

    def __init__(self, comunicacion):
        ''' Inicializa el hilo, el comunicador y el manejador
            de notificaciones (programacion funcional)
        '''
        Thread.__init__(self)
        self.comunicacion = comunicacion

        self.manejador_notificaciones = {
            NOTIF_MENSAJE_RECIBIDO: self.mostrar_mensaje_recibido,\
            NOTIF_CONTACTO: self.mostrar_informacion_proceso_contacto,\
            NOTIF_OPERACION_EXITOSA: self.mostrar_operacion_exitosa,\
            NOTIF_OPERACION_ERROR: Notificacion.mostrar_error_operacion,\
            NOTIF_DATOS_REGISTRO: self.mostrar_datos_registro,\
            NOTIF_BUSQUEDA: self.mostrar_resultados_busqueda,\
        }

    def run(self):
        ''' Funcion sobrecargada de Thread que inicia el hilo, en la cual
            esperamos recibir un paquete del comunicador y al receibir
            verificamos que no sea un paquete de finalizacion del notificador
            caso contrario manejamos el proposito del paquete
        '''
        while True:
            paquete = self.comunicacion.get()
            if paquete.codigo == NOTIF_SALIR:
                break
            self.manejador_notificaciones[paquete.codigo](paquete.extra);

    def mostrar_datos_registro(self, extra=None):
        pass

    def mostrar_resultados_busqueda(self, paquete):
        ## ver si es una lista o no ##
        Lista.listar_contactos_busqueda(paquete.usuario)

    def mostrar_informacion_proceso_contacto(self, extra):
        ''' Funcion que recibe la respuesta del proceso de agregar contacto
            si se pudo agregar correctamente entonces muestra un mensaje de
            confirmacion, en caso contrario un mensaje de error
        '''
        if extra is True:
            Vista.imprimir("\n# Contacto agregado correctamente #")
        else:
            Vista.imprimir("\n# El usuario no existe o ya ha sido agregado #")

    @staticmethod
    def mostrar_sesion_error():
        ''' Método estático que imprime un error de inicio de sesión
            es estático porque se crea un objeto de tipo hilo notificación
            una vez el usuario haya iniciado sesión
        '''
        Vista.imprimir("\n# Error: Usuario o contraseña inválidos #")

    @staticmethod
    def mostrar_registro_error():
        ''' Método estatico que imprime un error de registro,
            es estático porque se crea un objeto de tipo hilo notificación
            una vez el usuario haya iniciado sesión
        '''
        Vista.imprimir("\n# Error: No se ha podido registrar #")

    @staticmethod
    def mostrar_registro_ok():
        ''' Método estatico que notifica que el registro fue exitoso
            es estático porque se crea un objeto de tipo hilo notificación
            una vez el usuario haya iniciado sesión
        '''
        Vista.imprimir("\n# Usuario registrado exitosamente #")

    def mostrar_mensaje_recibido(self, mensaje):
        ''' Método que notifica al usuario de un mensaje nuevo '''
        Vista.imprimir("\nMensaje nuevo de " + mensaje.emisor + " \n")

    @staticmethod
    def mostrar_error_seleccion_usuario():
        ''' Método que imprime el mensaje de error correspodiente
            a usuario invalido
        '''
        Vista.imprimir("\n# Error: Selección de usuario inválido #")

    @staticmethod
    def mostrar_bienvenida():
        ''' Método estatico que imprime la bienvenida al sistema'''
        Vista.imprimir("____________________________________________________________")
        Vista.imprimir("|||||||| BIENVENIDO AL SISTEMA DE MENSAJERIA ONLINE ||||||||")
        Vista.imprimir("¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨")

    @staticmethod
    def mostrar_fin_programa():
        ''' Método estatico que imprime el final del sistema'''
        Vista.imprimir("\n____________________________________________________________")
        Vista.imprimir("|||||||||||||||||||| FIN DEL PROGRAMA ||||||||||||||||||||||")
        Vista.imprimir("¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨")

    def mostrar_operacion_exitosa(self, extra):
        ''' Método que informa sobre una operacion exitosa '''
        Vista.imprimir("\n# Operación exitosa!")

    @staticmethod
    def mostrar_error_conexion():
        ''' Método estatico que muestra el error de conexion '''
        Vista.imprimir("\n### Error de conexión con el servidor ###")

    @staticmethod
    def mostrar_error_opcion_invalida():
        ''' Metodo estatico que informa que la opcion es invalida'''
        Vista.limpiar_pantalla()
        Vista.imprimir("\n### Opción invalida ###")

    @staticmethod
    def mostrar_error_operacion(extra=None):
        ''' Metodo que indica que hubo un error al realizar la operacion'''
        Vista.imprimir("### Hubo un error al realizar la operación ###")

    @staticmethod
    def mostrar_correcta_conexion():
        ''' Metodo que muestra que hay conexion al servidor '''
        Vista.imprimir("\n# Conexión realizada exitosamente !!!")

    @staticmethod
    def mostrar_edicion_perfil():
        ''' Metodo que informa que los datos han sido actualizados '''
        Vista.limpiar_pantalla()
        Vista.imprimir("\n# Datos de perfil actualizados exitosamente !!!")

    @staticmethod
    def mostrar_no_hay_mensajes():
        ''' Metodo que muestra la notificacion de que no hay mensajes '''
        Vista.imprimir("\n# No hay mensajes aún ")

    @staticmethod
    def mostrar_no_hay_datos():
        ''' Metodo que indica que no hay nada para mostrar '''
        Vista.imprimir("\n# No hay nada para mostrar ")

    @staticmethod
    def mostrar_no_hay_contactos():
        ''' Metodo estatico que indica que no existen contactos '''
        Vista.imprimir("\n# No hay contactos aún ")

    @staticmethod
    def mostrar_no_hay_coincidencias():
        ''' Metodo que indica que el usuario no existe'''
        Vista.imprimir("# El usuario no existe")

    @staticmethod
    def mostrar_titulo_resultados_busqueda():
        '''Metodo que muestra el titulo de los resultados de busqueda '''
        Vista.imprimir("\n\n# Resultados de la Búsqueda: #\n")

class Lista:
    ''' Clase para mostrar las distintas listas del sistema '''

    @staticmethod
    def listar_mensajes(mensajes):
        ''' Método que recibe una lista de mensajes y los imprime '''
        Vista.limpiar_pantalla()
        if mensajes == []:
            Notificacion.mostrar_no_hay_mensajes()
        else:
            for mensaje in mensajes:
                Vista.imprimir(mensaje)

    @staticmethod
    def listar_contactos(contactos):
        ''' Método que recibe la lista de contactos y los imprime '''
        Vista.limpiar_pantalla()
        if contactos == []:
            Notificacion.mostrar_no_hay_contactos()
            return False
        else:
            i = 1
            for contacto in contactos:
                Vista.imprimir("(" + str(i) + ") " + str(contacto))
                i = i+1
            return True

    @staticmethod
    def listar_contactos_busqueda(contactos):
        ''' Método que recibe la lista de coincidencias y luego los imprime '''
        if isinstance(contactos, list):
            if contactos == []:
                Notificacion.mostrar_no_hay_coincidencias()
            else:
                for contacto in contactos:
                    Vista.imprimir(contacto)
        else:
            Vista.imprimir(contactos)

    @staticmethod
    def listar_perfil(usuario):
        ''' Metodo que recibe los datos del usuario y los imprime '''
        Vista.limpiar_pantalla()
        if usuario == []:
            Notificacion.mostrar_no_hay_datos()
        else:
            Vista.imprimir(usuario)
