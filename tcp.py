from enum import Enum

class Estado(Enum):
    CLOSED = 1
    LISTEN = 2
    SYN_RCVD = 3
    SYN_SENT = 4
    ESTABLISHED = 5
    FIN_WAIT_1 = 6
    FIN_WAIT_2 = 7
    CLISING = 8
    TIME_WAIT = 9
    CLOSE_WAIT = 10
    LAST_ACK = 11

    def __str__(self):
        return f'{self.name}'

class Flag(Enum):
    ACK = 1
    FIN = 2
    SYN = 3

    def __str__(self):
        return f'{self.name}'

class Nodo(object):
    def __init__(self, estado_inicial=None):
        # Variable que guarda el estado del nodo, inicialmente estan cerrados
        self.estado = estado_inicial if estado_inicial else Estado.CLOSED

        # Variable que guarda a que nodo esta conectado este
        self.conectado = None

    def esta_conectado(self):
        ### Completar
        pass

    # Esta funcion manda un paquete TCP, con flags, a otro Nodo
    def send(self, destinatario, flags):
        destinatario.receive(self, flags)
        self.estado = Estado.SYN_SENT

    # Esta funcion se ejecuta cuando un nodo recibe un paquete TCP.
    # Dependiendo que flags tenga el paquete, va a hacer una cosa u otra
    def receive(self, emisor, flags):
        if flags[0] == Flag.SYN:
            # TODO Checkear estado actual
            self.estado = Estado.SYN_RCVD

    # Hace que este nodo se conecte con el nodo 'destinatario'
    # Esto significa pasar de estado CLOSED a ESTABLISHED,
    # pasando por todos los pasos del protocolo TCP.
    def handshake(self, destinatario):
        ### Completar
        pass

    # Hace que este nodo se desconecte del nodo conectado
    # Esto significa pasar de estado ESTABLISHED a CLOSED,
    # pasando por todos los pasos del protocolo TCP. 
    def close(self, destinatario):
        ### Completar
        pass
