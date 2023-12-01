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


def meter_telefonos(lista_contactos: list, dict_contactos:set):
    """Guarda los telefonos de los clientes en una lista
    Args:
        lista_contactos (list): una lista con los datos de los contactos
        dict_contactos (set): diccionario con los datos de los contactos
    """
    telefonos = []
    if "@" not in lista_contactos[-1]:
                cont = 0
                for i in lista_contactos[3:]:
                    telefonos.append(i)
                    dict_contactos['telefonos'] = telefonos
                    cont += 1
    if "@" in lista_contactos[-1]:
        dict_contactos['telefonos'] = telefonos


def cargar_contactos(contactos: list):
    """ Carga los contactos iniciales de la agenda desde un fichero
    Args:
        contactos (list): lista vacía  con todos los diccionarios con los datos de los contactos
    """
    #TODO: Controlar los posibles problemas derivados del uso de ficheros...
    with open(RUTA_FICHERO, 'r') as fichero:
        for linea in fichero:
            linea = linea.replace("\n", "")
            lista_contactos = linea.split(";")
            dict_contactos = dict([("nombre", lista_contactos[0]), ("apellido", lista_contactos[1]), ("email", lista_contactos[2])])
            meter_telefonos(lista_contactos, dict_contactos)
            contactos.append(dict_contactos)


def pedir_nombre()-> str:
    """Pide el nombre del contacto que se va a agregar
    Returns: 
        str: retorna el nombre que se haya introducido
    """
    nombre = input("- Introduce el nombre del contacto: ").title()
    while nombre == "" or nombre == " ":
        print("**ERROR** vuleve a intentarlo.")
        nombre = input("Introduce el nombre del contacto: ").title()
    return nombre


def validar_email(email_nuevo:str, email:set, comprobar:bool):
    """Valida si el email que se ha escrito tiene un formato correcto
    Args:
        email_nuevo (str): el email escrito y que se va a comprobar
        email (set): conjunto donde están los emails únicos
        comprobar (bool): booleano que indica si el email está o no está ya escrito
    """
    if email_nuevo == "" or email_nuevo == " ":
        comprobar = False
        raise ValueError("el email no puede ser una cadena vacía")
    elif email_nuevo.lower() in email:
        comprobar = True
        raise ValueError("el email ya existe en la agenda")
    elif "@" not in email_nuevo:
        comprobar = False
        raise ValueError("el email no es un correo válido")


def pedir_email(email:set):
        """Pide el email que se le va a añadir al contacto y lo valida
        Args:
            email (set): conjunto donde están los emails únicos
        Returns:
            str: retorna el email ya validado
        """
        email_nuevo = "a"
        while email_nuevo.lower() in email or email_nuevo == "" or email_nuevo == " " or "@" not in email_nuevo:
            email_nuevo = input("- Introduce el email del contacto: ")
            if email_nuevo in email:
                comprobar = True
            else:
                comprobar = False
            validar_email(email_nuevo, email, comprobar)
            if email_nuevo == "" or email_nuevo == " ":
                raise ValueError("el email no puede ser una cadena vacía")
            elif email_nuevo.lower() in email:
                raise ValueError("el email ya existe en la agenda")
            elif "@" not in email_nuevo:
                raise ValueError("el email no es un correo válido")
        email.add(email_nuevo)
        return email_nuevo


def validar_telefono(telefono:str) -> bool:
    """ Valida si el teléfono introducido está escrito correctamente
    Args: 
        telefono (str): el telefono introducido del contacto
    Returns:
        bool: retorna True si el teléfono está correctamente esctrito y False si no lo está
    """
    if len(telefono) == 9 or len(telefono) == 12 and "+34" in telefono and telefono[1:].isdigit() == True:
        return True
    else:
        print("**ERROR** formato de telefono no válido.")
        return False


def pedir_telefono()->set:
    """ Pide el telefono del contacto y lo valida
    Returns:
        list: retorna una lista con los telefonos del contacto y si no añade ninguna se retornará vacíca
    """
    lista_telefonos= []
    cont = 1
    print("- Introduce los teléfonos (ENTER para salir)")
    telefono = input(f"- Teléfono {cont}: ").replace(" ", "")
    if telefono == "":
        print("- No has introducido ningún teléfono para el contacto.")
    while telefono != "":
        if validar_telefono(telefono):
            lista_telefonos.append(telefono)
            cont += 1
        telefono = input(f"- Teléfono {cont}: ").replace(" ", "")
    return lista_telefonos


def agregar_contacto(contactos:list, email:set):
    """Agrega un nuevo contacto en la agenda y lo mete en la lista de contactos en forma de diccionario
    Args:
        contactos (list): lista vacía  con todos los diccionarios con los datos de los contactos
        email (set): conjunto donde están los emails únicos
    """
    print("AGREGAR CONTACTO\n" + "-"*16 + "\n")
    pregunta = "n"
    while pregunta != "s" and pregunta != "si":
        nombre = pedir_nombre()
        apellido = input("- Introduce el apellido del contacto: ").capitalize()
        correo = False
        while not correo:
            try:
                email_nuevo = pedir_email(email)
            except ValueError as e:
                print(e)
            else:
                correo = True
        telefono = pedir_telefono()
        pregunta = preguntas("\n¿Está seguro que quiere añadir este contacto? (s/si/n/no) ")
        if pregunta == "n" or pregunta == "no":
            borrar_consola()
    if nombre >= "L":
        contactos.append( dict([("nombre", nombre), ("apellido", apellido), ("email", email_nuevo), ("telefonos", telefono)]))
    if nombre < "L" :
        contactos.insert(0, dict([("nombre", nombre), ("apellido", apellido), ("email", email_nuevo), ("telefonos", telefono)]))
    print(f"\n>> Se ha añadido a {nombre} {apellido} con éxito.")


def buscar_contacto(contactos:list, buscador:str)->int:
    """Busca la posicion del contacto por el email introducido
    Args:
        contactos (list): lista vacía  con todos los diccionarios con los datos de los contactos
        buscador (str): entrada con el email que se quiere buscar
    Returns:
        int: retorna la posicion del email que se ha introducido
        None: retorna None si el email introducido ya está en los contactos
    """
    cont = 0
    for i in contactos:
        if buscador not in i['email'] and cont == len(contactos):
            return None
        if i['email'] == buscador:
            return cont
        cont += 1


def eliminar_contacto(contactos: list, email: str):
    """ Elimina un contacto de la agenda
    Args: 
        contactos (list): lista vacía  con todos los diccionarios con los datos de los contactos
        email (set): conjunto donde están los emails únicos
    """
    print("ELIMINAR CONTACTO\n" + "-"*16 + "\n")
    try:
        #TODO: Crear función buscar_contacto para recuperar la posición de un contacto con un email determinado
        buscador = input("- Introduce el email del contacto: ")
        pos = buscar_contacto(contactos, buscador)
        pregunta= preguntas("\nSeguro que quiere eliminar este contacto? (s/si/n/no) ")
        if pos != None and pregunta == "si" or pregunta == "s":
            del contactos[pos]
            email.remove(buscador)
            print("\n>> Se eliminó 1 contacto")
        else:
            print("No se eliminó ningún contacto")
    except Exception:
        print(f"\n**Error** Este contacto no existe en tu lista de contactos")
        print("No se eliminó ningún contacto")


def ordenar_por_nombre(contactos:list)->list:
    """ Crea una copia de los contactos y la ordena por los nombres
    Args: 
        contactos (list): lista vacía  con todos los diccionarios con los datos de los contactos
    Returns:
        list: retorna la lista ordenada 
    """
    contactos_ordenados= []
    contactos_ordenar = contactos.copy()
    for i in range(len(contactos)):
        cont2 = 0
        while cont2 < len(contactos_ordenar):
            if contactos[i]['nombre'] > contactos_ordenar[cont2]['nombre']:
                contactos_ordenados.append(contactos_ordenar[cont2])
                del contactos_ordenar[cont2]
            cont2 +=1
    contactos_ordenados.append(contactos_ordenar[0])
    return contactos_ordenados


def mostrar_telefonos_34(telefono:str)->str:
    """Añadir - a los telefonos delante de +34 para imprimirlos
    Args:
        telefono (str): el telefono que se va a modificar
    Returns:
        str: retorna el telefomo modificado para imprimirlo
    """
    prefijo = [telefono[:3]]
    numeros = [telefono[3:]]
    prefijo.append("-")
    lista_telefono = prefijo + numeros
    str_telefono = "".join(lista_telefono)
    telefonos = str_telefono
    return telefonos


def mostrar_contactos(contactos:list):
    """ Imprime por pantalla los contactos todos los contactos de la agenda
    Args: 
        contactos (list): lista vacía  con todos los diccionarios con los datos de los contactos
    """
    if contactos == []:
        print("No hay ningún contacto en la agenda.")
    else:
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
                for telefono in i['telefonos']:
                    if "+34" in telefono:
                        telefono = mostrar_telefonos_34(telefono)
                    if cont < len(i['telefonos']):
                        print(f'{telefono} / ', end="")
                    elif cont == len(i['telefonos']):
                        print(f'{telefono}')
                    cont += 1
            print('.' * 6)


def menu_modificar(contactos: list,pos:int):
    """ Imprime por pantalla el menú para modificar los contactos
    Args:
        contactos (list): lista vacía  con todos los diccionarios con los datos de los contactos
        pos (int): la posición del email que se ha buscado
    """
    borrar_consola()
    print(f"CONTACTO: {contactos[pos]['nombre']} {contactos[pos]['apellido']} ({contactos[pos]['email']}) Telefonos: ", end="")
    if contactos[pos]['telefonos'] == []:
        print(f'ninguno')
    else:
        print(", ".join(contactos[pos]['telefonos']))
    print("-" * 19)
    print("1. Cambiar nombre")
    print("2. Cambiar apellido")
    print("3. Cambiar email")
    print("4. Añadir teléfono")
    print("5. Borrar teléfonos")
    print("6. Salir\n")


def modificar_contacto(contactos: list, email: set):
    """ Pide el email del contacto a modificar y modifica sus datos según lo que quiera modificar
    Args:
        contactos (list): lista vacía  con todos los diccionarios con los datos de los contactos
        email (set): conjunto donde están los emails únicos
    """
    buscador = input("Introduce el email del contacto: ")
    pos = buscar_contacto(contactos, buscador)
    if pos != None:
        opcion = 0
        while opcion != 6:
            borrar_consola()
            menu_modificar(contactos,pos)
            opcion = pedir_opcion()
            if opcion == 1:
                contactos[pos]['nombre'] = pedir_nombre()
            elif opcion == 2:
                contactos[pos]['apellido'] = input("Introduce el nuevo apellido: ")
            elif opcion == 3:
                contactos[pos]['email'] = pedir_email(email)
            elif opcion == 4:
                contactos[pos]['telefonos'] = pedir_telefono()
            elif opcion == 5:
                contactos[pos]['telefonos'].clear()
            elif opcion != 1 and  opcion != 2 and  opcion != 3 and  opcion != 4 and  opcion != 5 and opcion != 6:
                print("**ERROR** opción errónea.")
                pulse_tecla_para_continuar()
    else:
        print("**ERROR** No se ha encontrado ningún contacto.")
        modificar_contacto(contactos, email)


def menu_por_criterio():
    """ Imprime por pantalla el menú para mostrar contactos por los criterios correspondientes
    """
    print("MOSTRAR CONTACTOS POR CRITERIOS\n" + "-"*31)
    print("1. Mostrar contactos por Nombre")
    print("2. Mostrar contactos por Apellido")
    print("3. Mostrar contactos por Email")
    print("4. Mostrar contactos por Télefono")
    print("5. Salir\n")


def mostrar_contactos_por_criterio(contactos:list, criterio:str, msj:str):
    """ Imprime por pantalla los contactos una vez pasados por el criterio de busqueda
    Args:
        contactos (list): lista vacía  con todos los diccionarios con los datos de los contactos
        criterio (str): cadena que indica como 
    """
    borrar_consola()
    msj_bonito = msj.replace("'","").upper()
    mensaje = f"CONTACTOR POR {msj_bonito}S\n"
    print(mensaje + "-"*len(mensaje))
    cont = 1
    for i in contactos:
        if criterio in i[msj]:
            print(f"CONTACTO {cont}: {i['nombre']} {i['apellido']}  ({i['email']})  ", end="")
            cont +=1
            cont2 = 1
            print("Teléfonos: ", end="")
            if i['telefonos'] == []:
                print(f'ninguno')
            else:
                for j in i['telefonos']:
                    if "+34" in j:
                        j = mostrar_telefonos_34(j)
                    if cont2 < len(i['telefonos']):
                        print(f'{j} / ', end="")
                    elif cont2 == len(i['telefonos']):
                        print(f'{j}')
                    cont2 += 1
    pulse_tecla_para_continuar()

def mostrar_por_criterio(contactos):
    """ muestra el menu, pide la ocion y ejecuta la opcion elegida
    Args: 
        contactos (list): lista vacía  con todos los diccionarios con los datos de los contactos
    """
    opcion = 0
    cont = 1
    while opcion != 5:
        borrar_consola()
        menu_por_criterio()
        try:
            opcion = int(input(">> Seleccione una opción: "))
        except ValueError:
            print("**ERROR** elige una de las opciones anteriores")
            pulse_tecla_para_continuar()
        else:
            if opcion == 1:
                criterio = input("Introduce una letra o palabra para mostrar los contactos: ")
                mostrar_contactos_por_criterio(contactos, criterio, 'nombre')
            elif opcion == 2:
                criterio = input("Introduce una letra o palabra para mostrar los contactos: ")
                mostrar_contactos_por_criterio(contactos, criterio, 'apellido')
            elif opcion == 3:
                criterio = input("Introduce una letra o palabra para mostrar los contactos: ")
                mostrar_contactos_por_criterio(contactos, criterio, 'email')
            elif opcion == 4:
                criterio = input("Introduce una letra o palabra para mostrar los contactos: ")
                borrar_consola()
                mensaje = f"CONTACTOR POR TÉLEFONOS\n"
                print(mensaje + "-"*len(mensaje))
                for i in contactos:
                    for j in i['telefonos']:
                        if criterio in j:
                            print(f"Contacto {cont}: {i['nombre']} {i['apellido']} {i['email']} ", end="")
                            cont +=1
                            cont2 = 1
                            print("Teléfonos: ", end="")
                            if i['telefonos'] == []:
                                print(f'ninguno')
                            else:
                                for j in i['telefonos']:
                                    if "+34" in j:
                                        j = mostrar_telefonos_34(j)
                                    if cont2 < len(i['telefonos']):
                                        print(f'{j} / ', end="")
                                    elif cont2 == len(i['telefonos']):
                                        print(f'{j}')
                                    cont2 += 1
                pulse_tecla_para_continuar()
            elif opcion != 1 and  opcion != 2 and  opcion != 3 and  opcion != 4 and opcion != 5:
                print("**ERROR** opción errónea.")
                pulse_tecla_para_continuar()


def vaciar_agenda(contactos:list):
    """Vacia la agenda entera
    Args:
        contactos (list): lista vacía  con todos los diccionarios con los datos de los contactos
    """
    contactos.clear()
    print("Lista vaciada correctamente.")
    pulse_tecla_para_continuar()


def mostrar_menu():
    """ Muestra por pantalla el menú principal de la agenda
    """
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
    """ Pide una opción del menu para elegir
    Returns:
        int: retorna un numero como resultado
    """
    try:
        resultado = int(input("\n>> Seleccione una opción: "))
    except ValueError:
        return -1
    else:
        return resultado


def agenda(contactos: list, email: set):
    """ Ejecuta el menú de la agenda con varias opciones
    Args:
        contactos (list): lista vacía  con todos los diccionarios con los datos de los contactos
        email (set): conjunto donde están los emails únicos
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
                borrar_consola()
                modificar_contacto(contactos,email)
                pulse_tecla_para_continuar()
            elif opcion == 3:
                borrar_consola()
                eliminar_contacto(contactos,email)
                pulse_tecla_para_continuar()
            elif opcion == 4:
                borrar_consola()
                vaciar_agenda(contactos)
            elif opcion == 5:
                borrar_consola()
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
    """ Realiza la diferencia simétrica entre OPCIONES_MENU y un conjunto de 8
    Returns:
        set: retorna un conjunto sin el 8
    """
    diferencia = {8} ^ OPCIONES_MENU
    return diferencia


def pulse_tecla_para_continuar():
    """ Muestra un mensaje y realiza una pausa hasta que se pulse una tecla
    """
    print("\n")
    os.system("pause")


def guardar_email(contactos: list) -> set:
    """ Crea y guarda un conjunto con todos los emails de los contactos sin repetirse
    Args:
        contactos (list): lista vacía  con todos los diccionarios con los datos de los contactos
    Returns:
        set: retorna el conjunto creado
    """
    email = set()
    for i in contactos:
        email.add(i['email'])
    return email

def preguntas(msj:str)->str:
    """ Pregunta un mensaje que se responderá con si o no
    Args:
        msj (str): recibe un mensaje que imprime en la funcion
    Returns:
        str: retorna el resultado de la pregunta (s, si, n, no)
    """
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
    agregar_contacto(contactos, email)


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