import mfrc522
from machine import Pin,SPI
from utime import ticks_ms
import time


def lectura_tarjeta():
    spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
    spi.init()
    rdr = mfrc522.MFRC522(spi=spi, gpioRst=13, gpioCs=5)
    print("Por favor acerque la tarjeta")
    while True:
        (stat, tag_type) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()

            if stat == rdr.OK:
                print("Detectado, su Tag y su Id es: ")
                print("type: 0x%02x" % tag_type)
                print("uid: 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                print("")
                time.sleep(2)

                if rdr.select_tag(raw_uid) == rdr.OK:
                    key = b'\xff\xff\xff\xff\xff\xff'
                    ms = ticks_ms()
                    blockArray = bytearray(16)
                    for sector in range(1, 64):
                        if rdr.auth(rdr.AUTHENT1A, sector, key, raw_uid) == rdr.OK:
                            rdr.read(sector, into=blockArray)
                            print("data@%d: %s" % (sector, blockArray))
                        else:
                            print("Error de Autenticación")
                            break
                    rdr.stop_crypto1()

                    print("Lectura en " + str(ticks_ms() - ms)) # took 4594 ms
                    time.sleep(2)
                    break

                else:
                    print("Fallo de sección")
def lectura_llave():
    spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
    spi.init()
    rdr = mfrc522.MFRC522(spi=spi, gpioRst=13, gpioCs=5)
    print("Por favor acerque la llave")
    while True:
        (stat, tag_type) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()

            if stat == rdr.OK:
                print("Detectado, su Tag y su Id de la  llave es: ")
                print("type: 0x%02x" % tag_type)
                print("uid: 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                print("")
                time.sleep(2)

                if rdr.select_tag(raw_uid) == rdr.OK:
                    key = b'\xff\xff\xff\xff\xff\xff'
                    ms = ticks_ms()
                    blockArray = bytearray(16)
                    for sector in range(1, 64):
                        if rdr.auth(rdr.AUTHENT1A, sector, key, raw_uid) == rdr.OK:
                            rdr.read(sector, into=blockArray)
                            print("data@%d: %s" % (sector, blockArray))
                        else:
                            print("Error de Autenticación")
                            break
                    rdr.stop_crypto1()
                    

                    print("Lectura en " + str(ticks_ms() - ms)) # took 4594 ms
                    break

                else:
                    print("Fallo de sección")
lectura_tarjeta()
lectura_llave()