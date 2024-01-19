print("******************************************************************************************************************************************************************")
print ("Sistema de información Integral  para el registro y Administración de ventas del restaurante")
print("Registro de Usuario")


Id = input("Ingrese su numero de documento: ")
Name = input("Ingrese su Nombre: ")
lastName = input("Ingrese sus Apellidos: ")
Email = input("Ingrese su correo: ")

    
print ("\nBienvenido a RestoGuard:  "+"\nSu Numero De Documento Es: " +Id+"\nSu Nombre es: "+Name+"\nSu Apellido es: "+lastName+"\n Su Correo Electronico es: "+Email)

print("\n*************** Bienvenido a RestoGuard: ***************")  
print("*************** Menu Especial RestoGuard ***************")  

print("1- Mojarra Dorada", "18000 pesos")
print("2- Arroz de Coco ", "15000 pesos")

print("*************** Menu Especial RestoGuard ***************")  

print("3- Pollo Frito", "12000 pesos")
print("4- Carne Asada", "12000 pesos")
print("5- Sobrebarriga", "12000 pesos")
print("6- Milanesa De Pollo", "12000 pesos")       

print("****************************")

while True:
    print("Ingrese el numero del Producto: ?")
    opcion = str(input("Ingrese si para solicitar el pedido: ").lower())
    print("Usted ingreso la opcion",opcion)
    
    if opcion== "si":
        print("Que tipo de Producto desas?")
        Menu = int(input("Ingrese la opcion que desea: "))
        if Menu == 1:
            print("Usted a solicitado: ", "Pollo Frito", "El valor es de 18000 pesos")
        print("Desea pagar en efectivo: ")
        ingreso1 = int(input("Ingrese el dinero:"))
        operacion = ingreso1 - 18000
        print("Usted a ingresado: ",ingreso1,"su saldo es: ",operacion)
        print("Espere unos minutos por favor: ")
        break
        if Menu == 2:
             print("Usted a solicitado: ", "Una Menu de carne", "El valor es de 15000 pesos")     