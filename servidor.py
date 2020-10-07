import socket
import time
import hashlib
import threading
import logging

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 65000))
s.listen(25)
opcion = 0
n=0
def recibir(cs, add):
    time.sleep(1)
    msg = cs.recv(1024).decode("Latin1")
    if len(msg)==0:
        return True
    global opcion
    string = "Recibido de: "+str(add[0]) + " El mensaje:    "+ msg 
    print(string)
    return False

def enviar(cs, add, string):
    time.sleep(1)
    msg = string
    msg = f'{len(msg):<5}' + msg
    cs.send(bytes(msg, "Latin1"))
    msg = "Enviado a:  " + str(add[0]) + " El mensaje:    "+ msg
    print(msg)

def sha2(message):
    m = hashlib.sha256()
    m.update(message)
    return m.digest()

def confirmacion(cs, add):
    msg = "[FIN] Gracias, por todo!"
    msg = f'{len(msg):<5}' + msg
    time.sleep(5)
    print("Recibido de: " + str(add[0]) + " El mensaje:   " + msg)

def threewayhs(clientsocket, address):
    while recibir(clientsocket, address):
        pass
    enviar(clientsocket,address, "[SYN] [ACK] Hola! Bienvenido.")
    while recibir(clientsocket, address):
        pass
    
def eleccion(clientsocket, address):
    if opcion == "1":
        logging.debug("Se enviará archivo 1. Tamaño: 100MiB")
        enviarHash(clientsocket, address, 1)
        while recibir(clientsocket, address):
            pass
        enviarArchivo100(clientsocket, address)
    if opcion == "2":
        logging.debug("Se enviará archivo 2. Tamaño: 250MiB")
        enviarHash(clientsocket, address, 2)
        while recibir(clientsocket, address):
            pass
        enviarArchivo250(clientsocket, address)

def enviarHash(cs, add, archive):
    if archive == 1:
        fil = open('100Mb.mp4','rb')
        hashcode = sha2(fil.read())
        enviar(cs, add, hashcode.decode("Latin1"))
        fil.close()
    if archive == 2:
        fil = open('250Mb.mp4','rb')
        hashcode = sha2(fil.read())
        enviar(cs, add, hashcode.decode("Latin1"))
        fil.close()

def enviarArchivo100(cs, add):
    b.wait()
    contadorPaquetes = 0
    video = open('100Mb.mp4','rb')
    print('Enviando paquetes a ',str(add[0]),'...')
    buff = video.read(4096)
    inicio = time.time()
    while (buff):
        contadorPaquetes += 1
        cs.send(buff)
        buff = video.read(4096)
    video.close()
    fin = time.time()
    tiempoEnvio = fin - inicio
    print("Envío completado.")
    print("Tiempo de envío: " + str(tiempoEnvio) + " Segundos.")

def enviarArchivo250(cs, add):
    b.wait()
    contadorPaquetes = 0
    video = open('250Mb.mp4','rb')
    print('Enviando paquetes a ',str(add[0]),'...')
    buff = video.read(4096)
    inicio = time.time()
    while (buff):
        contadorPaquetes += 1
        cs.send(buff)
        buff = video.read(4096)
    video.close()
    fin = time.time()
    tiempoEnvio = fin - inicio
    print("Envío completado.")

def atenderCliente(cs,add):
    threewayhs(cs, add)
    eleccion(cs, add)
    confirmacion(cs, add)
    cs.shutdown(socket.SHUT_WR)
    cs.close()

logging.basicConfig(filename='tmp.log',
                    format='%(levelname)s %(asctime)s :: %(message)s',
                    level=logging.DEBUG) 
n =  int(input ("¿A cuántos clientes quiere atender hoy?"))
opcion = input("Seleccione la opción del archivo que quiere enviar hoy: \n1. Archivo 100 Mib\n2. Archivo 250 MiB\n--->")   
b = threading.Barrier(n)
    
while True:
    clientsocket, address = s.accept()
    logging.debug("Se recibió un cliente con la dirección"+address[0])
    t = threading.Thread(target = atenderCliente, args = (clientsocket,address))
    t.start()




