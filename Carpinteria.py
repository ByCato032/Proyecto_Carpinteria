import simpy
import numpy as np

#Variables de la carpintería
ventas = 0
ganancia = 0
compras = 0


#Porcentajes de venta para cada producto
porcentajes_ventas = {
   'mesas': np.random.uniform(0.25, 0.35),
    'sillas': np.random.uniform(0.15, 0.25),
    'roperos': np.random.uniform(0.1, 0.2),
    'cabeceras': np.random.uniform(0.07, 0.17),
    'mesa_de_noche': np.random.uniform(0.04, 0.14),
    'otros': np.random.uniform(0.15, 0.25)
}

def porcentaje_ganancia(producto):
    # Retorna el porcentaje de ganancia para un producto
    porcentajes_ganancia = {
        'mesas': 0.35,
        'sillas': 0.3,
        'roperos': 0.4,
        'cabeceras': 0.25,
        'mesa_de_noche': 0.2,
        'otros': 0.2
    }
    return porcentajes_ganancia[producto]

#Se ingresan los precios para cada producto
precios_base = {}
print("\n\033[;34m"+"--- Ingreso de precios para los productos ---"+ "\033[;37m")
for producto in porcentajes_ventas:
    while True:
        try:
            precio = float(input(f"Ingrese el precio base para {producto}: "))
            precios_base[producto] = precio
            break
        except ValueError:
            print("Debes escribir un número...")
            continue

#Cantidad de producto que se tiene en stock en base a los analisis hechos
cant_prod = {
    'mesas': 47,
    'sillas': 43,
    'roperos': 37,
    'cabeceras': 25,
    'mesa_de_noche': 19,
    'otros': 23
}

def cantidad_prod(producto):
    return cant_prod[producto]  #Retorna la cantidad que hay del producto

def producto_precio(producto):
    return precios_base[producto]  #Retorna el precio base de un producto

#Diccionarios para gurdar ventas y ganancias totales
ventas_totales = {}
ganancias_totales = {}
print("\033[;36m"+"\n---Simulacion de ventas de la carpinteria ---" + "\033[;37m")

#Funcion que realiza las ventas y ganancias
def venta(env, producto):
    global ventas, ganancia, compras
    porcentaje_venta = porcentajes_ventas[producto]

    while True:
        cantidad = np.random.randint(1, 50)

        if cantidad <= cantidad_prod(producto):
            precio_venta = producto_precio(producto) * porcentaje_venta
            ganancia_venta = precio_venta * porcentaje_ganancia(producto)

            ventas += precio_venta
            ganancia += ganancia_venta

            if producto in ventas_totales:
                ventas_totales[producto] += precio_venta
                ganancias_totales[producto] += ganancia_venta
            else:
                ventas_totales[producto] = precio_venta
                ganancias_totales[producto] = ganancia_venta

            print(f"Se vendió {cantidad} {producto} con un porcentaje de venta del %{porcentaje_venta*100:.2f}")
            print(f"Ganancia por venta de {producto}: ${ganancia_venta:.2f}")

            cant_prod[producto] -= cantidad  # Reducir la cantidad de productos disponibles
        else:
           # Realizar la venta con la cantidad de productos disponibles
            cantidad_vendida = cantidad_prod(producto)
            if cantidad_vendida > 0:
                precio_venta = producto_precio(producto) * porcentaje_venta
                ganancia_venta = precio_venta * porcentaje_ganancia(producto)

                ventas += precio_venta
                ganancia += ganancia_venta

                if producto in ventas_totales:
                    ventas_totales[producto] += precio_venta
                    ganancias_totales[producto] += ganancia_venta
                else:
                    ventas_totales[producto] = precio_venta
                    ganancias_totales[producto] = ganancia_venta

                print(f"No hay suficientes {producto} para vender {cantidad} unidades. Se vendieron {cantidad_vendida} unidades.")
                print(f"Ganancia por venta de {producto}: ${ganancia_venta:.2f}")

                cant_prod[producto] -= cantidad_vendida  # Reducir la cantidad de productos disponibles

        yield env.timeout(5)

env = simpy.Environment()

env.process(venta(env, 'mesas'))
env.process(venta(env, 'sillas'))
env.process(venta(env, 'roperos'))
env.process(venta(env, 'cabeceras'))
env.process(venta(env, 'mesa_de_noche'))
env.process(venta(env, 'otros'))

env.run(until=10)

print("\033[;32m"+"\n--- Total de cada producto ---" + "\033[;37m")
for producto in ventas_totales:
    print(f"Ventas totales de {producto}: ${ventas_totales[producto]:.2f}")
    print(f"Ganancia total de {producto}: ${ganancias_totales[producto]:.2f}")

print("\033[;32m"+"\n--- Total de ventas y ganancias ---" + "\033[;37m")
print(f"Ventas totales: ${ventas:.2f}")
print(f"Ganancia total: ${ganancia:.2f}")
