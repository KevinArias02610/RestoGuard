# Funciones varias RFID
# Programa diseñado por Wilson Perez
# ____________________Módulos_______________________________________________

from machine import Pin, SPI 
import mfrc522
from time import *
# ____________________Objetos_______________________________________________

spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
spi.init()
rdr = mfrc522.MFRC522(spi=spi, gpioRst=13, gpioCs=5)
led = Pin(2, Pin.OUT)


# ____________________Funciones_______________________________________________

#------------------------------------------------------------------------------------
# Primera función para leer tarjeta y saber su Id
#------------------------------------------------------------------------------------
idTarjeta = "uid: 0x03fca3a7"

def leer_id():
    Tarjeta = 'None'
    print("Acerque la tarjeta por favor")
    while Tarjeta == 'None':
        (stat, tag_type) = rdr.request(rdr.REQIDL)    
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                #print("type: 0x%02x" % tag_type)
                Tarjeta = ("uid: 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1],
                                                        raw_uid[2], raw_uid[3]))
                print("Tarjeta detectada, el código es: ", Tarjeta)
                sleep(0.5)
# Para comparar el ID de la tarjeta con el que se tiene en el string

                if idTarjeta == Tarjeta:
                    print("Coincide su identificación de la tarjeta")
                    led.on()
                    sleep(5)
                    led.off()
                else:
                    print("No coincide su identificación")
                    led.off()
#------------------------------------------------------------------------------------
# Segunda función para leer su llave y saber su Id
#------------------------------------------------------------------------------------
idsecret = "uid: 0x43f3b192"

def leer_id2():
    Llave = 'None'
    print("Acerque la Llave")
    while Llave == 'None':
        (stat, tag_type) = rdr.request(rdr.REQIDL)    
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                
                #print("type: 0x%02x" % tag_type)
                Llave = ("uid: 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1],
                                                        raw_uid[2], raw_uid[3]))
                print("Llave detectada, el código es: ", Llave)

# Para comparar el ID de la tarjeta con el que se tiene en el string

                if idsecret == Llave:
                    print("Coincide su identificación de la tarjeta")
                    led.on()
                    sleep(5)
                    led.off()
                else:
                    print("No coincide su identificación")
                    led.off()

