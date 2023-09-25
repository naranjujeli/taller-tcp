from tcp import Nodo, Estado, Flag
OK   = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

# Modificaciones nunca se pasa por el estado TIME_WAIT (se va directo a CLOSED) y no se pasa por el estado CLOSE_WAIT (se va al estado LAST_ACK)

def test1():
    # Test: El estado LISTEN funciona bien ante el flag SYN
    cliente = Nodo()
    servidor = Nodo(Estado.LISTEN)
    cliente.send(servidor, [Flag.SYN])

    # Se fija que al enviar el flag SYN a un nodo en estado LISTEN, este cambie a estado SYN_RCVD
    assert(servidor.estado == Estado.SYN_RCVD), f'El servidor no cambio a estado SYN_RCVD'

def test2():
    # Test: El estado SYN_SENT pasa a ESTABLISHED si se le envia un SYN + ACK
    cliente = Nodo(Estado.SYN_SENT)
    servidor = Nodo(Estado.LISTEN)
    servidor.send(cliente, [Flag.SYN, Flag.ACK])

    # Se fija que al enviar los flags SYN + ACK el cliente queda en estado ESTABLISHED
    assert(cliente.estado == Estado.ESTABLISHED), f'El cliente no cambio a estado ESTABLISHED'

def test3():
    # Test: El estado SYN_RCVD pasa a ESTABLISHED si se le envia un ACK
    cliente = Nodo()
    servidor = Nodo(Estado.LISTEN)
    cliente.send(servidor, [Flag.SYN])
    cliente.send(servidor, [Flag.ACK])

    # Se fija que al enviar el flag ACK el servidor queda en estado ESTABLISHED
    assert(servidor.estado == Estado.ESTABLISHED), f'El servidor no cambio a estado ESTABLISHED'

def test4():
    # Test: El estado LAST_ACK pasa a CLOSED si se le envia un ACK
    cliente = Nodo(Estado.ESTABLISHED)
    servidor = Nodo(Estado.ESTABLISHED)
    servidor.send(cliente, [Flag.FIN])
    servidor.send(cliente, [Flag.ACK])

    # Se fija que al enviar el flag ACK el cliente queda en estado CLOSED
    assert(cliente.estado == Estado.CLOSED), f'El cliente no cambio a estado CLOSED'

def test5():
    cliente = Nodo(Estado.ESTABLISHED)
    servidor = Nodo(Estado.FIN_WAIT_1)
    cliente.send(servidor, [Flag.FIN])
    
    # Se fija que al enviar el flag FIN el cliente queda en estado CLOSING
    assert(cliente.estado == Estado.CLOSING), f'El cliente no cambio a estado CLOSING'

def test6():
    cliente = Nodo(Estado.ESTABLISHED)
    servidor = Nodo(Estado.FIN_WAIT_1)
    servidor.send(cliente, [Flag.FIN])
    servidor.send(cliente, [Flag.ACK])
    
    # Se fija que al enviar el flag ACK el cliente queda en estado CLOSED
    assert(cliente.estado == Estado.CLOSED), f'El cliente no cambio a estado CLOSED'

def test7():
    cliente = Nodo(Estado.ESTABLISHED)
    servidor = Nodo(Estado.FIN_WAIT_1)
    cliente.send(servidor, [Flag.ACK])
    
    # Se fija que al enviar el flag ACK el servidor queda en estado FIN_WAIT_2
    assert(servidor.estado == Estado.FIN_WAIT_2), f'El servidor no cambio a estado FIN_WAIT_2'

def test8():
    cliente = Nodo(Estado.ESTABLISHED)
    servidor = Nodo(Estado.FIN_WAIT_1)
    cliente.send(servidor, [Flag.ACK])
    cliente.send(servidor, [Flag.FIN])
    
    # Se fija que al enviar el flag FIN el servidor queda en estado CLOSED
    assert(servidor.estado == Estado.CLOSED), f'El servidor no cambio a estado CLOSED'

def test():
    ### Invitacion a crear mas tests...
    pass



def correr_tests(*argv):
    for i, test in enumerate(argv):
        try:
            test()
            print(f'{OK}Test {i+1} esta bien!{ENDC}')
        except Exception as e:
            print(f'{FAIL}Error Test {i+1}: {str(e)}{ENDC}')

if __name__ == '__main__':
    correr_tests(
                test1,
                test2,
                test3,
                test4,
                test5,
                test6,
                test7,
                test8
                )
