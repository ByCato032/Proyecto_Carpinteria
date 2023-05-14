import simpy
import random

#Variables de la carpintería
ventas = 0
ganancia = 0
compras = 0

#Porcentajes de venta para cada producto
porcentajes_ventas = {
    'mesas': random.uniform(0.25,0.35),
    'sillas': random.uniform(0.15, 0.25),
    'roperos': random.uniform(0.1, 0.2),
    'cabeceras': random.uniform(0.07, 0.17),
    'mesa_de_noche': random.uniform(0.04, 0.14),
    'otros': random.uniform(0.15,0.25)
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

def producto_precio(producto):
    precios_base = {
        'mesas': 1000,
        'sillas': 500,
        'roperos': 2000,
        'cabeceras': 800,
        'mesa_de_noche': 600,
        'otros': 400
    }
    return precios_base[producto] #Retorna el precio base de un producto

#Diccionarios para gurdar ventas y ganancias totales
ventas_totales = {}
ganancias_totales = {}
print("\033[;36m"+"\n---Simulacion de ventas de la carpinteria ---" + "\033[;37m")
#Funcion que realiza las ventas y ganancias
def venta(env,producto):
    global ventas, ganancia, compras
    porcentaje_venta = porcentajes_ventas[producto]
    
    while True:
        cantidad = random.randint(1, 50)
        precio_venta = producto_precio(producto) * porcentaje_venta
        ganancia_venta = precio_venta * porcentaje_ganancia(producto)
        
        ventas += precio_venta
        ganancia += ganancia_venta

        #Se actualiza las ventas y ganancias totales para cada producto
        if producto in ventas_totales:
            ventas_totales[producto] += precio_venta
            ganancias_totales[producto] += ganancia_venta
        else:
            ventas_totales[producto] = precio_venta
            ganancias_totales[producto] = ganancia_venta
        
        print(f"Se vendió {cantidad} {producto} con un porcentaje de venta del ${porcentaje_venta*100:.2f}")
        print(f"Ganancia por venta de {producto}: ${ganancia_venta:.2f}")
        #print(f"Ventas totales: ${ventas:.2f}")
        #print(f"Ganancia total: ${ganancia:.2f}")
        yield env.timeout(5)  # Simular tiempo de venta

#Se crea el objeto env para realizar el ambiente de simulacion
env = simpy.Environment()

#Se crean los procesos de simulacion de venta
env.process(venta(env,'mesas'))
env.process(venta(env,'sillas'))
env.process(venta(env,'roperos'))
env.process(venta(env,'cabeceras'))
env.process(venta(env,'mesa_de_noche'))
env.process(venta(env,'otros'))

env.run(until=10)  #Simular durante el tiempo especificado

#Se imprimen las ventas y ganacias totales de la carpinteria
print("\033[;32m"+"\n--- Total de cada producto ---" + "\033[;37m")
for producto in ventas_totales:
    print(f"Ventas totales de {producto}: ${ventas_totales[producto]:.2f}")
    print(f"Ganancia total de {producto}: ${ganancias_totales[producto]:.2f}")

print("\033[;32m"+"\n--- Total de ventas y ganancias ---" + "\033[;37m")
print(f"Ventas totales: ${ventas:.2f}")
print(f"Ganancia total: ${ganancia:.2f}")