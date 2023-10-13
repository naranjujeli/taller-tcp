# Taller TCP de la materia Programación sobre Redes

Este pequeño y sencillo proyecto pretende simular los pasos del proceso de conexión y desconexión vía TCP. Implementa la máquina de estados que se puede encontrar en [RFC 739](https://www.rfc-es.org/rfc/rfc0793-es.txt).

En breves palabras, el algoritmo crea dos objetos de la clase `Nodo` y los hace interactuar enviándose paquetes TCP. Esto puede ser tanto con el objetivo de establecer una conexión como el de cerrarla.