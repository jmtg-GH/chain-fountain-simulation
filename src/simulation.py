# src/simulation.py

"""
Módulo que contiene la lógica principal de la simulación, incluyendo la
inicialización del sistema y el bucle de integración temporal.
"""

import numpy as np
from . import constants as const
from . import physics

def inicializar_sistema():
    """
    Crea y devuelve los arrays iniciales para las posiciones y velocidades.
    Esta versión incluye una configuración realista para el experimento de la fuente
    y mantiene la lógica de depuración del péndulo para pruebas.
    """
    # Creamos los arrays vacíos con el tamaño correcto
    posiciones = np.zeros((const.NUM_ESLABONES, 2), dtype=float)
    velocidades = np.zeros((const.NUM_ESLABONES, 2), dtype=float)

    # --- Mantenemos la lógica de depuración del péndulo ---
    # Si el número de eslabones es muy pequeño, asumimos que estamos probando el péndulo.
    if const.NUM_ESLABONES <= 5:
        print("Usando configuración de péndulo para depuración.")
        # Iniciar el péndulo desde un ángulo para que oscile
        angulo_inicial = np.deg2rad(30)  # 30 grados
        posiciones[0] = np.array([0.0, 0.0])
        if const.NUM_ESLABONES > 1:
            posiciones[1] = np.array([
                const.LONGITUD_ESLABON * np.sin(angulo_inicial),
                -const.LONGITUD_ESLABON * np.cos(angulo_inicial)
            ])

    # --- Lógica Principal: Configuración de la Fuente de Cadena ---
    # Si tenemos un número normal de eslabones, usamos la configuración del experimento.
    else:
        print("Usando configuración de 'fuente' para la simulación completa.")

        # --- 1. Definir la geometría del "recipiente" o mesa ---
        # Estas constantes definen el escenario de nuestro experimento.
        ALTURA_BORDE = 0.5      # Altura 'y' del borde de la mesa desde donde cae la cadena.
        POS_X_BORDE = 0.0       # Posición en 'x' de ese borde.
        ANCHO_RECIPIENTE = 0.2  # Ancho en 'x' donde se apila la cadena.

        num_colgando = 5  # El número de eslabones que cuelgan inicialmente.

        # --- 2. Posicionar los eslabones que cuelgan del borde ---
        # El primer eslabón (i=0) está justo en el borde, y los siguientes caen desde ahí.
        for i in range(num_colgando):
            posiciones[i] = np.array([POS_X_BORDE, ALTURA_BORDE - i * const.LONGITUD_ESLABON])

        # --- 3. Posicionar los eslabones apilados en el recipiente ---
        # Colocamos el resto de la cadena en una pila desordenada a la derecha del borde
        # y, crucialmente, a una pequeña altura SOBRE el suelo (y > 0).
        for i in range(num_colgando, const.NUM_ESLABONES):
            posiciones[i] = np.array([
                # Posición 'x' aleatoria dentro del ancho del recipiente
                POS_X_BORDE + np.random.uniform(0.01, ANCHO_RECIPIENTE),
                # Posición 'y' aleatoria, pero siempre por encima de cero
                np.random.uniform(0.01, 0.1)
            ])

    print("Sistema inicializado con éxito.")
    return posiciones, velocidades

def ejecutar_bucle_simulacion(posiciones, velocidades):
    """
    Ejecuta el bucle principal de la simulación usando el método de Euler-Cromer.
    """
    historial_posiciones = []
    num_pasos = int(const.TIEMPO_TOTAL_SIM / const.DT)

    print(f"Iniciando simulación por {const.TIEMPO_TOTAL_SIM} segundos...")
    print(f"Número total de pasos: {num_pasos}")

    for paso in range(num_pasos):
        # 1. Calcular Fuerzas
        fuerzas = physics.calcular_fuerzas_netas(posiciones, velocidades)
        
        # 2. Actualizar Velocidades
        aceleraciones = fuerzas / const.MASA_ESLABON
        velocidades += aceleraciones * const.DT
        
        # 3. Actualizar Posiciones
        posiciones += velocidades * const.DT

        # --- 4. APLICAR RESTRICCIONES Y COLISIONES ---
        for i in range(const.NUM_ESLABONES):
            # 4a. Colisión con el Suelo (eje y)
            if posiciones[i, 1] < 0.0:
                posiciones[i, 1] = 0.0
                velocidades[i, 1] = 0.0
            
            # --- NUEVO: 4b. Colisión con las Paredes del Recipiente (eje x) ---
            # Pared Izquierda
            if posiciones[i, 0] < const.CONTENEDOR_X_MIN:
                posiciones[i, 0] = const.CONTENEDOR_X_MIN
                # Hacemos que rebote con una pequeña pérdida de energía
                velocidades[i, 0] *= -0.5 
            
            # Pared Derecha
            if posiciones[i, 0] > const.CONTENEDOR_X_MAX:
                posiciones[i, 0] = const.CONTENEDOR_X_MAX
                velocidades[i, 0] *= -0.5

        # 5. Guardar Estado
        if paso % 100 == 0:
            historial_posiciones.append(posiciones.copy())

    print("Simulación completada.")
    return historial_posiciones