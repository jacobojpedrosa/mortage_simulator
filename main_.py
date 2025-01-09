import matplotlib.pyplot as plt
import csv

def simulacion_hipoteca(capital, interes_anual, plazo_anos, seguro_vida=0, seguro_vivienda=0, alarma=0, amortizaciones_extraordinarias=None, comision_amortizacion=0, titulo_grafica="Desglose de la cuota mensual: Amortización vs Intereses"):
    """
    Simula una hipoteca considerando capital, interés anual, plazo en años, vinculaciones adicionales,
    y amortizaciones extraordinarias con comisión.

    Args:
        capital (float): Monto total del préstamo.
        interes_anual (float): Tasa de interés anual en porcentaje (por ejemplo, 3.5 para 3.5%).
        plazo_anos (int): Plazo de la hipoteca en años.
        seguro_vida (float): Coste mensual del seguro de vida (opcional).
        seguro_vivienda (float): Coste mensual del seguro de vivienda (opcional).
        alarma (float): Coste mensual del servicio de alarma (opcional).
        amortizaciones_extraordinarias (list): Lista de diccionarios donde cada uno contiene:
            - 'mes' (int): Mes en el que se realiza la amortización extraordinaria.
            - 'monto' (float): Monto de la amortización extraordinaria.
            - 'tipo' (str): 'cuota' para reducir cuota mensual, 'plazo' para reducir plazo.
        comision_amortizacion (float): Porcentaje de comisión sobre las amortizaciones extraordinarias.
        titulo_grafica (str): Título personalizado para la gráfica.

    Returns:
        dict: Resultados de la simulación incluyendo pago mensual, total anual, y total al final del plazo.
    """
    if amortizaciones_extraordinarias is None:
        amortizaciones_extraordinarias = []

    # Convertir la tasa de interés anual a mensual
    interes_mensual = (interes_anual / 100) / 12

    # Número total de pagos
    num_pagos = plazo_anos * 12

    # Cálculo de la cuota mensual usando la fórmula de anualidades
    cuota_mensual_base = (capital * interes_mensual) / (1 - (1 + interes_mensual) ** -num_pagos)

    # Costes mensuales adicionales
    costes_adicionales = seguro_vida + seguro_vivienda + alarma

    # Cuota mensual total
    cuota_mensual_total = cuota_mensual_base + costes_adicionales

    # Generar los detalles de amortización mensual
    saldo_restante = capital
    amortizacion = []
    intereses = []
    cuota = []
    saldos = []
    vinculaciones = []
    total_pagado = 0

    for mes in range(1, num_pagos + 1):
        amort_extra_mes = next((amort for amort in amortizaciones_extraordinarias if amort['mes'] == mes), None)
        if amort_extra_mes:
            monto_extra = amort_extra_mes['monto']
            comision = monto_extra * (comision_amortizacion / 100)
            monto_total = monto_extra + comision

            if amort_extra_mes['tipo'] == 'plazo':
                saldo_restante -= monto_total
            elif amort_extra_mes['tipo'] == 'cuota':
                saldo_restante -= monto_total
                # Recalcular cuota mensual base
                num_pagos_restantes = num_pagos - mes + 1
                cuota_mensual_base = (saldo_restante * interes_mensual) / (1 - (1 + interes_mensual) ** -num_pagos_restantes)

        interes_mes = saldo_restante * interes_mensual
        amortizacion_mes = cuota_mensual_base - interes_mes

        # Evitar saldo negativo
        if saldo_restante < amortizacion_mes:
            amortizacion_mes = saldo_restante
            cuota_mensual_base = interes_mes + amortizacion_mes

        saldo_restante -= amortizacion_mes

        amortizacion.append(amortizacion_mes)
        intereses.append(interes_mes)
        cuota_actual = amortizacion_mes + interes_mes + costes_adicionales
        cuota.append(cuota_actual)
        saldos.append(saldo_restante if saldo_restante > 0 else 0)
        vinculaciones.append(costes_adicionales)

        total_pagado += cuota_actual

        if saldo_restante <= 0:
            break

    # Guardar resultados en un archivo CSV
    with open('simulacion_hipoteca.csv', 'w', newline='') as csvfile:
        fieldnames = ['Mes', 'Amortización (€)', 'Intereses (€)', 'Saldo Restante (€)', 'Costes Vinculaciones (€)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for mes in range(len(amortizacion)):
            writer.writerow({
                'Mes': mes + 1,
                'Amortización (€)': round(amortizacion[mes], 2),
                'Intereses (€)': round(intereses[mes], 2),
                'Saldo Restante (€)': round(saldos[mes], 2),
                'Costes Vinculaciones (€)': round(vinculaciones[mes], 2)
            })

    # Resultados anuales y totales
    total_anual = sum(cuota[:12]) if len(cuota) >= 12 else sum(cuota)

    # # Graficar la amortización mensual
    # plt.figure(figsize=(10, 6))
    # plt.plot(range(1, len(amortizacion) + 1), amortizacion, label="Amortización", color="blue")
    # plt.plot(range(1, len(intereses) + 1), intereses, label="Intereses", color="orange")
    # plt.plot(range(1, len(cuota) + 1), cuota, label="Cuota", color="red")
    # plt.xlabel("Mes")
    # plt.ylabel("Cantidad (€)")
    # plt.title(titulo_grafica)
    # plt.legend()
    # plt.grid(True)

    # Agregar resumen de resultados a la gráfica
    resumen = (
        f"Cuota Mensual Base: {round(cuota_mensual_base, 2)} €\n"
        f"Cuota Mensual Total: {round(cuota_mensual_total, 2)} €\n"
        f"Total Anual: {round(total_anual, 2)} €\n"
        f"Total Pagado: {round(total_pagado, 2)} €"
    )
    # plt.gcf().text(0.15, 0.75, resumen, fontsize=10, bbox=dict(facecolor='white', alpha=0.7))

    # plt.show()

    return {
        "Cuota Mensual Base": round(cuota_mensual_base, 2),
        "Cuota Mensual Total": round(cuota_mensual_total, 2),
        "Total Anual": round(total_anual, 2),
        "Total Pagado": round(total_pagado, 2)
    }



# Ejemplo de uso
# amortizaciones = [
#     {'mes': 24, 'monto': 10000, 'tipo': 'cuota'},  # Amortización extraordinaria en el mes 24 con reducción de cuota
#     {'mes': 36, 'monto': 15000, 'tipo': 'cuota'},   # Amortización extraordinaria en el mes 36 con reducción de cuota
#     {'mes': 48, 'monto': 15000, 'tipo': 'cuota'},   # Amortización extraordinaria en el mes 48 con reducción de cuota
#     {'mes': 60, 'monto': 15000, 'tipo': 'cuota'},   # Amortización extraordinaria en el mes 48 con reducción de cuota
# ]

amortizaciones = []

# data = simulacion_hipoteca(
#     capital=378000,
#     interes_anual=2.1,
#     plazo_anos=30,
#     seguro_vida=266/3,
#     seguro_vivienda=641/12,
#     alarma=55,
#     amortizaciones_extraordinarias=amortizaciones,
#     comision_amortizacion=0.5,
#     titulo_grafica="Simulación de Hipoteca Sabadell con Ajustes"
# )

# print("Resultados de la simulación de hipoteca:")
# for key, value in data.items():
#     print(f"{key}: {value} €")

resultados = []
for i in range(0,30):
    for j in range(0,30):
        y = j+1
        #'Yes' if fruit == 'Apple' else 'No'

        tipo = 'cuota' if y < i else 'plazo'

        amortizaciones.append({'mes': 12 * y, 'monto': 10000, 'tipo': tipo})


    # print(f"{amortizaciones}\n\n\n")

    data = simulacion_hipoteca(
        capital=378000,
        interes_anual=2.1,
        plazo_anos=30,
        seguro_vida=266/3,
        seguro_vivienda=641/12,
        alarma=55,
        amortizaciones_extraordinarias=amortizaciones,
        comision_amortizacion=0.5,
        titulo_grafica="Simulación de Hipoteca Sabadell con Ajustes"
    )

    
    print(f"Variante: {i}")
    print("Resultados de la simulación de hipoteca:")
    for key, value in data.items():
        print(f"{key}: {value} €")
    print("#############################################")