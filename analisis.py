import csv
from collections import defaultdict
import matplotlib.pyplot as plt

# Leer archivo CSV
with open('ventas_tienda.csv', newline='', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    datos = [fila for fila in lector]

# Convertir los valores numéricos
for fila in datos:
    fila["cantidad"] = int(fila["cantidad"])
    fila["precio_unitario"] = float(fila["precio_unitario"])
    fila["ingreso"] = fila["cantidad"] * fila["precio_unitario"]

# a) Total de productos vendidos por tipo
ventas_totales = defaultdict(int)
for fila in datos:
    ventas_totales[fila["producto"]] += fila["cantidad"]

print("Total de productos vendidos por tipo:")
for producto, total in ventas_totales.items():
    print(f"{producto}: {total} unidades")

# b) Mes con más ventas en unidades
ventas_por_mes = defaultdict(int)
for fila in datos:
    ventas_por_mes[fila["mes"]] += fila["cantidad"]

mes_mayor = max(ventas_por_mes, key=ventas_por_mes.get)
print(f"\nMes con más ventas: {mes_mayor} ({ventas_por_mes[mes_mayor]} unidades)")

# c) Producto con más ingresos
ingresos_por_producto = defaultdict(float)
for fila in datos:
    ingresos_por_producto[fila["producto"]] += fila["ingreso"]

producto_mayor_ingreso = max(ingresos_por_producto, key=ingresos_por_producto.get)
print(f"\nProducto con más ingresos: {producto_mayor_ingreso} (${ingresos_por_producto[producto_mayor_ingreso]:,.2f})")

# d) Tendencia de ventas (gráfica de barras por mes y producto)
productos = set(fila["producto"] for fila in datos)
meses = sorted(set(fila["mes"] for fila in datos))

# Inicializar estructura de datos
ventas_mensuales = {producto: [0]*len(meses) for producto in productos}

# Llenar estructura
mes_indices = {mes: i for i, mes in enumerate(meses)}
for fila in datos:
    i = mes_indices[fila["mes"]]
    ventas_mensuales[fila["producto"]][i] += fila["cantidad"]

# Graficar
plt.figure(figsize=(10,6))
for producto, valores in ventas_mensuales.items():
    plt.plot(meses, valores, label=producto, marker='o')

plt.title("Tendencia de ventas por mes y producto")
plt.xlabel("Mes")
plt.ylabel("Cantidad Vendida")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# e) Promedio de ventas por producto
print("\nPromedio mensual por producto:")
for producto in productos:
    total = ventas_totales[producto]
    promedio = total / 6  # 6 meses
    print(f"{producto}: {promedio:.2f} unidades/mes")

# Gráfica de ingresos por producto
plt.figure(figsize=(8,5))
productos_ordenados = list(ingresos_por_producto.keys())
ingresos = [ingresos_por_producto[p] for p in productos_ordenados]

plt.bar(productos_ordenados, ingresos, color="skyblue")
plt.title("Ingresos Totales por Producto")
plt.ylabel("Ingresos ($)")
plt.tight_layout()
plt.show()
