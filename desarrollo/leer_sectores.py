# Funciones varias RFID
# Programa diseñado por Wilson Perez
# ____________________Módulos_______________________________________________

from machine import Pin, SPI 
import mfrc522
from time import *
import time
# ____________________Objetos_______________________________________________

spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
spi.init()
rdr = mfrc522.MFRC522(spi=spi, gpioRst=13, gpioCs=5)
led = Pin(2, Pin.OUT)

# ____________________Funciones_______________________________________________
                    
def leer_sectores_tarjeta():
    Tarjeta = 'None'
    print("Coloca tarjeta para leer los sectores: ")
    while Tarjeta:        
        (stat, tag_type) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                print("Tarjeta detectada")
                print("type: 0x%02x" % tag_type)
                print("uid: 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1],
                                                   raw_uid[2], raw_uid[3]))
                print("")
                if rdr.select_tag(raw_uid) == rdr.OK:
                    key = b'\xff\xff\xff\xff\xff\xff'
                    ms = ticks_ms()
                    blockArray = bytearray(16)
                    for sector in range(0, 64):
                        if rdr.auth(rdr.AUTHENT1A, sector, key, raw_uid) == rdr.OK:
                            rdr.read(sector, into=blockArray)
                            print("datos@%d: %s" % (sector, blockArray))
                            led.on()
                            led.off()
                        else:
                            print("Error de autenticación")
                            break
                    rdr.stop_crypto1()
                    print("Datos leidos en: " + str(ticks_ms() - ms)) # took 4594 ms
                    break
                else:
                    print("Fallido")
leer_sectores_tarjeta()

def leer_sectores_llave():
    print("Coloca la llave para leer los sectores: ")
    time.sleep(2)
    Llave = 'None'
    while Llave:        
        (stat, tag_type) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                print("llave detectada")
                print("type: 0x%02x" % tag_type)
                print("uid: 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1],
                                                   raw_uid[2], raw_uid[3]))
                print("")
                if rdr.select_tag(raw_uid) == rdr.OK:
                    key = b'\xff\xff\xff\xff\xff\xff'
                    ms = ticks_ms()
                    blockArray = bytearray(16)
                    for sector in range(0, 64):
                        if rdr.auth(rdr.AUTHENT1A, sector, key, raw_uid) == rdr.OK:
                            rdr.read(sector, into=blockArray)
                            print("datos@%d: %s" % (sector, blockArray))
                            led.on()
                            led.off()
                        else:
                            print("Error de autenticación")
                            break
                    rdr.stop_crypto1()
                    print("Datos leidos en: " + str(ticks_ms() - ms)) # took 4594 ms
                    break
                else:
                    print("Fallido")
leer_sectores_llave()