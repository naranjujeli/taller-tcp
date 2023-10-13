from enum import Enum

class Estado(Enum):
    CLOSED = 1
    LISTEN = 2
    SYN_RCVD = 3
    SYN_SENT = 4
    ESTABLISHED = 5
    FIN_WAIT_1 = 6
    FIN_WAIT_2 = 7
    CLOSING = 8
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

        # enviando_primera_syn = self.estado == Estado.CLOSED and Flag.SYN in flags
        # enviando_syn_ack = self.estado == Estado.SYN_RCVD and (Flag.SYN in flags and Flag.ACK in flags)
        
        # if enviando_primera_syn:
        #     self.estado = Estado.SYN_SENT
        # elif enviando_syn_ack:
        #     self.estado = Estado.SYN_SENT

    # Esta funcion se ejecuta cuando un nodo recibe un paquete TCP.
    # Dependiendo que flags tenga el paquete, va a hacer una cosa u otra
    def receive(self, emisor, flags):
        syn_recibido = Flag.SYN in flags
        ack_recibido = Flag.ACK in flags
        fin_recibido = Flag.FIN in flags
        if self.estado == Estado.LISTEN: 
            if syn_recibido:
                # LISTEN recibe SYN
                self.estado = Estado.SYN_RCVD
        elif self.estado == Estado.SYN_SENT:
            if syn_recibido:
                if ack_recibido:
                    # SYN_SENT recibe SYN/ACK
                    self.estado = Estado.ESTABLISHED
                else:
                    # SYN_SENT recibe SYN
                    self.estado = Estado.SYN_RCVD
        elif self.estado == Estado.SYN_RCVD: 
            if ack_recibido:
                # SYN_RCVD recibe ACK
                self.estado = Estado.ESTABLISHED
        elif self.estado == Estado.ESTABLISHED:
            if fin_recibido:
                # ESTABLISHED recibe FIN
                self.estado = Estado.LAST_ACK
        elif self.estado == Estado.FIN_WAIT_1:
            if ack_recibido:
                # FIN_WAIT_1 recibe ACK
                self.estado = Estado.FIN_WAIT_2
            elif fin_recibido:
                # FIN_WAIT_1 recibe FIN
                self.estado = Estado.CLOSING
        elif self.estado == Estado.FIN_WAIT_2:
            if fin_recibido:
                # FIN_WAIT_2 recibe FIN
                self.estado = Estado.CLOSED
        elif self.estado == Estado.CLOSING:
            if ack_recibido:
                # CLOSING recibe ACK
                self.estado = Estado.CLOSED
        elif self.estado == Estado.LAST_ACK:
            if ack_recibido:
                # LAST_ACK recibe ACK
                self.estado = Estado.CLOSED


    # Hace que este nodo se conecte con el nodo 'destinatario'
    # Esto significa pasar de estado CLOSED a ESTABLISHED,
    # pasando por todos los pasos del protocolo TCP.
    def handshake(self, destinatario):
        self.send(destinatario, [Flag.SYN])
        self.estado = Estado.SYN_SENT
        destinatario.send(self, [Flag.SYN, Flag.ACK])
        self.send(destinatario, [Flag.ACK])

    # Hace que este nodo se desconecte del nodo conectado
    # Esto significa pasar de estado ESTABLISHED a CLOSED,
    # pasando por todos los pasos del protocolo TCP. 
    def close(self, destinatario):
        self.send(destinatario, [Flag.FIN])
        self.estado = Estado.FIN_WAIT_1
        destinatario.send(self, [Flag.ACK])
        destinatario.send(self, [Flag.FIN])
        destinatario.estado = Estado.LAST_ACK
        self.send(destinatario, [Flag.ACK])
