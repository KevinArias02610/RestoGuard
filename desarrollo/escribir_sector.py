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
def escribir_sector(direc = 1, datos = bytearray(16)):
    print("Coloque la tarjeta o llave para cambiar su información")
    while True:      
        if type(datos) == type('str'):
            if len(datos) == 16:
                dat = bytes(datos, 'utf-8')
            else:
                completa = datos + " " * (16 - len(datos))
                dat = bytes(completa, 'utf-8')
        elif type(datos) == type(bytearray(1)):
            dat = datos
        else:
            dat = bytearray(datos)      
        (stat, tag_type) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                print("Tarjeta detectada")
                print("  - tag type: 0x%02x" % tag_type)
                print("  - uid: 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1],
                                                       raw_uid[2], raw_uid[3]))
                print("")
                if rdr.select_tag(raw_uid) == rdr.OK:
                    key = b'\xff\xff\xff\xff\xff\xff'                
                    if rdr.auth(rdr.AUTHENT1A, direc, key, raw_uid) == rdr.OK:
                        stat = rdr.write(direc, dat)
                        rdr.stop_crypto1()
                        if stat == rdr.OK:
                            print("Datos escritos en la tarjeta")
                            led.on()
                            sleep(2)
                            led.off()
                            break
                        else:
                            print("Proceso de escritura fallido")
                    else:
                        print("Error de autenticación")
                else:
                    print("Falla con el Tag")


datos_str = "Miriam Suarez"
escribir_sector(2, datos_str)
led.off()
sleep(3)                   
