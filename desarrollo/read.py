import network, time
from machine import Pin, SPI
import utime
import ujson
import ufirebase as firebase
import urequests
from mfrc522 import MFRC522
import umail
from utelegram import Bot
import sys

spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
spi.init()
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)

# Configuraciones de correo para emisor y receptor
sender_email = 'lasdeliciasdelcomelon@gmail.com'
sender_name = 'Las delicias del comelon'
sender_app_password = 'dwgb oetf hgqx jotm'
recipient_email = ''
recipient_email_admin = 'kjulianr41@gmail.com'
email_subject = ''

nueva_compra = {
    "Plato": "",
    "Precio": 0,
    "fecha": ""
}
 # token para la autenticacion del bot 
TOKEN = '6387781123:AAHiEKiDD6FhsavX0ChVS5NQe6UrviyMcNo'
bot = Bot(TOKEN)
 
# funcion para conectar red  
def conectaWifi(red, password):
    miRed = network.WLAN(network.STA_IF)

    if not miRed.isconnected():
        miRed.active(True)
        miRed.connect(red, password)
        print('Conectando a la red', red + "…")
        timeout = time.time() + 10  # Espera hasta 10 segundos para la conexión

        while not miRed.isconnected():
            if time.time() > timeout:
                print('Error: No se pudo conectar a la red')
                return False
            time.sleep(1)

    print('Conexión exitosa')
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    return True

def obtenerFecha():
    tiempo_actual = utime.time()
    fecha_hora_actual = utime.localtime(tiempo_actual)
    # Imprimir la fecha y hora formateadas
    formato_fecha_hora = "{:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d}".format(
        fecha_hora_actual[2], fecha_hora_actual[1], fecha_hora_actual[0],
        fecha_hora_actual[3], fecha_hora_actual[4], fecha_hora_actual[5]
    )
    return formato_fecha_hora

def enviarCorreo(datos_usuario, destinatario):
    
    nombres = datos_usuario.get("Nombres")
    apellidos = datos_usuario.get("Apellidos")
    cc = datos_usuario.get("CC")
    # Logica para armar tabla
    compras = datos_usuario.get("Compras", [])
    tabla = ""
    # Cabecera de la tabla condicionada
    if destinatario:
        tabla += f"Gracias {nombres} por tu visita! aqui esta tu cuenta\n\n"
    else:
        tabla += f"Cuenta actualizada para el cliente {nombres} {apellidos} con CC. {cc}\n\n"
    
    tabla += "Platos pedidos\t\t\tPrecio\t\t\tFecha y hora\t\t\n"
    tabla += "-" * 83 + "\n"  # Línea horizontal"
    
    if compras:
        # Inicializar la variable para la suma total
        total_precio = 0

        # Iterar sobre las compras y agregar cada fila a la tabla
        for compra in compras:
            plato = compra.get("Plato", "")
            precio = compra.get("Precio", "")
            fecha = compra.get("fecha", "")

            # Sumar el precio al total
            total_precio += precio
            
            # Formatear la fila de la tabla
            precio_formateado = "${:,.0f}".format(precio).replace(",", ".")
            fila = f"{plato}\t\t{precio_formateado}\t\t{fecha}\t\t\n"

            # Agregar la fila a la tabla
            tabla += fila

        # Agregar la fila con el total al final de la tabla
        tabla += "-" * 83 + "\n"
        tabla += f"Total\t\t${total_precio:,.2f}\t\t\n\n"
        
        # Imprimir la tabla
        print(tabla)
    else:
        tabla = "No hay compras registradas."
        print("No hay compras registradas.")

    if destinatario:
        recipient_email = datos_usuario.get("Correo")
        email_subject = f"Compra restaurante delicias del comelon exitosa"
        tabla += f"Consulta nuestra web https://lasdeliciaselcomelon.netlify.app/"
    else:
        recipient_email = sender_email
        email_subject = f"Actualizacion cuenta de {nombres} {apellidos}"
        
    # Send email once after MCU boots up
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)
    smtp.login(sender_email, sender_app_password)
    smtp.to(recipient_email)
    smtp.write("De:" + sender_name + "<"+ sender_email+">\n")
    smtp.write("Subject:" + email_subject + "\n")
    smtp.write(tabla)
    smtp.send()
    smtp.quit()        

def enviar_primer_mensaje(token, chat_id):
    base_url = f"https://api.telegram.org/bot{token}/sendMessage"
    mensaje = """ *Bienvenido nuevamente a Las delicias del comelon*
                  \n  _______________________________________
                  \n  Menu Especial Las delicias del comelon
                  \n  _______________________________________
                  \n  1- Mojarra Dorada.       Valor: $18.000 
                  \n  2- Arroz de Coco.        Valor: $15.000 
                  \n  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
                  \n  _______________________________________
                  \n  Menu Corriente Las delicias del comelon
                  \n  _______________________________________
                  \n  3- Pollo Frito.          Valor: $18.000 
                  \n  4- Carne Asada.          Valor: $15.000 
                  \n  5- Sobrebarriga.         Valor: $18.000 
                  \n  6- Milanesa De Pollo.    Valor: $15.000
                  \n  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
                  \n *Ingresa el numero del menu que vas a pedir hoy*
                  \n  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
                  \n
                  \n Visita nuestra web https://lasdeliciaselcomelon.netlify.app/ 
               """
    params = {
        "chat_id": chat_id,
        "text": mensaje
        }
    try:
        response = urequests.post(base_url, json=params)
        print("Mensaje enviado:", response.text)
    except Exception as e:
        print("Error al enviar mensaje:", e)

def responder_mensaje(token, chat_id, mensaje):
    base_url = f"https://api.telegram.org/bot{token}/sendMessage"
    mensaje = f"""\n {mensaje}.
                  \n Su cuenta llegara a su correo electronico.
                  \n Si desea pedir otro plato ingrese el numero, de lo contrario omita este mensaje.
                  """
    params = {
        "chat_id": chat_id,
        "text": mensaje
        }
    try:
        response = urequests.post(base_url, json=params)
        print("Respuesta enviada:", response.text)
    except Exception as e:
        print("Error al Responder:", e)
        
def chat_bot(chat_id, datos_usuario):
    @bot.add_message_handler("1")
    def help(update):
        nueva_compra = {}
        nueva_compra["Precio"] = 18000
        nueva_compra["Plato"] = "Mojarra Dorada."
        nueva_compra["fecha"] = obtenerFecha()
        responder_mensaje(TOKEN, chat_id, "Usted seleccionó Mojarra Dorada por un valor: $18.000")
        proceso_enviar_compra(nueva_compra, datos_usuario)
    
    @bot.add_message_handler("2")
    def help(update):
        nueva_compra = {}
        nueva_compra["Precio"] = 15000
        nueva_compra["Plato"] = "Arroz de Coco"
        nueva_compra["fecha"] = obtenerFecha()
        responder_mensaje(TOKEN, chat_id, "Usted seleccionó Arroz de Coco por un valor: $15.000") 
        proceso_enviar_compra(nueva_compra, datos_usuario)
    
    @bot.add_message_handler("3")
    def help(update):
        nueva_compra = {}
        nueva_compra["Precio"] = 18000
        nueva_compra["Plato"] = "Pollo frito"
        nueva_compra["fecha"] = obtenerFecha()
        responder_mensaje(TOKEN, chat_id, "Usted seleccionó Pollo frito por un valor: $18.000")
        proceso_enviar_compra(nueva_compra, datos_usuario)
    
    @bot.add_message_handler("4")
    def help(update):
        nueva_compra = {}
        nueva_compra["Precio"] = 15000
        nueva_compra["Plato"] = "Carne Asada"
        nueva_compra["fecha"] = obtenerFecha()
        responder_mensaje(TOKEN, chat_id, "Usted seleccionó Carne Asada por un valor: $15.000")
        proceso_enviar_compra(nueva_compra, datos_usuario)
    
    @bot.add_message_handler("5")
    def help(update):
        nueva_compra = {}
        nueva_compra["Precio"] = 18000
        nueva_compra["Plato"] = "Sobrebarriga"
        nueva_compra["fecha"] = obtenerFecha()
        responder_mensaje(TOKEN, chat_id, "Usted seleccionó Sobrebarriga por un valor: $18.000")
        proceso_enviar_compra(nueva_compra, datos_usuario)
    
    @bot.add_message_handler("6")
    def help(update):
        nueva_compra = {}
        nueva_compra["Precio"] = 15000
        nueva_compra["Plato"] = "Milanesa de pollo"
        nueva_compra["fecha"] = obtenerFecha()
        responder_mensaje(TOKEN, chat_id, "Usted seleccionó Milanesa de pollo por un valor: $15.000")
        proceso_enviar_compra(nueva_compra, datos_usuario)
        
        
    bot.start_loop()          
        
    
def proceso_enviar_compra(nueva_compra, datos_usuario):
    # Obtén la lista de compras actual
    compras = datos_usuario.get("Compras", [])
    
    # Asegúrate de tener una lista (incluso si está vacía)
    if not isinstance(compras, list):
        compras = []

    # Crea una copia de la lista de compras para evitar modificar la original
    compras_nuevas = compras.copy()
    
    # Se hace el push de la nueva compra
    compras_nuevas.append(nueva_compra)

    # Actualiza los datos del usuario con la nueva lista de compras
    datos_usuario["Compras"] = compras_nuevas

    # Actualiza los datos del usuario en Firebase
    firebase.put(card_id, datos_usuario, bg=0)
    print("Compra agregada exitosamente.")
    
    # Envía el correo electrónico
    enviarCorreo(datos_usuario, True)
    enviarCorreo(datos_usuario, False)
    
    
if conectaWifi("ETB2022", "Familia2022"):
    
    print("Acerque su tarjeta")    
    firebase.setURL("https://restoguard-db-default-rtdb.firebaseio.com/")
    
    while True:    
        (stat, tag_type) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                card_id = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                print(f"card_id: {card_id}")
                
                # Obtiene los datos actuales del usuario

                firebase.get(card_id, "datos", bg=0)
                datos_usuario = firebase.datos
                
                # Extraer el valor de "chat_id"
                chat_id = datos_usuario.get("chat_id")
                
                # Enviamos el primer mensaje a telegram                
                enviar_primer_mensaje(TOKEN, chat_id)                   
                chat_bot(chat_id, datos_usuario)                
                print("Finaliza el loop")
else:
       print ("Imposible conectar")
       miRed.active (False)
