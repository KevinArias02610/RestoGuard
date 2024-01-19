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


# ____________________Funciones_______________________________________________
idLlave = "uid: 0x43f3b192"

def leer_id_llave():
    Llave = 'None'
    print("Acerque la llave por favor")
    while Llave == 'None':
        (stat, tag_type) = rdr.request(rdr.REQIDL)    
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                #print("type: 0x%02x" % tag_type)
                codigo = ("uid: 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1],
                                                        raw_uid[2], raw_uid[3]))
                print("Llave detectada, el código es: ", codigo)
                sleep(0.5)
# Para comparar el ID de la tarjeta con el que se tiene en el string

                if idLlave == codigo:
                    print("Coincide su identificación de la Llave")
                    led.on()
                    sleep(5)
                    led.off()
                else:
                    print("No coincide su identificación")
                    led.off()
leer_id()
leer_id_llave()