"""
27/11/2023

Práctica del examen para realizar en casa
-----------------------------------------

* El programa debe estar correctamente documentado.

* Debes intentar ajustarte lo máximo que puedas a lo que se pide en los comentarios TODO.

* Tienes libertad para desarrollar los métodos o funciones que consideres, pero estás obligado a usar como mínimo todos los que se solicitan en los comentarios TODO.

* Además, tu programa deberá pasar correctamente las pruebas unitarias que se adjuntan en el fichero test_agenda.py, por lo que estás obligado a desarrollar los métodos que se importan y prueban en la misma: pedir_email(), validar_email() y validar_telefono()

"""

import os
import pathlib
from os import path

# Constantes globales
RUTA = pathlib.Path(__file__).parent.absolute() 

NOMBRE_FICHERO = 'contactos.csv'

RUTA_FICHERO = path.join(RUTA, NOMBRE_FICHERO)

#TODO: Crear un conjunto con las posibles opciones del menú de la agenda
OPCIONES_MENU = {1,2,3,4,5,6,7,8}
#TODO: Utiliza este conjunto en las funciones agenda() y pedir_opcion()


def borrar_consola():
    """ Limpia la consola
    """
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")


def meter_telefonos(lista, diccionario):
    telefonos = []
    if "@" not in lista[-1]:
                cont = 0
                for i in lista[3:]:
                    telefonos.append(i)
                    diccionario['telefonos'] = telefonos
                    cont += 1
    if "@" in lista[-1]:
        diccionario['telefonos'] = telefonos


def cargar_contactos(contactos: list):
    """ Carga los contactos iniciales de la agenda desde un fichero
    ...
    """
    #TODO: Controlar los posibles problemas derivados del uso de ficheros...
    with open(RUTA_FICHERO, 'r') as fichero:
        for linea in fichero:
            linea = linea.replace("\n", "")
            lista = linea.split(";")
            diccionario = dict([("nombre", lista[0]), ("apellido", lista[1]), ("email", lista[2])])
            meter_telefonos(lista, diccionario)
            contactos.append(diccionario)


def pedir_nombre():
    nombre = input("Introduce el nombre del contacto: ").title()
    while nombre == "" or nombre == " ":
        print("**ERROR** vuleve a intentarlo.")
        nombre = input("Introduce el nombre del contacto: ").title()
    return nombre


def validar_email(email_nuevo, contactos,  noce = True):
    for i in contactos:
        if email_nuevo.lower() in contactos[i]['email']:
            noce = True
            raise ValueError("el email ya existe en la agenda")
    if email_nuevo == "" or email_nuevo == " ":
        noce = False
        raise ValueError("el email no puede ser una cadena vacía")
    if "@" not in email_nuevo:
        noce = False
        raise ValueError("el email no es un correo válido")


def pedir_email(email:set):
        email_nuevo = input("Introduce el email del contacto: ")
        while email_nuevo.lower() in email or email_nuevo == "" or email_nuevo == " " or "@" not in email_nuevo:
            try:
                validar_email(email_nuevo, email)
            except ValueError as e:
                print(e)
                email = input("Introduce el email del contacto: ")
                return email_nuevo
            else:
                email.add(email_nuevo)
                return email_nuevo


def validar_telefono(telefono:str) -> bool:
    if len(telefono) == 9 or len(telefono) == 12 and "+34" in telefono and telefono[1:].isdigit() == True:
        return True
    else:
        print("**ERROR** formato de telefono no válido.")
        return False


def pedir_telefono():
    lista_telefonos= []
    cont = 1
    print("Introduce los teléfonos (ENTER para salir)")
    telefono = input(f"Teléfono {cont}: ").replace(" ", "")
    if telefono == "":
        print("No has introducido ningún teléfono para el contacto.")
    while telefono != "":
        if validar_telefono(telefono):
            lista_telefonos.append(telefono)
            cont += 1
        telefono = input(f"Teléfono {cont}: ").replace(" ", "")
    return lista_telefonos


def agregar_contacto(contactos:list, email):
    pregunta = "n"
    while pregunta != "s" and pregunta != "si":
        nombre = pedir_nombre()
        apellido = input("Introduce el apellido del contacto: ").capitalize()
        email_nuevo = pedir_email(email)
        telefono = pedir_telefono()
        pregunta = preguntas("¿Está seguro que quiere añadir este contacto? (s/si/n/no) ")
    contactos.append(dict([("nombre", nombre), ("apellido", apellido), ("email", email_nuevo), ("telefonos", telefono)]))
    print(f"Se ha añadido a {nombre} con éxito.")


def buscar_contacto(contactos, buscador):
    cont = 0
    for i in contactos:
        if buscador not in i['email'] and cont == len(contactos):
            return None
        if i['email'] == buscador:
            return cont
        cont += 1


def eliminar_contacto(contactos: list, email: str):
    """ Elimina un contacto de la agenda
    ...
    """
    try:
        #TODO: Crear función buscar_contacto para recuperar la posición de un contacto con un email determinado
        buscador = input("Introduce el email del contacto: ")
        pos = buscar_contacto(contactos, buscador)
        pregunta= preguntas("Seguro que quiere eliminar este contacto? (s/si/n/no) ")
        if pos != None and pregunta == "si" or pregunta == "s":
            del contactos[pos]
            print("Se eliminó 1 contacto")
        else:
            print("No se encontró el contacto para eliminar")
    except Exception as e:
        print(f"**Error** {e}")
        print("No se eliminó ningún contacto")


def ordenar_por_nombre(contactos:list):
    contactos_ordenados = contactos.copy()
    contactos_ordenadosv2= []
    contactos_ordenar = contactos.copy()
    for i in range(len(contactos)):
        cont2 = 0
        while cont2 < len(contactos_ordenar):
            if contactos_ordenados[i]['nombre'] > contactos_ordenar[cont2]['nombre']:
                contactos_ordenadosv2.append(contactos_ordenar[cont2])
                del contactos_ordenar[cont2]
            cont2 +=1
    contactos_ordenadosv2.append(contactos_ordenar[0])
    return contactos_ordenadosv2


def mostrar_telefonos_34(j):
    a = [j[:3]]
    b = [j[3:]]
    a.append("-")
    c = a + b
    d = "".join(c)
    j = d
    return j


def mostrar_contactos(contactos:list):
    contactos_ordenados = ordenar_por_nombre(contactos)
    print(f'AGENDA ({len(contactos)})')
    print("-" * 6)
    for i in contactos_ordenados:
        print(f"Nombre: {i['nombre']} {i['apellido']} ({i['email']})")
        if i['telefonos'] == []:
            print(f'Teléfonos: ninguno')
        else:
            cont = 1
            print("Teléfonos: ", end="")
            for j in i['telefonos']:
                if "+34" in j:
                    j = mostrar_telefonos_34(j)
                if cont < len(i['telefonos']):
                    print(f'{j} / ', end="")
                elif cont == len(i['telefonos']):
                    print(f'{j}')
                cont += 1
        print('.' * 6)


def menu_modificar(contactos: list,pos:int):
    borrar_consola()
    print(f"CONTACTO: {contactos[pos]['nombre']} {contactos[pos]['apellido']}")
    print("-" * 19)
    print("1. Cambiar nombre")
    print("2. Cambiar apellido")
    print("3. Cambiar email")
    print("4. Añadir teléfono")
    print("5. Borrar teléfono")
    print("6. Salir\n")


def modificar_contacto(contactos: list, email: set):
    buscador = input("Introduce el email del contacto: ")
    pos = buscar_contacto(contactos, buscador)
    opcion = 0
    while opcion != 6:
        menu_modificar(contactos,pos)
        opcion = pedir_opcion()
        if opcion == 1:
            contactos[pos]['nombre'] = pedir_nombre()
        elif opcion == 2:
            contactos[pos]['apellido'] = input("Introduce el nuevo apellido: ")
        elif opcion == 3:
            contactos[pos]['email'] = pedir_email(contactos[pos]['email'], email)
        elif opcion == 4:
            contactos[pos]['telefonos'] = pedir_telefono()
        elif opcion == 5:
            contactos[pos]['telefonos'].clear()
        elif opcion != 1 and  opcion != 2 and  opcion != 3 and  opcion != 4 and  opcion != 5:
            print("**ERROR** opción errónea.")
            pulse_tecla_para_continuar()


def mostrar_por_criterio(contactos):
    criterio = input("Indique el criterio de búsqueda (nombre, apellido, email o teléfonos): ").lower().replace("é", "e")
    cont = 1
    while criterio != "nombre" and criterio != "apellido" and criterio != "email" and criterio != "telefonos":
        print("**ERROR** introduce un criterio válido.")
        criterio = input("Indique el criterio de búsqueda (nombre, apellido, email o teléfonos): ").lower().replace("é", "e")
    if criterio == "telefonos":
        print("AGENDA DE TELÉFONOS\n" + "-"*19)
        for elemento in contactos:
            if elemento['telefonos'] == []:
                print(f'Teléfonos del contacto {cont}: Este contacto no tiene teléfonos registrados.')
            else:
                print(f'Teléfonos del contacto {cont}: ' + ", ".join(elemento['telefonos']))
                cont += 1
    else:
        msj = f"AGENDA DE {criterio.upper()}S\n"
        print(msj + "-"*len(msj))
        for elemento in contactos:
            print(f"Contacto {cont}: {elemento[criterio]}")
            cont += 1


def vaciar_agenda(contactos:list):
    contactos.clear()
    print("Lista vaciada correctamente.")
    pulse_tecla_para_continuar()


def mostrar_menu():
    borrar_consola()
    print("AGENDA")
    print("-" * 6)
    print("1. Nuevo contacto")
    print("2. Modificar contacto")
    print("3. Eliminar")
    print("4. Vaciar agenda")
    print("5. Cargar agenda incial")
    print("6. Mostrar contactos por criterio")
    print("7. Mostrar la agenda completa")
    print("8. Salir\n")


def pedir_opcion():
    try:
        resultado = int(input("\n>> Seleccione una opción: "))
    except ValueError:
        return -1
    else:
        return resultado


def agenda(contactos: list, email: set):
    """ Ejecuta el menú de la agenda con varias opciones
    ...
    """
    #TODO: Crear un bucle para mostrar el menú y ejecutar las funciones necesarias según la opción seleccionada...
    opcion = 0
    while opcion != 8:
        mostrar_menu()
        opcion = pedir_opcion()

        #TODO: Se valorará que utilices la diferencia simétrica de conjuntos para comprobar que la opción es un número entero del 1 al 7
        diferencia = diferencia_simetrica()
        if opcion in diferencia:
            if opcion == 1:
                borrar_consola()
                agregar_contacto(contactos,email)
                pulse_tecla_para_continuar()
            elif opcion == 2:
                modificar_contacto(contactos,email)
            elif opcion == 3:
                borrar_consola()
                eliminar_contacto(contactos,email)
                pulse_tecla_para_continuar()
            elif opcion == 4:
                borrar_consola()
                vaciar_agenda(contactos)
            elif opcion == 5:
                cargar_contactos(contactos)
                print("Lista cargada correctamete.")
                pulse_tecla_para_continuar()
            elif opcion == 6:
                borrar_consola()
                mostrar_por_criterio(contactos)
                pulse_tecla_para_continuar()
            elif opcion == 7:
                borrar_consola()
                mostrar_contactos(contactos)
                pulse_tecla_para_continuar()
            else:
                print("**ERROR** opción errónea.")
                pulse_tecla_para_continuar()


def diferencia_simetrica() -> set: 
    diferencia = {8} ^ OPCIONES_MENU
    return diferencia


def pulse_tecla_para_continuar():
    """ Muestra un mensaje y realiza una pausa hasta que se pulse una tecla
    """
    print("\n")
    os.system("pause")


def guardar_email(contactos: list) -> set:
    email = set()
    for i in contactos:
        email.add(i['email'])
    return email

def preguntas(msj):
    pregunta = input(msj)
    while pregunta != "s" and pregunta != "si" and pregunta != "n" and pregunta != "no":
        print("**ERROR** entrada inválida")
        pregunta = input(msj)
    return pregunta


def main():
    """ Función principal del programa
    """
    borrar_consola()

    #TODO: Asignar una estructura de datos vacía para trabajar con la agenda
    contactos = []

    #TODO: Modificar la función cargar_contactos para que almacene todos los contactos del fichero en una lista con un diccionario por contacto (claves: nombre, apellido, email y telefonos)
    #TODO: Realizar una llamada a la función cargar_contacto con todo lo necesario para que funcione correctamente.
    cargar_contactos(contactos)

    email = guardar_email(contactos)
    #TODO: Crear función para agregar un contacto. Debes tener en cuenta lo siguiente:
    # - El nombre y apellido no pueden ser una cadena vacía o solo espacios y se guardarán con la primera letra mayúscula y el resto minúsculas (ojo a los nombre compuestos)
    # - El email debe ser único en la lista de contactos, no puede ser una cadena vacía y debe contener el carácter @.
    # - El email se guardará tal cuál el usuario lo introduzca, con las mayúsculas y minúsculas que escriba. 
    #  (CORREO@gmail.com se considera el mismo email que correo@gmail.com)
    # - Pedir teléfonos hasta que el usuario introduzca una cadena vacía, es decir, que pulse la tecla <ENTER> sin introducir nada.
    # - Un teléfono debe estar compuesto solo por 9 números, aunque debe permitirse que se introduzcan espacios entre los números.
    # - Además, un número de teléfono puede incluir de manera opcional un prefijo +34.
    # - De igual manera, aunque existan espacios entre el prefijo y los 9 números al introducirlo, debe almacenarse sin espacios.
    # - Por ejemplo, será posible introducir el número +34 600 100 100, pero guardará +34600100100 y cuando se muestren los contactos, el telófono se mostrará como +34-600100100. 
    #TODO: Realizar una llamada a la función agregar_contacto con todo lo necesario para que funcione correctamente.
    #agregar_contacto(contactos, email)


    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Realizar una llamada a la función eliminar_contacto con todo lo necesario para que funcione correctamente, eliminando el contacto con el email rciruelo@gmail.com
    eliminar_contacto(contactos, email)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Crear función mostrar_contactos para que muestre todos los contactos de la agenda con el siguiente formato:
    # ** IMPORTANTE: debe mostrarlos ordenados según el nombre, pero no modificar la lista de contactos de la agenda original **
    #
    # AGENDA (6)
    # ------
    # Nombre: Antonio Amargo (aamargo@gmail.com)
    # Teléfonos: niguno
    # ......
    # Nombre: Daniela Alba (danalba@gmail.com)
    # Teléfonos: +34-600606060 / +34-670898934
    # ......
    # Nombre: Laura Iglesias (liglesias@gmail.com)
    # Teléfonos: 666777333 / 666888555 / 607889988
    # ......
    # ** resto de contactos **
    #
    #TODO: Realizar una llamada a la función mostrar_contactos con todo lo necesario para que funcione correctamente.
    mostrar_contactos(contactos)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Crear un menú para gestionar la agenda con las funciones previamente desarrolladas y las nuevas que necesitéis:
    # AGENDA
    # ------
    # 1. Nuevo contacto
    # 2. Modificar contacto
    # 3. Eliminar contacto
    # 4. Vaciar agenda
    # 5. Cargar agenda inicial
    # 6. Mostrar contactos por criterio
    # 7. Mostrar la agenda completa
    # 8. Salir
    #
    # >> Seleccione una opción: 
    #
    #TODO: Para la opción 3, modificar un contacto, deberás desarrollar las funciones necesarias para actualizar la información de un contacto.
    #TODO: También deberás desarrollar la opción 6 que deberá preguntar por el criterio de búsqueda (nombre, apellido, email o telefono) y el valor a buscar para mostrar los contactos que encuentre en la agenda.
    agenda(contactos,email)


if __name__ == "__main__":
    main()