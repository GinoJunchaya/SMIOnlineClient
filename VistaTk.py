import tkinter.messagebox as tkmsgbox
import tkinter.scrolledtext as tkst
from functools import partial
from threading import Thread
from pygame import mixer
from tkinter import ttk
from tkinter import *
from utils import *
import os

class Vista:
	''' Clase que representa a la vista en tkinter '''
	def __init__(self, controlador):
		self.controlador = controlador
		self.frame_contactos = None
		self.frame_chat = None
		self.nick_contacto = ''
		self.buttons_contactos = []
		self.lista_generos = ["Masculino", "Femenino", "No especificar"]

		try:
			mixer.init()
			self.reproductor = mixer.Sound("Cliente/sounds/mensaje.wav")
		except:
			self.reproductor = None

	def iniciar(self):
		''' Funcion que crea la ventana con el titulo SMIOnline | v1.0, dibuja
		 	los datos de entrada del servidor para luego iniciar la ventana
		'''
		self.ventana = Ventana('SMIOnline | v1.0')
		self.mostrar_entrada_servidor()
		self.ventana.invocar()

	def cerrar(self):
		''' Función que cierra la ventana y termina el programa '''
		self.ventana.salir()
		self.controlador.cerrar_sesion()

	def clear_grid(self, ventana):
		''' Limpia los widgets dibujados en la grilla de una ventana '''
		list = ventana.grid_slaves()
		for l in list:
			l.destroy()

	def clear_pack(self, ventana):
		''' Limpia los widgets dibujados en una ventana con pack'''
		list = ventana.pack_slaves()
		for l in list:
			l.destroy()

	def mostrar_resultados_busqueda(self, coincidencias):
		''' Ventana que muestra los resultados de la búsqueda
		'''
		ventana_datos = Ventana("Resultados de la Búsqueda")
		ventana_datos.centrar(300,400)

		etiqueta_titulo = Label(ventana_datos.ventana,
						text="Resultados de la Búsqueda", font="Ubuntu 15 bold")
		etiqueta_titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10,
																	sticky=W)

		frame_resultados = Contenedor(ventana_datos.ventana, width=250, height=200,
							bg=FONDO_CONTACTOS, highlightbackground=FONDO_CONTACTOS,
							highlightcolor=FONDO_CONTACTOS, highlightthickness=1)
		frame_resultados.grid(row=1, rowspan=2, column=0, columnspan=2, padx=10,
								pady=10)

		if isinstance(coincidencias, list):
			for i in coincidencias:
				Label(frame_resultados.interior, text="Nombre y Apellido: " + i.nombre + " " + i.apellido,
					font="Ubuntu 10", bg=FONDO_CONTACTOS).pack()
				Label(frame_resultados.interior, text="Sexo: " + i.sexo, font="Ubuntu 10",
					bg=FONDO_CONTACTOS).pack()
				Label(frame_resultados.interior, text="Fecha de nacimiento: " + i.fecha_nacimiento,
					font="Ubuntu 10", bg=FONDO_CONTACTOS).pack()
				Label(frame_resultados.interior, text="Nick: " + i.nick, font="Ubuntu 10",
					bg=FONDO_CONTACTOS).pack()
				Label(frame_resultados.interior, text=" ", font="Ubuntu 10", bg=FONDO_CONTACTOS).pack()
		else:
			Label(frame_resultados.interior,
				text="Nombre y Apellido: " + coincidencias.nombre + " " + coincidencias.apellido,
				font="Ubuntu 10", bg=FONDO_CONTACTOS).pack()
			Label(frame_resultados.interior, text="Sexo: " + coincidencias.sexo, font="Ubuntu 10",
				bg=FONDO_CONTACTOS).pack()
			Label(frame_resultados.interior, text="Fecha de nacimiento: " + coincidencias.fecha_nacimiento,
				font="Ubuntu 10", bg=FONDO_CONTACTOS).pack()
			Label(frame_resultados.interior, text="Nick: " + coincidencias.nick, font="Ubuntu 10",
				bg=FONDO_CONTACTOS).pack()

		boton_cerrar = Button(ventana_datos.ventana, text="Cerrar", command=ventana_datos.ventana.destroy, fg=LABEL_2, bg=CLOSE)
		boton_cerrar.grid(row=3, column=1, sticky=E, pady=20)

		ventana_datos.invocar()

	def mostrar_perfil_usuario(self):
		''' Ventana emergente que muestra el perfil del usuario, pidiendo los
			datos del perfil desde el controlador, y mostrandolos en forma
			ordenada, permitiendo editar dichos datos a traves de un botón que
			abre otra ventana emergente
		'''
		ventana_datos = Ventana("Datos del perfil")
		ventana_datos.centrar(260,200)

		datos_usuario = self.controlador.post_datos_perfil_usuario()

		etiqueta_titulo = Label(ventana_datos.ventana, text="Mi Perfil",
													font="Ubuntu 20 bold")
		etiqueta_titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10,
																	sticky=W)

		etiqueta_titulo_nombre_apellido = Label(ventana_datos.ventana,
							text="Nombre y Apellido: ", font="Ubuntu 10 bold")
		etiqueta_titulo_nombre_apellido.grid(row=1, column=0, sticky=E, padx=10)

		etiqueta_titulo_sexo = Label(ventana_datos.ventana, text="Sexo: ",
														font="Ubuntu 10 bold")
		etiqueta_titulo_sexo.grid(row=2, column=0, sticky=E, padx=10)

		etiqueta_titulo_fecha = Label(ventana_datos.ventana, text="Fecha de nac.: ",
															font="Ubuntu 10 bold")
		etiqueta_titulo_fecha.grid(row=3, column=0, sticky=E, padx=10)

		etiqueta_titulo_nickname = Label(ventana_datos.ventana, text="Nickname: ",
														font="Ubuntu 10 bold")
		etiqueta_titulo_nickname.grid(row=4, column=0, sticky=E, padx=10)

		etiqueta_nombre_apellido = Label(ventana_datos.ventana,
					text=(datos_usuario.nombre + " " + datos_usuario.apellido))
		etiqueta_nombre_apellido.grid(row=1, column=1, sticky=W)

		etiqueta_sexo = Label(ventana_datos.ventana, text=datos_usuario.sexo)
		etiqueta_sexo.grid(row=2, column=1, sticky=W)

		etiqueta_fecha = Label(ventana_datos.ventana,
											text=datos_usuario.fecha_nacimiento)
		etiqueta_fecha.grid(row=3, column=1, sticky=W)

		etiqueta_nickname = Label(ventana_datos.ventana, text=datos_usuario.nick)
		etiqueta_nickname.grid(row=4, column=1, sticky=W)

		boton_cerrar = Button(ventana_datos.ventana, text="Cerrar",
					command=ventana_datos.ventana.destroy, fg=LABEL_2, bg=CLOSE)
		boton_cerrar.grid(row=5, column=0, sticky=E, pady=20, padx=5)

		boton_editar = Button(ventana_datos.ventana, text="Editar",
						command=lambda:self.evento_editar_perfil(ventana_datos),
														fg=LABEL_2, bg=PRIMARIO)
		boton_editar.grid(row=5, column=1, sticky=W, pady=20)
		ventana_datos.invocar()

	def mostrar_editar_perfil_usuario(self):
		''' Función que crea una ventana y dibuja los widgets que se utilizarán
			para la edicion del perfil del usuario, cargando previamente
			en cada uno de ellos los datos actuales
		'''
		ventana_datos = Ventana("Editar datos del perfil")
		ventana_datos.centrar(280,210)

		datos_usuario = self.controlador.post_datos_perfil_usuario()

		etiqueta_titulo = Label(ventana_datos.ventana, text="Editar perfil",
														font="Ubuntu 20 bold")
		etiqueta_titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=W)

		etiqueta_titulo_nombre = Label(ventana_datos.ventana, text="Nombre: ",
														font="Ubuntu 10 bold")
		etiqueta_titulo_nombre.grid(row=1, column=0, sticky=E, padx=10)

		etiqueta_titulo_apellido = Label(ventana_datos.ventana, text="Apellido: ",
														font="Ubuntu 10 bold")
		etiqueta_titulo_apellido.grid(row=2, column=0, sticky=E, padx=10)

		etiqueta_titulo_sexo = Label(ventana_datos.ventana, text="Sexo: ",
		 												font="Ubuntu 10 bold")
		etiqueta_titulo_sexo.grid(row=3, column=0, sticky=E, padx=10)

		etiqueta_titulo_fecha = Label(ventana_datos.ventana, text="Fecha de nac.: ",
		 												font="Ubuntu 10 bold")
		etiqueta_titulo_fecha.grid(row=4, column=0, sticky=E, padx=10)

		nombre_var = StringVar(ventana_datos.ventana)
		nombre_var.set(datos_usuario.nombre)
		box_nombre = CajaTexto(ventana=ventana_datos.ventana, variable=nombre_var,
																	tamano=20)
		box_nombre.invocar_grid(1,1,sticky=W)

		apellido_var = StringVar(ventana_datos.ventana)
		apellido_var.set(datos_usuario.apellido)
		box_apellido = CajaTexto(ventana=ventana_datos.ventana,
											variable=apellido_var, tamano=20)
		box_apellido.invocar_grid(2,1,sticky=W)

		sexo_var = StringVar(ventana_datos.ventana)
		sexo_var.set(datos_usuario.sexo)

		seleccion_sexo = Seleccion(ventana=ventana_datos.ventana, var=sexo_var,
												elementos=self.lista_generos)
		seleccion_sexo.invocar_grid(3,1,sticky=W)

		fecha_var = StringVar(ventana_datos.ventana)
		fecha_var.set(datos_usuario.fecha_nacimiento)
		box_fecha = CajaTexto(ventana=ventana_datos.ventana, variable=fecha_var,
																	tamano=20)
		box_fecha.invocar_grid(4,1,sticky=W)

		boton_guardar = Button(ventana_datos.ventana, text="Guardar",
								command=lambda:self.evento_guardar_perfil_editado(\
								nombre_var.get(), apellido_var.get(), sexo_var.get(),
								fecha_var.get()), fg=LABEL_2, bg=PRIMARIO)
		boton_guardar.grid(row=5, column=0, sticky=E, pady=20)

		boton_cerrar = Button(ventana_datos.ventana, text="Cancelar",
					command=ventana_datos.ventana.destroy, fg=LABEL_2, bg=CLOSE)
		boton_cerrar.grid(row=5, column=1, sticky=W, pady=20, padx=5)

		ventana_datos.invocar()

	def mostrar_entrada_servidor(self):
		''' Dibuja los widgets utilizados para la entrada de datos y conexion
			con el servidor
		'''
		self.ventana.centrar(300,150)
		etiqueta_titulo = Etiqueta(ventana=self.ventana.ventana,
									nombre="Ingrese los datos del servidor",
									color=LABEL_1, fuente=FUENTE_PRED,
									tamano="15")
		etiqueta_titulo.invocar_grid(0, 0, 1, 2, sticky=W+E)

		self.ddns = StringVar(self.ventana.ventana)
		self.puerto = StringVar(self.ventana.ventana)

		etiqueta_dns = Etiqueta(ventana=self.ventana.ventana, nombre="DNS:",
								color=LABEL_1, fuente=FUENTE_PRED, tamano=10)
		etiqueta_dns.invocar_grid(3,0,sticky=E)

		box_dns = CajaTexto(ventana=self.ventana.ventana, variable=self.ddns,
							tamano=20)
		box_dns.invocar_grid(3,1,sticky=W)
		box_dns.caja_texto.focus()

		etiqueta_puerto = Etiqueta(ventana=self.ventana.ventana, nombre="PUERTO:",
								color= LABEL_1, fuente=FUENTE_PRED, tamano=10)
		etiqueta_puerto.invocar_grid(4,0,sticky=E)

		box_puerto = CajaTexto(ventana=self.ventana.ventana,
											variable=self.puerto, tamano=10)
		box_puerto.caja_texto.bind('<Return>', self.bind_evento_conectarse)
		box_puerto.invocar_grid(4,1,sticky=W)

		boton_conectarse = Boton(ventana=self.ventana.ventana, nombre="Conectarse",
						color=LABEL_2, fondo=PRIMARIO,
						evento=lambda: self.evento_conectarse([self.ddns.get(),
							int(self.puerto.get())]), tamano=30)
		boton_conectarse.invocar_grid(5,0,1,2)

	def mostrar_registrarse(self):
		''' Dibuja en la ventana los widgets utilizados para la entrada de
			datos del registro
		'''
		self.ventana.centrar(440,180)
		etiqueta_titulo = Etiqueta(ventana=self.ventana.ventana,
									nombre="Formulario de registro",
									color=LABEL_1, fuente=FUENTE_PRED,
									tamano="15")
		etiqueta_titulo.invocar_grid(0,0,1,5,sticky=W+E)

		nombre = StringVar(self.ventana.ventana)
		apellido = StringVar(self.ventana.ventana)
		sexo = StringVar(self.ventana.ventana)
		fecha_nacimiento = StringVar(self.ventana.ventana)
		nickname = StringVar(self.ventana.ventana)
		password = StringVar(self.ventana.ventana)

		# ENTRADA NICKNAME

		etiqueta_nick = Etiqueta(ventana=self.ventana.ventana,
							nombre="Nickname: ", color=LABEL_1,
							fuente=FUENTE_PRED, tamano=10)
		etiqueta_nick.invocar_grid(1,0,sticky=E)

		box_nick = CajaTexto(ventana=self.ventana.ventana, variable=nickname,
																	tamano=15)
		box_nick.invocar_grid(1,1,sticky=W)

		# ENTRADA PASSWORD

		etiqueta_password = Etiqueta(ventana=self.ventana.ventana,
							nombre="Contraseña: ", color=LABEL_1,
							fuente=FUENTE_PRED, tamano=10)
		etiqueta_password.invocar_grid(1,4,sticky=E)

		box_password = CajaTexto(ventana=self.ventana.ventana, variable=password,
																	tamano=15)
		box_password.tipo_password()
		box_password.invocar_grid(1,5,sticky=W)

		# ENTRADA NOMBRE

		etiqueta_nombre = Etiqueta(ventana=self.ventana.ventana, nombre="Nombre: ",
									color=LABEL_1, fuente=FUENTE_PRED, tamano=10)
		etiqueta_nombre.invocar_grid(2,0,sticky=E)

		box_nombre = CajaTexto(ventana=self.ventana.ventana, variable=nombre,
								tamano=15)
		box_nombre.invocar_grid(2,1,sticky=W)

		# ENTRADA APELLIDO

		etiqueta_apellido = Etiqueta(ventana=self.ventana.ventana,
									nombre="Apellido: ", color=LABEL_1,
									fuente=FUENTE_PRED, tamano=10)
		etiqueta_apellido.invocar_grid(2,4,sticky=E)

		box_apellido = CajaTexto(ventana=self.ventana.ventana, variable=apellido,
								tamano=15)
		box_apellido.invocar_grid(2,5,sticky=W)

		# ENTRADA SEXO

		etiqueta_sexo = Etiqueta(ventana=self.ventana.ventana, nombre="Sexo: ",
									color=LABEL_1, fuente=FUENTE_PRED, tamano=10)
		etiqueta_sexo.invocar_grid(3,0,sticky=E)

		sexo.set(self.lista_generos[0])

		seleccion_sexo = Seleccion(ventana=self.ventana.ventana, var=sexo,
									elementos=self.lista_generos)
		seleccion_sexo.invocar_grid(3,1,sticky=W)

		# ENTRADA FECHA DE NACIMIENTO

		etiqueta_fecha = Etiqueta(ventana=self.ventana.ventana,
									nombre="Fecha de nac.: ", color=LABEL_1,
									fuente=FUENTE_PRED, tamano=10)
		etiqueta_fecha.invocar_grid(3,4,sticky=E)

		box_fecha = CajaTexto(ventana=self.ventana.ventana,
								variable=fecha_nacimiento, tamano=15)
		box_fecha.invocar_grid(3,5,sticky=W)

		# BOTONES

		boton_registro = Boton(ventana=self.ventana.ventana,
						nombre="Registrarse", color=LABEL_2,
						fondo=SECUNDARIO,
						evento=lambda: self.evento_proceso_registro([nombre.get(),
							apellido.get(), sexo.get(), fecha_nacimiento.get(),
							nickname.get(), password.get()]))
		boton_registro.invocar_grid(4,4,1,1)

		boton_login = Boton(ventana=self.ventana.ventana,
						nombre="Iniciar sesión", color=LABEL_2,
						fondo=PRIMARIO, evento=lambda: self.evento_ir_a_login())
		boton_login.invocar_grid(4,5,1,1)

	def mostrar_inicio_usuario(self):
		''' Función que dibuja los widgets que corresponden al menu del usuario,
			una barra superior con el nick del usuario, luego una caja de
			texto que corresponde a la busqueda o para agregar, luego un
			contenedor con los mensajes y otro con los mensajes, ademas botones
			para enviar, cerrar sesion y ver perfil
		'''
		self.ventana.centrar(528,490)

		# BARRA SUPERIOR
		barra_sup = Frame(height=30, width=528, bg=PRIMARIO)
		barra_sup.grid(row=0, column=0, columnspan=4)

		etiqueta_nick = Etiqueta(ventana=self.ventana.ventana,
									nombre=("Bienvenido " + self.datos_cuenta[0]),
									color=LABEL_2, fuente=FUENTE_PRED, tamano=10,
									fondo=PRIMARIO)
		etiqueta_nick.invocar_grid(0,0,sticky=W)

		# CAJA BUSQUEDA
		nick_buscar = StringVar(self.ventana.ventana)

		campo_buscar = CajaTexto(ventana=self.ventana.ventana,
					variable=nick_buscar, tamano=20, fuente=(FUENTE_PRED, 15))
		campo_buscar.invocar_grid(1,0,1,2, sticky=W, x=20, y=10)
		campo_buscar.caja_texto.focus()

		boton_buscar = Boton(ventana=self.ventana.ventana, nombre="Buscar",
						color=LABEL_2, fondo=PRIMARIO,
						evento=lambda: self.evento_buscar(nick_buscar.get()),
						tamano=5)
		boton_buscar.invocar_grid(1,2,x=0,y=0,sticky=W)

		boton_agregar = Boton(ventana=self.ventana.ventana, nombre="Agregar",
						color=LABEL_2, fondo=PRIMARIO,
						evento=lambda: self.evento_agregar(nick_buscar.get()),
						tamano=15)
		boton_agregar.invocar_grid(1,3, x=10, y=0, sticky=W)

		# LISTA CONTACTOS

		self.label_cont = Label(self.ventana.ventana, text="Lista de contactos",
							bg=SECUNDARIO, fg=LABEL_2, width=17, padx=5, pady=5)
		self.label_cont.grid(row=2, column=3, sticky=NW, padx=10, pady=10)

		self.frame_contactos = Contenedor(self.ventana.ventana, width=130,
								height=280, bg=FONDO_CONTACTOS,
								highlightbackground=FONDO_CONTACTOS,
								highlightcolor=FONDO_CONTACTOS,
								highlightthickness=1)
		self.frame_contactos.grid(row=3, rowspan=2, column=3, padx=0, pady=0)

		etiqueta_prueba = Label(self.frame_contactos.interior,
								text="Lista de contactos", bg=FONDO_CONTACTOS)
		etiqueta_prueba.pack()

		# BLOQUE CHAT

		self.label_contacto = Label(self.ventana.ventana, text="Chat con: ",
									bg=PRIMARIO, fg=LABEL_2, width=30, padx=5,
									pady=5, anchor=W, font="Ubuntu 13 bold")
		self.label_contacto.grid(row=2, column=0, columnspan=3, sticky=W,
															padx=20, pady=10)

		self.frame_chat = Contenedor(self.ventana.ventana, width=300, height=50,
									bg=FONDO_CHAT, highlightbackground=FONDO_CHAT,
									highlightcolor=FONDO_CHAT,highlightthickness=1)
		self.frame_chat.grid(row=3, column=0, rowspan=2, columnspan=3, padx=0,
							pady=0)

		etiqueta_prueba = Label(self.frame_chat.interior, text=" ", bg=FONDO_CHAT)
		etiqueta_prueba.grid(row=0, column=0, sticky=E)

		# BLOQUE MENSAJE

		self.mensaje = StringVar(self.ventana.ventana)
		self.campo_mensaje = CajaTexto(ventana=self.ventana.ventana,
					variable=self.mensaje, tamano=31, fuente=(FUENTE_PRED, 13))
		self.campo_mensaje.caja_texto.bind('<Return>', self.bind_enter_enviar)

		self.campo_mensaje.invocar_grid(5,0,1,3,x=20,y=10)

		# BOTONES SALIR - ENVIAR

		boton_enviar = Boton(ventana=self.ventana.ventana, nombre="Enviar",
							color=LABEL_2, fondo=PRIMARIO,
							evento=lambda:self.enviar_mensaje(self.mensaje.get(),
												self.nick_contacto), tamano=36)

		boton_enviar.invocar_grid(6,0,1,3,x=20,y=0)

		boton_salir = Boton(ventana=self.ventana.ventana, nombre="Ver perfil",
							color=LABEL_2, fondo=PERFIL,
							evento=lambda: self.evento_ver_perfil(), tamano=15)
		boton_salir.invocar_grid(5,3,1,1,x=10,y=0,sticky=W)

		boton_salir = Boton(ventana=self.ventana.ventana, nombre="Salir",
							color=LABEL_2, fondo=CLOSE,
							evento=lambda: self.cerrar(), tamano=15)
		boton_salir.invocar_grid(6,3,1,1,x=10,y=0,sticky=W)

	def mostrar_login(self):
		''' Función que dibuja los widgets del login en la ventana
		'''
		self.ventana.centrar(300,150)
		etiqueta_titulo = Etiqueta(ventana=self.ventana.ventana,
									nombre="Ingrese los datos del usuario",
									color=LABEL_1, fuente=FUENTE_PRED,
									tamano="15")

		etiqueta_titulo.invocar_grid(0,0,1,2,sticky=W+E)

		self.nick = StringVar(self.ventana.ventana)
		self.password = StringVar(self.ventana.ventana)

		etiqueta_nick = Etiqueta(ventana=self.ventana.ventana,
								nombre="Nombre de usuario:", color=LABEL_1,
								fuente=FUENTE_PRED, tamano=10)
		etiqueta_nick.invocar_grid(3,0,sticky=E)

		box_nick = CajaTexto(ventana=self.ventana.ventana, variable=self.nick,
							tamano=20)
		box_nick.invocar_grid(3,1,sticky=W)
		box_nick.caja_texto.focus()

		etiqueta_password = Etiqueta(ventana=self.ventana.ventana,
								nombre="Contraseña:", color=LABEL_1,
								fuente=FUENTE_PRED, tamano=10)
		etiqueta_password.invocar_grid(4,0,sticky=E)

		box_password = CajaTexto(ventana=self.ventana.ventana,
										variable=self.password, tamano=20)
		box_password.caja_texto.bind('<Return>', self.bind_evento_login)
		box_password.tipo_password()
		box_password.invocar_grid(4,1,sticky=W)

		boton_login = Boton(ventana=self.ventana.ventana,
						nombre="Iniciar sesión", color=LABEL_2,
						fondo=PRIMARIO, evento=lambda: self.evento_login(\
									[self.nick.get(), self.password.get()]))
		boton_login.invocar_grid(5,0,1,1)

		boton_registro = Boton(ventana=self.ventana.ventana,
						nombre="Registrarse", color=LABEL_2,
						fondo=SECUNDARIO, evento=lambda: self.evento_registrarse())
		boton_registro.invocar_grid(5,1,1,1)

	def verificar_mensaje(self, mensaje, texto=''):
		''' Funcion recursiva que separa en varias lineas un texto segun el
			MAX_CARACTERES por linea
		'''
		# caso base
		if len(mensaje) <= MAX_CARACTERES:
			texto = texto + mensaje[0:]
			return texto
		else:
			# trabajo
			texto = texto + mensaje[0:MAX_CARACTERES] + "\n"
			# recursión
			return self.verificar_mensaje(mensaje[MAX_CARACTERES:], texto)

	def enviar_mensaje(self, mensaje, nick_contacto):
		'''	Función que recibe el mensaje a enviar y el receptor del mensaje,
			primero valida que el campo del nick no esté vacio, en este caso
			notifica al usuario que se debe especificar un contacto primero,
			y en caso de que el nick sea especificado se procede a graficar el
			mensaje en el contenedor para luego a traves del controlador enviar
			al servidor la petición de envío del mensaje
		'''
		if not(mensaje and mensaje.strip()):
			return

		if nick_contacto == '':
			PopupError("Usuario desconocido", "Primero debes seleccionar un\
						contacto")
			self.campo_mensaje.resetear()
		else:
			texto = self.verificar_mensaje(mensaje)
			espaciado = Label(self.frame_chat.interior, text=ESPACIADO,\
								bg=FONDO_CHAT)
			espaciado.grid(row=self.row, column=1)
			label_mensaje = Label(self.frame_chat.interior, text=texto,
									fg=LABEL_2, bg=SECUNDARIO, padx=10, pady=10,
									anchor=W, width=MAX_CARACTERES)
			label_mensaje.grid(row=self.row, column=2, pady=5, sticky=E)
			self.row = self.row + 1
			self.controlador.enviar_mensaje([nick_contacto, mensaje])
			self.actualizar_scroll_chat()
			self.campo_mensaje.resetear()

	def bind_enter_enviar(self, evento):
		''' Función que recibe el evento 'Enter' al enviar el mensaje, el cual
			llama al evento enviar mensaje
		'''
		self.enviar_mensaje(self.mensaje.get(), self.nick_contacto)

	def bind_evento_conectarse(self, evento):
		''' Función que recibe el evento 'Enter' al conectarse al servidor,
			el cual llama al evento conectarse
		'''
		try:
			self.evento_conectarse([self.ddns.get(), int(self.puerto.get())])
		except ValueError:
			PopupError("Error", "El puerto no es válido")

	def bind_evento_login(self, evento):
		''' Función que recibe el evento 'Enter' al iniciar sesión, el cual
			llama al evento login
		'''
		self.evento_login([self.nick.get(), self.password.get()])

	def recibir_mensaje(self, mensaje, nick_contacto):
		''' Función que recibe el mensaje y el nick del contacto que envió el
		 	mensaje, para luego mostrarlo en el contenedor de los mensajes
		'''
		if self.nick_contacto == nick_contacto:
			texto = self.verificar_mensaje(mensaje)
			label_mensaje = Label(self.frame_chat.interior, text=texto,
										fg=LABEL_2, bg=PRIMARIO, padx=10, pady=10,
										anchor=W, width=MAX_CARACTERES)
			label_mensaje.grid(row=self.row, column=0, pady=5, sticky=W)
			self.row = self.row + 1
		elif self.nick_contacto != nick_contacto:
			for boton in self.buttons_contactos:
				if boton['text'] == nick_contacto:
					boton.config(bg=NOTIFICACION_FONDO, fg=NOTIFICACION_LETRA)
					if self.reproductor != None:
						self.reproductor.play()
					break
		self.actualizar_scroll_chat()

	def actualizar_mensajes(self, mensajes):
		''' Función que resetea el Contenedor de los mensajes, y muestra los
			mensajes que recibe por parametros
		'''
		self.clear_grid(self.frame_chat.interior)
		labels = []
		self.row = 0
		for i in mensajes:
			texto = self.verificar_mensaje(i.contenido, "")
			if i.emisor == self.datos_cuenta[0]:
				## ESPACIADO ##
				labels.append(Label(self.frame_chat.interior, text=ESPACIADO,
									bg=FONDO_CHAT))
				labels[-1].grid(row=self.row, column=1)

				## MENSAJE ENVIADO ##
				labels.append(Label(self.frame_chat.interior, text=texto,
									fg=LABEL_2, bg=SECUNDARIO, padx=10, pady=10,
									anchor=W, width=MAX_CARACTERES))
				labels[-1].grid(row=self.row, column=2, pady=5, sticky=E)
			else:
				## MENSAJE RECIBIDO ##
				labels.append(Label(self.frame_chat.interior, text=texto,
									fg=LABEL_2, bg=PRIMARIO, padx=10, pady=10,
									anchor=W, width=MAX_CARACTERES))
				labels[-1].grid(row=self.row, column=0, pady=5, sticky=W)
			self.row = self.row + 1

		self.actualizar_scroll_chat()

	def actualizar_scroll_chat(self):
		''' Función que actualiza el scroll del chat, es decir que al
			recibir o enviar mensajes, el scroll siempre va a ir bajando
		'''
		self.ventana.ventana.update()
		self.frame_chat.canvas.yview_moveto(0)
		self.ventana.ventana.update()
		self.frame_chat.canvas.yview_moveto(1)

	def chatear_con(self, nick_contacto):
		''' Función que recibe el nombre del contacto con el que se quiere
			chatear, lo que primero se hace es actualizar el color de estado del
			contacto ya que si es que el color estaba en rojo, al hacer click,
			se debe volver a poner su color de conectado o desconectado según el
			contacto, para luego cargar sus mensajes
		'''
		self.nick_contacto = nick_contacto
		contactos = self.controlador.listar_contactos()
		for button in self.buttons_contactos:
			if button['text'] == self.nick_contacto:
				for contacto in contactos:
					if contacto.nick == nick_contacto:
						if contacto.estado is True:
							button.config(bg=CONECTADO_FONDO,
															fg=CONECTADO_LETRA)
						else:
							button.config(bg=DESCONECTADO_FONDO,
														fg=DESCONECTADO_LETRA)
						break
				break	
		mensajes = self.controlador.listar_mensajes_contacto(nick_contacto)
		self.label_contacto.config(text="Chat con: " + nick_contacto)
		self.actualizar_mensajes(mensajes)

	def actualizar_contactos(self):
		''' Función que pide la lista de contactos del usuario al controlador,
			luego, si es la primera vez que se le muestran los contactos en
			esta sesión, se le mostrarán los contactos con su respectivo estado
			Verde (Conectado) o Gris (Desconectado) y el caso contrario, se
			revisará primero que el estado del contacto no esté en rojo
			(Mensaje pendiente) para poder actualizar los colores de Conectado
			o Desconectado
		'''
		contactos = self.controlador.listar_contactos()
		if self.buttons_contactos == []:
			self.clear_pack(self.frame_contactos.interior)
			for i in contactos:
				if i.estado is True:
					self.buttons_contactos.append(Button(self.frame_contactos.\
						interior, text=i.nick, fg=CONECTADO_LETRA, bg=CONECTADO_FONDO,
						width=15, command=partial(self.chatear_con,i.nick)))
				else:
					self.buttons_contactos.append(Button(self.frame_contactos.\
						interior, text=i.nick, fg=DESCONECTADO_LETRA,
						bg=DESCONECTADO_FONDO, width=15,
						command=partial(self.chatear_con, i.nick)))
				self.buttons_contactos[-1].pack()
		else:
			for boton in self.buttons_contactos:
				if boton['background'] != NOTIFICACION_FONDO:
					for contacto in contactos:
						if boton['text'] == contacto.nick:
							if contacto.estado is True:
								boton.config(bg=CONECTADO_FONDO,
															fg=CONECTADO_LETRA)
							else:
								boton.config(bg=DESCONECTADO_FONDO,
														fg=DESCONECTADO_LETRA)
			cant_contactos = len(contactos)
			cant_botones = len(self.buttons_contactos)
			diferencia = cant_contactos - cant_botones
			if diferencia > 0:
				for i in contactos[0-diferencia:]:
					if i.estado is True:
						self.buttons_contactos.append(Button(self.frame_contactos.interior,
							text=i.nick, fg=CONECTADO_LETRA, bg=CONECTADO_FONDO,
							width=15, command=partial(self.chatear_con, i.nick)))
					else:
						self.buttons_contactos.append(Button(self.frame_contactos.interior,
							text=i.nick, fg=DESCONECTADO_LETRA, bg=DESCONECTADO_FONDO,
							width=15, command=partial(self.chatear_con, i.nick)))
					self.buttons_contactos[-1].pack()

	def evento_guardar_perfil_editado(self, nombre, apellido, sexo, fecha):
		''' Función que recibe los datos nuevos del perfil, envia la solicitud
			al servidor mediante una función del controlador, y muestra
			el resultado al usuario
		'''
		res = self.controlador.actualizar_datos_perfil_usuario([nombre,\
													apellido, sexo, fecha])
		if res is True:
			Notificacion.mostrar_editar_perfil_exitoso()
		else:
			Notificacion.mostrar_editar_perfil_error()

	def evento_editar_perfil(self, ventana):
		''' Función que maneja el evento de editar el perfil, el cual recibe
		  	la ventana de *Ver perfil* y la cierra, para luego mostrar el
			formulario de edición de perfil
		'''
		ventana.salir()
		self.mostrar_editar_perfil_usuario()

	def evento_buscar(self, usuario):
		''' Función que recibe el nick del usuario a buscar y lo pasa al contro-
			lador para que realice la petición al servidor
		'''
		self.controlador.buscar_usuario(usuario)

	def evento_login(self, datos_cuenta):
		''' Función que recibe los datos de la cuenta para iniciar sesión
			(usuario, contraseña) luego llama al controlador para realice las
			peticiones al servidor de verificacion de credenciales, en caso
			de no ser validas, notifica al usuario, y en caso contrario, limpia
			la ventana, dibuja la de inicio de usuario e inicia el hilo de las
			notificaciones
		'''
		self.datos_cuenta = datos_cuenta
		res = self.controlador.iniciar_sesion(datos_cuenta[0], datos_cuenta[1],
															self.datos_servidor)
		if res is False:
			Notificacion.mostrar_login_error()
		else:
			self.clear_grid(self.ventana.ventana)
			self.mostrar_inicio_usuario()
			comunicador = self.controlador.post_comunicador_notificaciones()
			self.notificador = Notificacion(comunicador, self.frame_chat,
											self.frame_contactos, self)
			self.notificador.start()

	def evento_ver_perfil(self):
		''' Función que maneja el evento de ver perfil, el cual crea la ventana
			emergente con los datos del usuario
		'''
		self.mostrar_perfil_usuario()

	def evento_agregar(self, contacto):
		''' Función que maneja el evento para agregar un contacto, el cual
			recibe el nick del contacto a agregar y directamente llama al
			controlador para realizar la peticion al servidor de agregar el
			contacto
		'''
		self.controlador.agregar_contacto(contacto)

	def evento_registrarse(self):
		''' Función que maneja el evento registrarse el cual resetea la ventana
			y dibuja los elementos del registro
		'''
		self.clear_grid(self.ventana.ventana)
		self.mostrar_registrarse()

	def evento_ir_a_login(self):
		''' Función que maneja el evento de login el cual resetea la ventana
			y dibuja los elementos del login
		'''
		self.clear_grid(self.ventana.ventana)
		self.mostrar_login()

	def evento_proceso_registro(self, datos):
		''' Función que recibe los datos del usuario a registrarse, luego
			llama a una función del controlador para verificar si hubo un
			error al registrarse, para luego notificar si hay un error o no, y
			para el ultimo caso, redirigimos al usuario al login
		'''
		res = self.controlador.registro_usuario(datos, self.datos_servidor)
		if res is False:
			Notificacion.mostrar_registro_error()
		else:
			Notificacion.mostrar_registro_ok()
			self.evento_ir_a_login()

	def evento_conectarse(self, datos_servidor):
		''' Función que maneja el evento de conexión del servidor
			la cual recibe un vector con los datos del servidor atribuidos por
			el usuario, llama al controlador para verificar su validez
			y luego nos indica a modo de notificación su hubo un error con
			la conexión, en caso contrario, nos dirige al login
		'''
		self.datos_servidor = datos_servidor
		res = self.controlador.verificar_conexion_servidor(datos_servidor)
		if res is False:
			Notificacion.mostrar_error_servidor()
		else:
			self.evento_ir_a_login()


class Contenedor(Frame):
	''' A pure Tkinter scrollable frame that actually works!
	* Use the 'interior' attribute to place widgets inside the scrollable frame
	* Construct and pack/place/grid normally
	* This frame only allows vertical scrolling
	'''
	def __init__(self, parent, *args, **kw):
		Frame.__init__(self, parent, *args, **kw)
		vscrollbar = Scrollbar(self, orient=VERTICAL)
		vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
		self.canvas = Canvas(self, bd=0, highlightthickness=1,
						yscrollcommand=vscrollbar.set, width=kw['width'],
						bg=kw['bg'])
		self.canvas.pack(side=LEFT, fill=BOTH, expand=FALSE)
		vscrollbar.config(command=self.canvas.yview)
		self.canvas.xview_moveto(0)
		self.canvas.yview_moveto(1)
		self.interior = interior = Frame(self.canvas, bg=kw['bg'])
		interior_id = self.canvas.create_window(0, 0, window=interior, anchor=NW)

		def _configure_interior(event):
			size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
			self.canvas.config(scrollregion="0 0 %s %s" % size)
			if interior.winfo_reqwidth() != self.canvas.winfo_width():
				self.canvas.config(width=kw['width'])
		interior.bind('<Configure>', _configure_interior)

		def _configure_canvas(event):
			if interior.winfo_reqwidth() != self.canvas.winfo_width():
				self.canvas.itemconfigure(interior_id, width=kw['width'])
		self.canvas.bind('<Configure>', _configure_canvas)

class Notificacion(Thread):
	''' Clase para mostrar las notificaciones del sistema '''

	def __init__(self, comunicacion, frame_chat, frame_contactos, vista=None):
		''' Inicializa el hilo, el comunicador y el manejador
			de notificaciones (programacion funcional)
		'''
		Thread.__init__(self)
		self.vista = vista
		self.comunicacion = comunicacion
		self.frame_contactos = frame_contactos
		self.frame_chat = frame_chat

		self.manejador_notificaciones = {
			NOTIF_MENSAJE_RECIBIDO: self.mostrar_mensaje_recibido,\
			NOTIF_CONTACTO: self.mostrar_informacion_proceso_contacto,\
			NOTIF_DATOS_REGISTRO: self.mostrar_carga_datos,\
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

	def mostrar_resultados_busqueda(self, paquete):
		''' Método que notifica al usuario los resultados de su busqueda '''
		if paquete.usuario != []:
			self.vista.mostrar_resultados_busqueda(paquete.usuario)
		else:
			PopupExito("Resultados", "No hay resultados")

	@staticmethod
	def mostrar_editar_perfil_exitoso():
		''' Funcion que muestra la notificacion de la edicion de perfil
			exitoso
		'''
		PopupExito("Operación exitosa",
					"Se ha actualizado la información de perfil correctamente")

	@staticmethod
	def mostrar_editar_perfil_error():
		''' Función que muestra la notificacion de error al editar perfil '''
		PopupError("Error en la operación", "Ha ocurrido un error al editar los\
																		datos")

	def mostrar_carga_datos(self, extra=None):
		''' Método que manejará la notificacion que los datos del usuario han
			sido recibidos y procederá a actualizar su lista de contactos
		'''
		self.vista.actualizar_contactos()

	def mostrar_mensaje_recibido(self, mensaje):
		''' Método que maneja el mensaje recibido, llamando a la función de la
			vista que le mostrará al usuario la notificacion correspondiente
		'''
		self.vista.recibir_mensaje(mensaje.contenido, mensaje.emisor)

	def mostrar_informacion_proceso_contacto(self, extra):
		''' Funcion que recibe la respuesta del proceso de agregar contacto
			si se pudo agregar correctamente entonces muestra un mensaje de
			confirmacion, en caso contrario un mensaje de error
		'''
		if extra is True:
			Notificacion.mostrar_contacto_ok()
			self.vista.actualizar_contactos()
		else:
			Notificacion.mostrar_contacto_error()


	@staticmethod
	def mostrar_contacto_ok():
		''' Método estático que informa que el contacto fue agregado correcta-
			mente
		'''
		popup_exito = PopupExito("Operacion exitosa", "El contacto fue agregado correctamente")

	@staticmethod
	def mostrar_contacto_error():
		''' Método estático que reporta que falló el proceso de agregar el
			contacto debido a que el usuario no existe o ya ha sido agregado
			o que es uno mismo
		'''
		popup_error = PopupError("Error", "El usuario no existe o ya ha sido agregado")

	@staticmethod
	def mostrar_login_error():
		''' Método estático que reporta que el inicio de sesión ha sido inco-
			rrecto
		'''
		popup_error = PopupError("Error", "Usuario o contraseña inválidos")

	@staticmethod
	def mostrar_registro_ok():
		''' Método estático que informa que el registro ha sido exitoso '''
		popup_ok = PopupExito("Registro", "Usuario registrado exitosamente")

	@staticmethod
	def mostrar_registro_error():
		''' Método estático que reporta un error al registrar un usuario '''
		popup_ok = PopupError("Error", "Ha ocurrido un error en el proceso de registro")

	@staticmethod
	def mostrar_login_ok():
		''' Método estático que muestra en pantalla el inicio de sesión exitoso
		'''
		popup_ok = PopupExito("Inicio de sesión exitoso", "Los datos son correctos")

	@staticmethod
	def mostrar_error_servidor():
		''' Método estático que muestra en pantalla un error de conexión con el
			servidor
		'''
		popup_error = PopupError("Error", "Error de conexión con el servidor")

	@staticmethod
	def mostrar_exito_servidor():
		''' Método estático que muestra en pantalla la información de la
			conexión exitosa con el datos_servidor
		'''
		popup_error = PopupExito("Conexión exitosa", "La conexion con el servidor fue exitosa")

class PopupError():
	''' Ventana emergente que muestra el error pasado por parametros '''
	def __init__(self, titulo, subtitulo):
		self.popup_error = tkmsgbox.showerror(titulo, subtitulo)

class PopupExito():
	''' Ventana emergente que muestra la información pasada por parametros '''
	def __init__(self, titulo, subtitulo):
		self.popup_info = tkmsgbox.showinfo(titulo, subtitulo)

class Ventana:
	'''	Clase que representa una ventana principal de Tkinter '''

	def __init__(self, nombre):
		self.ventana = Tk()
		self.ventana.title(nombre)
		self.ventana['background'] = FONDO_VENTANA

	def invocar(self):
		''' Función que crea la ventana iniciando el bucle de eventos '''
		self.ventana.mainloop()

	def salir(self):
		''' Función que cierra la ventana '''
		self.ventana.destroy()

	def centrar(self, tamX, tamY):
		''' Función que dimensiona y centra la ventana según la pantalla
			en la que se está ejecutando
		'''
		frm_width = self.ventana.winfo_rootx() - self.ventana.winfo_x()
		win_width = tamX + 2 * frm_width
		titlebar_height = self.ventana.winfo_rooty() - self.ventana.winfo_y()
		win_height = tamY + titlebar_height + frm_width
		x = self.ventana.winfo_screenwidth() // 2 - win_width // 2
		y = self.ventana.winfo_screenheight() // 2 - win_height // 2
		self.ventana.geometry('{}x{}+{}+{}'.format(tamX, tamY, x, y))

class Boton():
	''' Clase que representa un botón de Tkinter (Button) '''
	def __init__(self, ventana, nombre, color, fondo, evento, tamano=0):
		self.boton = Button(ventana, text=nombre,
							fg= color, bg=fondo,
							command=evento, cursor="hand1", width=tamano)

	def invocar_grid(self,fila=0,columna=0,comb_fila=1,comb_columna=1, x=10, y=10, sticky=W+E):
		self.boton.grid(row=fila, column=columna,
						rowspan=comb_fila, columnspan=comb_columna, padx=x, pady=y,
						sticky=sticky)

	def invocar_pack(self, posicion = "centro"):
		if posicion == "centro" :
			self.boton.pack()
		elif posicion == "derecha" :
			self.boton.pack(side=RIGHT)
		elif posicion == "izquierda" :
			self.boton.pack(side=LEFT)

class Etiqueta():
	'''	Clase que representa las etiquetas de Tkinter (Label) '''
	def __init__(self, ventana, nombre, color, fuente, tamano, justify=CENTER,
					fondo=LABEL_FONDO, estilo="bold"):
		self.etiqueta = Label(ventana, text=nombre, fg=color, bg=fondo,
							font=(fuente + " " + str(tamano) + " " + estilo),
							justify=justify, anchor=NW)

	def invocar_place(self, pos_x=100, pos_y=100):
		self.etiqueta.place(x=pos_x, y=pos_y)

	def invocar_grid(self,fila=0,columna=0,comb_fila=1,comb_columna=1, sticky=W,
					x=5, y=5):
		self.etiqueta.grid(row=fila, column=columna, rowspan=comb_fila,
						columnspan=comb_columna, sticky=sticky, padx=x, pady=y)

	def invocar_pack(self, posicion = "centro"):
		if posicion == "centro" :
			self.etiqueta.pack()
		elif posicion == "derecha" :
			self.etiqueta.pack(side=RIGHT)
		elif posicion == "izquierda" :
			self.etiqueta.pack(side=LEFT)

class Seleccion:
	''' Clase que representa el OptionMenu de Tkinter '''
	def __init__(self, ventana, var, elementos):
		self.select = OptionMenu(ventana, var, *elementos)

	def invocar_pack(self):
		self.select.pack()

	def invocar_grid(self, fila, columna, columnspan=1, rowspan=1, x=0, y=0,
					sticky=W+E):
		self.select.grid(row=fila, column=columna, columnspan=columnspan,
							rowspan=rowspan, padx=x, pady=y, sticky=sticky)

class CajaTexto():
	''' Clase que representa las cajas de texto de Tkinter (Entry) '''

	def __init__(self, ventana, variable, tamano, fuente=(FUENTE_PRED, 10)):
		self.caja_texto = Entry(ventana, textvariable=variable, width=tamano,
								font=fuente)

	def tipo_password(self):
		''' Método para ocultar el contenido de lo que está siendo digitado '''
		self.caja_texto.config(show="*")

	def invocar_grid(self, fila, columna, comb_fila=1, comb_columna=1,
					sticky=W+E, x=0, y=0):
		''' Método que posiciona el Widget según una grilla, especificando
			la posición en la misma
		'''
		self.caja_texto.grid(row=fila, column=columna, padx=x, pady=y,
					rowspan=comb_fila, columnspan=comb_columna, sticky=sticky)

	def invocar_pack(self, posicion = "centro"):
		''' Método que posiciona el Widget ajustandose a la ventana y segun
			la posicion que se le pase en los argumentos
		'''
		if posicion == "centro" :
			self.caja_texto.pack()
		elif posicion == "derecha" :
			self.caja_texto.pack(side=RIGHT)
		elif posicion == "izquierda" :
			self.caja_texto.pack(side=LEFT)

	def resetear(self):
		''' Método que elimina el contenido del Entry '''
		self.caja_texto.delete(0, END)
