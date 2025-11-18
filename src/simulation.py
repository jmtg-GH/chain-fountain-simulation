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
    Crea y devuelve los arrays iniciales para las posiciones y velocidades
    de los eslabones de la cadena.

    Retorna:
        tuple: (posiciones, velocidades)
               - posiciones (np.ndarray): Array de forma (N, 2) con las posiciones [x, y] de cada eslabón.
               - velocidades (np.ndarray): Array de forma (N, 2) con las velocidades [vx, vy] de cada eslabón.
    """
    # Creamos los arrays vacíos con el tamaño correcto (NUM_ESLABONES x 2 dimensiones)
    posiciones = np.zeros((const.NUM_ESLABONES, 2), dtype=float)
    velocidades = np.zeros((const.NUM_ESLABONES, 2), dtype=float)

    # --- Configuración Inicial de la Cadena ---
    # Colocamos los primeros 5 eslabones colgando del borde (en x=0)
    # y el resto apilados en el "recipiente" (una pila en el suelo a la derecha).
    
    num_colgando = 5
    
    # Eslabones colgando (formando una línea vertical hacia abajo desde el origen)
    for i in range(num_colgando):
        posiciones[i] = np.array([0.0, -i * const.LONGITUD_ESLABON])

    # Eslabones en el recipiente (apilados en una pequeña pila en el suelo)
    for i in range(num_colgando, const.NUM_ESLABONES):
        # Pequeña variación aleatoria para que no estén perfectamente alineados
        posiciones[i] = np.array([0.1 + np.random.uniform(-0.01, 0.01), 0.0])

    print("Sistema inicializado con éxito.")
    print(f"Número de eslabones: {const.NUM_ESLABONES}")
    
    return posiciones, velocidades

def ejecutar_bucle_simulacion(posiciones, velocidades):
    """
    Ejecuta el bucle principal de la simulación usando el método de Euler-Cromer.

    Args:
        posiciones (np.ndarray): Estado inicial de las posiciones.
        velocidades (np.ndarray): Estado inicial de las velocidades.
    
    Returns:
        list: Una lista de arrays de posiciones, guardando el estado en cada paso.
    """
    historial_posiciones = []
    num_pasos = int(const.TIEMPO_TOTAL_SIM / const.DT)

    print(f"Iniciando simulación por {const.TIEMPO_TOTAL_SIM} segundos...")
    print(f"Número total de pasos: {num_pasos}")

    for paso in range(num_pasos):
        # 1. Calcular todas las fuerzas netas basadas en las posiciones actuales
        fuerzas = physics.calcular_fuerzas_netas(posiciones)
        
        # 2. Actualizar las velocidades (Método de Euler-Cromer)
        # v(t+dt) = v(t) + (F/m) * dt
        aceleraciones = fuerzas / const.MASA_ESLABON
        velocidades += aceleraciones * const.DT
        
        # 3. Actualizar las posiciones usando las *nuevas* velocidades
        # x(t+dt) = x(t) + v(t+dt) * dt
        posiciones += velocidades * const.DT
        
        # Guardar el estado actual para la visualización posterior
        # Guardamos una copia para que no se modifique en el siguiente paso
        if paso % 100 == 0: # Guardamos 1 de cada 100 pasos para no usar demasiada memoria
            historial_posiciones.append(posiciones.copy())

    print("Simulación completada.")
    return historial_posiciones