import json
import os

FILE_NAME = "registros.json"


""" Función encargada de cargar registros existentes """


def cargar_registros():

    """ Carga los registros almacenados en formato JSONL. """

    # Si el archivo no existe se devuelve una lista vacía
    if not os.path.exists(FILE_NAME):
        return []

    # Inicializamos lista de registros vacia
    registros = []

    # Abrimos el archivo "FILE_NAME" en modo lectura
    # en un contexto seguro "with"
    with open(FILE_NAME, "r", encoding="utf-8") as file:

        # Iteramos el archivo JSONL linea por linea
        for linea in file:

            # Limpiamos espacios en blanco
            linea = linea.strip()

            # Si alguna linea contiene una lista vacia la descartamos
            if not linea or linea == "[]":
                continue

            # Agregamos nuevo registro y gestionamos posible error
            try:
                # Agregamos nueva linea de texto JSONL
                registros.append(json.loads(linea))
            # Manejamos error con una excepción
            except json.JSONDecodeError:
                print(f"Advertencia: Linea inválida ignorada -> {linea}")

    # Devolvemos lista de registros
    return registros


""" Función encargada de guarda un nuevo registro """


def guardar_registro(nuevo_registro):

    """Agrega un nuevo registro sin sobrescribir todo el archivo."""
    # Verificamos con os que el archivo exista
    if os.path.exists(FILE_NAME):

        # Abrimos el archivo en un entorno seguro "with"
        with open(FILE_NAME, encoding="utf-8") as file:
            contenido = file.read().strip()

        # Si el archivo contiene una lista vacia la borramos
        if contenido == "[]":
            # Abrimos en modo escritura para poder hacer modificaciones
            with open(FILE_NAME, "w", encoding="utf-8") as file:
                # Borramos
                file.write("")

    # Abrimos archivo en modo append en un entorno seguro "with"
    with open(FILE_NAME, "a", encoding="utf-8") as file:
        # Agregamos nuevo registro en formato JSONL
        json.dump(nuevo_registro, file)
        # Salto de linea para mantener un registro en cada linea
        file.write("\n")


""" Función encargada de listar todos los registos """


def listar_registros():

    """Muestra todos los registros almacenados."""
    # Cargamos los registros existentes
    registros = cargar_registros()
    # Si no tenemos registros imprimimos mensaje y detenemos la funcion
    if not registros:
        print("No hay registros aún.\n")
        return

    # En caso contrario iteramos por la lista de registros
    for i, registro in enumerate(registros, start=1):
        # Imprimimos cada diccionario que corresponde a un registro
        print(
            f"{i}. Nombre: {registro['nombre']}",
            "Edad: {registro['edad']}, Email: {registro['email']}")


""" Función encargada de buscar un registro por nombre """


def buscar_registro():

    """Busca un registro por nombre."""
    # Pedimos al usuario que ingrese el nombre
    nombre = input("Ingrese el nombre a buscar: ")
    # Cargamos registros existentes
    registros = cargar_registros()

    # Filtramos registros por el nombre proporcionado
    encontrados = [r for r in registros
                   if r["nombre"].lower() == nombre.lower()]

    # Si encontramos algun registro lo Imprimimos
    if encontrados:
        # Iteramos por los registros encontrados
        for registro in encontrados:
            # Imprimimos registro
            print(
                f"Nombre: {registro['nombre']}",
                "Edad: {registro['edad']}, Email: {registro['email']}")
    # Si no encontramos imprimimos mensaje
    else:
        print("Registro no encontrado.\n")


""" Función encargada de borrar un registros del archivo """


def eliminar_registro():

    """Elimina un registro por nombre."""
    # Pedimos al usuario que ingrese el nombre
    nombre = input("Ingrese el nombre a eliminar: ")
    # Cargamos registros existentes
    registros = cargar_registros()
    # Filtramos registros por nombre
    registros_filtrados = [r for r in registros
                           if r["nombre"].lower() != nombre.lower()]

    # Si no encontramos registro imprimimos mensaje
    if len(registros) == len(registros_filtrados):
        print("No se encontró el registro.\n")
    # Si encontramos
    else:
        # Abrimos archivo en modo escritura
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            # Sobreescribimos los registros sin el registro a eliminar
            for reg in registros_filtrados:
                json.dump(reg, file)
                file.write("\n")
        print("Registro eliminado con éxito!\n")


""" Función encargada de modificar datos de un registro """


def modificar_registro():

    """Modifica un registro existente en el archivo JSONL."""
    # Cargamos registros existentes
    registros = cargar_registros()
    # Pedimos al usuario que ingrese nombre de registro
    nombre_buscar = input("Ingrese el nombre del registro"
                          "que desea modificar: ")

    # Iteramos por los registros
    for registro in registros:
        # Si el registro actual contiene el nombre a buscar
        if registro["nombre"].lower() == nombre_buscar.lower():
            # Hemos encontrado el registro
            print(f"Registro encontrado: {registro}")

            # Pedimos al usuario que ingrese los nuevos datos
            nuevo_nombre = input(
                f"Nuevo nombre ({registro['nombre']}): "
                ) or registro["nombre"]
            nueva_edad = input(
                f"Nueva edad ({registro['edad']}): "
                ) or registro["edad"]
            nuevo_email = input(
                f"Nuevo email ({registro['email']}): "
                ) or registro["email"]

            # Asignamos nuevos valores
            registro["nombre"] = nuevo_nombre
            registro["edad"] = nueva_edad
            registro["email"] = nuevo_email

            # Abrimos archivo en modo escritura
            with open(FILE_NAME, "w", encoding="utf-8") as file:
                # Reescribimos registros
                for reg in registros:
                    json.dump(reg, file)
                    file.write("\n")

            print("Registro modificado con éxito!\n")
            return

    print("Registro no encontrado.\n")


""" Función encargada de gestionar menú principal """


def menu():

    """Muestra el menú de opciones."""
    while True:
        print("\n--- SISTEMA DE REGISTROS ---")
        print("1. Agregar registro")
        print("2. Listar registros")
        print("3. Buscar registro")
        print("4. Eliminar registro")
        print("5. Modificar registro")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        # Gestionamos opcion introducida
        if opcion == "1":
            guardar_registro(
                    {"nombre": input("Nombre: "),
                     "edad": input("Edad: "), "email": input("Email: ")})
        elif opcion == "2":
            listar_registros()
        elif opcion == "3":
            buscar_registro()
        elif opcion == "4":
            eliminar_registro()
        elif opcion == "5":
            modificar_registro()
        elif opcion == "6":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida, intente de nuevo.\n")


menu()
