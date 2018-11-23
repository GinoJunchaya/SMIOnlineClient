from modelo.Usuario import Usuario
from Controlador import *

class AplicacionCliente:
    ''' Clase correspondiente a la aplicación '''

    def __init__(self):
        ''' Crea un objeto correspondiente al usuario que inició
            la aplicación
        '''
        self.usuario = Usuario()

    @staticmethod
    def salir():
        ''' Método estatico para finalizar el programa '''
        exit()

    def iniciar(self):
        ''' Método que crea el controlador pasandole el usuario e inicia
            la vista
        '''
        controlador = Controlador(self.usuario, AplicacionCliente.salir)
        controlador.iniciar_vista()

if __name__ == "__main__":
    app = AplicacionCliente()
    app.iniciar()
