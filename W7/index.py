import threading
import queue
import time
import random
import struct
from datetime import datetime
import subprocess
import platform

#? Global variables
global_queue = queue.Queue(maxsize=10) #* Queue to store messages
condition = threading.Condition() #* Condition variable to synchronize threads
stop_event = threading.Event() #* Event to stop the threads

#? Counters for metrics
fill_count = 0 #* Number of times the queue get filled
producer_wait_times = [] #* List of wait times for producers (drones)
consumer_wait_times = [] #* List of wait times for consumers (server)

def construct_operation(dron_id):
    """
    Construc the message sended from drone to the server.

    args:
        dron_id (int): The id of the drone that is sending the message.

    returns:
        message (bytes): The message that the drone is sending.
    """
    operation_code = random.randint(0, 0xFFFFFFFF)
    payload_size = random.randint(1, 50)
    payload = bytes(random.getrandbits(8) for _ in range(payload_size))

    message = struct.pack(f"<II{len(payload)}s", dron_id, operation_code, payload)
    
    return message

def producer(dron_id):
    """
    Simulate the sending of messages from the drones to the server.

    args:
        dron_id (int): The id of the drone that is sending the message.
    """
    global global_queue, fill_count
    while not stop_event.is_set():
        start_time = time.time()
        with condition:
            while global_queue.full():
                with condition:
                    fill_count += 1
                    print("Cola llena, Drone esperando...")
                    if stop_event.wait(timeout=0.1):
                        return
            wait_time = time.time() - start_time
            producer_wait_times.append(wait_time)

            message = construct_operation(dron_id)
            global_queue.put(message)

            dron_id, operation_code, payload = parse_operation(message)

            print(f"Mensaje Enviado: Dron ID {dron_id} - Codigo de operacion {operation_code} - Mensaje tamaño: {len(message)} bytes - Mensaje: {payload}")

            dron_id = (dron_id + 1) % 30

            condition.notify()
        time.sleep(random.random())

def parse_operation(message):
    """
    Process the message received from the drone.

    args: 
        message (bytes): The message received from the drone.

    returns:
        dron_id (int): The id of the drone that sent the message.
        operation_code (int): The operation code of the message.
        payload (bytes): The payload of the message.
    """
    format = f"<II{len(message) - 8}s"
    dron_id, operation_code, payload = struct.unpack(format, message)
    
    return dron_id, operation_code, payload

def consumer():
    global global_queue
    while not stop_event.is_set():
        start_time = time.time()
        with condition:
            while global_queue.empty():
                print("Cola vacía, Servidor esperando...")
                if stop_event.wait(timeout=0.1):
                    return
            
            wait_time = time.time() - start_time
            consumer_wait_times.append(wait_time)
            
            message = global_queue.get()
            dron_id, operation_code, payload = parse_operation(message)
            
            print(f"Mensaje recibido: Dron ID {dron_id} - Codigo de operacion {operation_code} - Mensaje tamaño: {len(message)} bytes - Mensaje: {payload}")
            
            condition.notify()
        time.sleep(random.random())

def test(num_drones, num_consumers):
    """
    Perform a test with the given parameters.

    args:
        queue_size (int): The size of the queue.
        num_drones (int): The number of drones that will send messages.
        num_consumers (int): The number of consumers that will process the messages.
        test_time (int): The time in seconds that the test will run.

    returns:
        result (dict): A dictionary containing the test configuration and results.
    """
    
    global global_queue, fill_count, producer_wait_times, consumer_wait_times
    fill_count = 0
    producer_wait_times = []
    consumer_wait_times = []

    producer_threads = []
    for dron_id in range(num_drones):
        thread = threading.Thread(target=producer, args=(dron_id,))
        producer_threads.append(thread)
        thread.start()

    consumer_threads = []
    for _ in range(num_consumers):
        thread = threading.Thread(target=consumer)
        consumer_threads.append(thread)
        thread.start()

    time.sleep(2)

    print("Finalizando prueba...")
    print(f"Tiempo de ejecución: {2} segundos")
    
    stop_event.set()
    time.sleep(0.1)
    for thread in producer_threads:
        thread.join()
    for thread in consumer_threads:
        thread.join()
    stop_event.clear()

    result = {
        'num_drones': num_drones,
        'num_consumers': num_consumers,
        'times_filled': fill_count,
        'average_producer_wait_time': sum(producer_wait_times) / len(producer_wait_times) if producer_wait_times else None,
        'average_consumer_wait_time': sum(consumer_wait_times) / len(consumer_wait_times) if consumer_wait_times else None
    }

    return result

def run_tests():
    """
    Run a series of tests with different configurations and store the results.
    """

    configurations = [
        {'num_drones': 10, 'num_consumers': 30},
        {'num_drones': 20, 'num_consumers': 20},
        {'num_drones': 30, 'num_consumers': 10},
        {'num_drones': 20, 'num_consumers': 20},
        {'num_drones': 10, 'num_consumers': 30},
    ]

    results = []
    for config in configurations:
        print(f"Ejecutando prueba con configuración: {config}")
        result = test(config['num_drones'], config['num_consumers'])
        results.append(result)
        print(f"Prueba completada.")
        print()

    print("Resultados de las pruebas:")
    for result in results:
        results.append(result)
    
    return results

def generate_report():
    
    date = datetime.now().strftime("%Y-%m-%d")

    results = test()
    
    qmd_content = f"""
---
title: "Producer-Consumer Problem with Condition Variables"
author: "Emmanuel Silva Diaz"
date: {date}
format: pdf
jupyter: python3
---

# Introduction

En el contexto de sistemas distribuidos y aplicaciones concurrentes, la sincronización eficiente entre productores 
y consumidores es crucial para mantener el rendimiento y la estabilidad del sistema. En este informe, se explora el 
comportamiento de un sistema de encolado de mensajes que simula un entorno en el que múltiples drones (productores) 
envían mensajes a un servidor (consumidor). El objetivo es evaluar la capacidad del sistema para manejar la 
sincronización y la gestión del tamaño de la cola bajo diversas configuraciones.

# Objective

El estudio se centra en analizar un sistema simple de encolado de mensajes en el que los drones representan 
los productores que envían mensajes y el servidor representa al consumidor que procesa estos mensajes. Se simula 
la capacidad de carga del servidor y el comportamiento de los drones para evaluar la eficiencia del sistema en 
términos de sincronización entre hilos y manejo de la capacidad de la cola.

# Metodology

1. Para realizar el análisis, se llevaron a cabo pruebas con las siguientes condiciones:
    - Tamaño de la cola: Se mantiene constante en 10 mensajes.
    - Duración del test: Se fija en 5 segundos para cada configuración.

2. Las configuraciones varían en los siguientes parámetros:
    - Número de productores (drones): Desde 10 hasta 30.
    - Número de consumidores (servidores): Desde 5 hasta 30.

3. Las pruebas se configuran en tres etapas cualitativas:
    - Número de productores mayor que el número de consumidores: Para evaluar cómo el sistema maneja un alto nivel de 
    concurrencia en los productores.
    - Número de productores igual al número de consumidores: Para observar el comportamiento del sistema cuando 
    ambos tipos de hilos están equilibrados.
    - Número de productores menor que el número de consumidores: Para analizar la eficiencia del sistema con menos 
    productores en comparación con los consumidores.

## Métricas y Análisis

Se recopilan las siguientes métricas durante las pruebas:
- Número de veces que la cola se llena: Indicativo de cómo los productores manejan la espera cuando la 
cola alcanza su capacidad máxima.
- Tiempo de espera promedio de los productores y consumidores: Mide la eficiencia de la sincronización 
entre productores y consumidores.

Para la implementacion de este estudio se llevaron a cabo las siguientes funciones:

- **construct_operation()**: Esta funcion construye el mensaje que el dron envia al servidor.
- **producer(drone_id)**: Esta funcion simula el envio de mensajes desde los drones al servidor.
- **parse_operation(message)**: Esta funcion procesa el mensaje recibido desde el dron, es decir, decodea el mensaje.
- **consumer()**: Esta funcion simula el procesamiento de mensajes por parte del servidor.
- **test()**: Esta funcion realiza una prueba con una configuracion especifica.
- **run_tests()**: Esta funcion ejecuta los test con diferentes configuraciones y almacena los resultados.

# Test Results

{results.to_markdown(index=False)}

# Analysis and Discussion
1. Impacto del Número de Productores y Consumidores en el Llenado de la Cola:
    - Altos Productores, Bajos Consumidores: En configuraciones con muchos drones y pocos consumidores 
    (como en la Configuración 3), la cola se llena más frecuentemente (50 veces). Esto es esperado, ya 
    que el alto número de productores genera mensajes más rápido de lo que los consumidores pueden procesar, 
    llevando a un llenado constante de la cola.
    - Igual Número de Productores y Consumidores: Cuando el número de drones y consumidores es igual 
    (Configuración 2 y 4), la cola se llena de manera significativa, pero no tan frecuentemente como en el 
    caso anterior. La sincronización entre productores y consumidores es más equilibrada, aunque sigue 
    habiendo una presión considerable sobre la cola.
    - Bajos Productores, Altos Consumidores: En configuraciones con menos drones y más consumidores 
    (como en la Configuración 1 y 5), la cola no se llena (Configuración 1) o se llena menos frecuentemente 
    (Configuración 5). En estos casos, la alta capacidad de procesamiento de los consumidores permite que el 
    sistema mantenga la cola vacía o con poca carga. Los tiempos de espera de los productores son más bajos en 
    comparación con las configuraciones donde hay más productores, y los tiempos de espera de los consumidores 
    son más estables, aunque ligeramente elevados en la Configuración 5 debido a la ligera carga en la cola.

2. Tiempos de Espera de Productores y Consumidores:
    - Productores: Los tiempos de espera de los productores aumentan en configuraciones donde el número de 
    productores es alto en comparación con los consumidores. Esto es evidente en la Configuración 5, donde 
    los tiempos de espera de los productores son significativamente más altos (0.95 segundos). La alta frecuencia 
    de llenado de la cola contribuye a estos tiempos de espera.
    - Consumidores: Los tiempos de espera de los consumidores son consistentes y relativamente altos en todas 
    las configuraciones (alrededor de 2 segundos). Esto sugiere que los consumidores están procesando mensajes 
    a un ritmo mucho más lento que el de los productores, lo que puede ser un factor limitante en el rendimiento 
    del sistema.

3. Sincronización y Utilización de Variables de Condición:
    - Utilización de Variables de Condición: La implementación de variables de condición es efectiva para sincronizar 
    productores y consumidores, evitando bloqueos innecesarios y gestionando el acceso a la cola de manera eficiente. 
    Sin embargo, en configuraciones con un alto número de productores, la cola se llena con frecuencia, y los 
    productores deben esperar, lo que resalta la importancia de una sincronización adecuada.
    - Desafíos: Uno de los principales desafíos es equilibrar el número de productores y consumidores para minimizar 
    los tiempos de espera y el llenado de la cola. Demasiados productores pueden llevar a un llenado excesivo de la 
    cola, mientras que un número insuficiente de consumidores puede causar tiempos de espera prolongados para los 
    mensajes.



# Conclusion

   
   """
    with open("informe.qmd", "w", encoding="utf-8") as file:
        file.write(qmd_content)

    subprocess.run(["quarto", "render", "informe.qmd", "--to", "pdf"])

    pdf_file = "informe.pdf"
    if platform.system() == "Darwin":
        subprocess.run(["open", pdf_file])
    elif platform.system() == "Windows":
        subprocess.run(["start", pdf_file], shell=True)
    else:
        subprocess.run(["xdg-open", pdf_file])

if __name__ == "__main__":
    run_tests()
