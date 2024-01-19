import network, time
from machine import Pin
from utime import sleep, sleep_ms, ticks_us
from dht import DHT22
import ujson
from utelegram import Bot

rele= Pin(14, Pin.OUT)
sensor_dht = DHT22(Pin(4))

TOKEN = '6387781123:AAHiEKiDD6FhsavX0ChVS5NQe6UrviyMcNo'

bot = Bot(TOKEN)

def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True


if conectaWifi ("RedMan", "!QAZxsw2"):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())

    @bot.add_message_handler('Inicio')
    def help(update):
            update.reply('''Bienvenido a RestoGuard
                            \nSi se encuentra registrado ingrese la opcion Menu
                            \nSi no se encuentra registrado ingrese la opcion Registrar
                            ''')

     
    @bot.add_message_handler('Menu')
    def help(update):
        update.reply('''
                      Sistema de información Integral para el registro y Administración de ventas del restaurante:  
                       
                      \n***** Menu Especial RestoGuard *****
                      \n  1- Mojarra Dorada.      Valor: $18000 
                      \n  2- Arroz de Coco.        Valor: $15000 
                      
                      \n***** Menu Corriente RestoGuard *****
                      \n  3- Pollo Frito.                Valor: $12000 
                      \n  4- Carne Asada.            Valor: $12000 
                      \n  5- Sobrebarriga.            Valor: $12000 
                      \n  6- Milanesa De Pollo.   Valor: $12000
                      \n  Para continuar digite la palabra Opcion 
                      ''')

    @bot.add_message_handler('Opcion')
    def help(update):
        A = update.reply("Seleccione en numero de un producto:")
        if A == 1:
            update.reply("1 producto:")
    
      
    bot.start_loop()
       
        
    
 
else:
       print ("Imposible conectar")
       miRed.active (False)
       