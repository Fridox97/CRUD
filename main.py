from tkinter import *
from tkinter import ttk

import pymysql
import pandas as pd


config_db = {
    'user': 'root',
    'password': '21password',
    'host': 'localhost',
    'database': 'new_db',
    'port': 3307
}

root = Tk()
root.title('Agregar')

frame_introducir = ttk.Frame(root, padding=20)
frame_introducir.grid()
INSERT = 'INSERT'
UPDATE = 'UPDATE'
producto_seleccionado = []
columnas = ['ID', 'Nombre', 'Modelo', 'Marca', 'UPC/EAN', 'Precio', 'Cantidad']

label_presentacion = Label(frame_introducir, text='Introduzca la información de su producto', font=10)
label_presentacion.grid(row=0, column=0, columnspan=2)

# Declarando todas las variables para los labels, entry fields y su posicion en el grid

nombre = Entry(frame_introducir, width=50, borderwidth=5)
nombre.grid(row=2, column=0)
modelo = Entry(frame_introducir, width=50, borderwidth=5)
modelo.grid(row=3, column=0)
marca = Entry(frame_introducir, width=50, borderwidth=5)
marca.grid(row=4, column=0)
upc = Entry(frame_introducir, width=50, borderwidth=5)
upc.grid(row=5, column=0)
precio = Entry(frame_introducir, width=50, borderwidth=5)
precio.grid(row=6, column=0)
cantidad = Entry(frame_introducir, width=50, borderwidth=5)
cantidad.grid(row=7, column=0)

label_nombre = Label(frame_introducir, text='Nombre')
label_nombre.grid(row=2, column=1)
label_modelo = Label(frame_introducir, text='Modelo')
label_modelo.grid(row=3, column=1)
label_marca = Label(frame_introducir, text='Marca')
label_marca.grid(row=4, column=1)
label_upc = Label(frame_introducir, text='UPC')
label_upc.grid(row=5, column=1)
label_precio = Label(frame_introducir, text='Precio')
label_precio.grid(row=6, column=1)
label_cantidad = Label(frame_introducir, text='Cantidad')
label_cantidad.grid(row=7, column=1)


def agregar_producto():

    # Confiramamos que los valores introducidos sean numericos
    if upc.get().isnumeric() and precio.get().isnumeric() and cantidad.get().isnumeric():
        # Revisamos si el upc introducido ya existe en la lista, en caso de existir, no agregamos el producto
        if verificar_upc(INSERT, upc_a_confirmar=upc.get()):
            print('UPC ya existente')
            return

        if 12 <= len(upc.get()) <= 13 and int(precio.get()) > 0 and int(cantidad.get()) > 0:
            sql = "INSERT INTO `table_products` (`nombre`, `modelo`, `marca`, `upc`, `precio`, `cantidad`) " \
                  "VALUES (" + "'" + nombre.get() + "', '" + modelo.get() + "', '" + \
                  marca.get() + "', '" + upc.get() + "', '" + precio.get() + "', '" + cantidad.get() + "')"

            insert_data(sql)
            # Luego de agregar el producto, eliminamos la informacion de todos los entry fields, para poder agregar
            # informacion nueva
            nombre.delete(0, len(nombre.get()))
            modelo.delete(0, len(modelo.get()))
            marca.delete(0, len(marca.get()))
            upc.delete(0, len(upc.get()))
            precio.delete(0, len(precio.get()))
            cantidad.delete(0, len(cantidad.get()))

        else:
            print('Valores invalidos')

    else:
        print('ERROR')


def insert_data(query):
    conn = pymysql.connect(**config_db)

    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query)

        conn.commit()


def obtener_data():

    conn = pymysql.connect(**config_db)

    with conn:
        with conn.cursor() as cursor:

            sql = "SELECT * FROM `table_products`"
            cursor.execute(sql)
            result = cursor.fetchall()
            tabla = pd.DataFrame(result, columns=['ID', 'Nombre', 'Modelo', 'Marca', 'UPC/EAN', 'Precio', 'Cantidad'])
            tabla_de_productos = tabla.to_numpy().tolist()

    return tabla_de_productos


def verificar_upc(accion, upc_a_confirmar='', id_update=''):
    conn = pymysql.connect(**config_db)

    with conn:
        with conn.cursor() as cursor:
            query = "SELECT `upc`, `id` FROM `table_products` WHERE `upc` = " + upc_a_confirmar
            cursor.execute(query)
            result = cursor.fetchall()

    if accion == 'INSERT' and result == ():
        return False

    elif accion == 'INSERT' and result != ():
        return True

    elif accion == 'UPDATE' and result[0][1] != id_update:
        return True

    else:
        return False


def ventana_tabla():
    root.lower()
    root_tabla = Tk()
    root_tabla.title('Datos')

    frame_tabla = ttk.Frame(root_tabla, padding=10)
    frame_tabla.grid()

    generar_tabla(frame_tabla, root_tabla)
    root_tabla.mainloop()


def drop_producto(id_eliminar):
    conn = pymysql.connect(**config_db)

    with conn:
        with conn.cursor() as cursor:
            query = "DELETE FROM `table_products` WHERE `id` = " + str(id_eliminar)
            cursor.execute(query)
            print('Producto eliminado')

        conn.commit()


def actualizar_db(id_producto, nombre, modelo, marca, upc, precio, cantidad):
    conn = pymysql.connect(**config_db)

    if upc.isnumeric() and precio.isnumeric() and cantidad.isnumeric():

        if 12 <= len(upc) <= 13 and int(precio) > 0 and int(cantidad) > 0:

            if verificar_upc(UPDATE, upc_a_confirmar=upc, id_update=id_producto):
                print('UPC ya existente')
                return

            query = "UPDATE `table_products` SET nombre = '" + nombre + "' , modelo = '" + modelo + "' , marca = '" + marca + "' , upc = '" + upc \
                    + "' , precio = '" + precio + "' , cantidad = '" + cantidad + "' WHERE `id` = " + str(id_producto)

            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)

                conn.commit()
        else:
            print('El UPC: ' + upc + ' no es valido\nO el precio o cantidad son inferiores a 0')


def ventana_actualizar(producto):

    root.lower()
    root_actualizar = Tk()
    root_actualizar.title('Actualizar')
    frame_actualizar = ttk.Frame(root_actualizar, padding=20)
    frame_actualizar.grid()
    label_id_a_actualizar = Label(frame_actualizar, text='Haga los cambios pertinentes a el producto')
    label_id_a_actualizar.grid(row=0, column=0, columnspan=2)
    data = []

    Button(frame_actualizar, text='Actualizar', command=lambda: actualizar_db(producto[0], data[0].get(), data[1].get(), data[2].get(),
                                                                              data[3].get(), data[4].get(), data[5].get()),
           padx=154, borderwidth=5).grid(row=11, column=0, columnspan=2)

    Button(frame_actualizar, text='Regresar', command=root_actualizar.destroy, padx=157, borderwidth=5).grid(row=13, column=0, columnspan=2)

    for i in range(len(producto) - 1):
        celda = Entry(frame_actualizar, width=50, borderwidth=5)
        celda.grid(row=i + 1, column=0)
        celda.insert(0, producto[i+1])
        data.append(celda)

    Label(frame_actualizar, text='Nombre').grid(row=1, column=1)
    Label(frame_actualizar, text='Modelo').grid(row=2, column=1)
    Label(frame_actualizar, text='Marca').grid(row=3, column=1)
    Label(frame_actualizar, text='UPC').grid(row=4, column=1)
    Label(frame_actualizar, text='Precio').grid(row=5, column=1)
    Label(frame_actualizar, text='Cantidad').grid(row=6, column=1)

    root_actualizar.mainloop()


def generar_tabla(frame, root):
    tabla_arreglada = obtener_data()
    print('Felix')
    for x in range(len(tabla_arreglada)):
        if x < len(columnas):
            Label(frame, text=columnas[x], font=('Arial', 12, 'bold')).grid(row=0, column=x)

        eliminar = Button(frame, text='Eliminar', command=lambda posicion=x: drop_producto(tabla_arreglada[posicion][0]), bg='RED')
        eliminar.grid(row=x + 1, column=len(tabla_arreglada[0]), padx=1, pady=1)

        actualizar = Button(frame, text='Actualizar', command=lambda posicion=x: ventana_actualizar(tabla_arreglada[posicion]), bg='CYAN')
        actualizar.grid(row=x + 1, column=len(tabla_arreglada[0]) + 1, padx=1, pady=1)

        regrear = Button(frame, text='Regresar', command=root.destroy, width=15)
        regrear.grid(row=0, column=7, columnspan=2, pady=5)

        for y in range(len(tabla_arreglada[0])):
            celdita = Entry(frame, width=15, justify='center')
            celdita.grid(row=x + 1, column=y)
            celdita.insert(0, tabla_arreglada[x][y])


def main():
    Button(frame_introducir, text='Registrar', command=agregar_producto, padx=153,
           borderwidth=5).grid(row=8, column=0, columnspan=2)
    Button(frame_introducir, text='Tabla de productos', command=ventana_tabla, padx=125,
           borderwidth=5).grid(row=9, column=0, columnspan=2)

    root.mainloop()


if __name__ == '__main__':
    main()
