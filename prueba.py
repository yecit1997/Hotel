'''
Monotoreo del estado de la CPU y bateria
'''

import time
import psutil


def convertir_tiempo(segundos):
    minutos, segundos = divmod(segundos, 60)
    horas, minutos = divmod(minutos, 60)
    
    return "%d: %02d: %02d" % (horas, minutos, segundos)

while True:
    bateria = psutil.sensors_battery()
    print(psutil.virtual_memory())
    # print('Bateria: ',bateria)
    
    uso_cpu = psutil.cpu_percent(interval=1)
    print(f'Uso de CPU: {uso_cpu}')
    
    time.sleep(1)
    
    if bateria is not None:
        print('Porcentaje de bateria: ', bateria.percent)
        print('conectado a la corriente: ', bateria.power_plugged)
        print('Tiempo restante de bateria: ', convertir_tiempo(bateria.secsleft))
        


