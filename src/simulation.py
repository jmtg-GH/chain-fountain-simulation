# src/simulation.py

"""
Módulo que contiene la lógica principal de la simulación, incluyendo la
inicialización del sistema y el bucle de integración temporal.
"""

import numpy as np
from . import constants as const # Usamos un punto para importación relativa dentro del paquete 'src'

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