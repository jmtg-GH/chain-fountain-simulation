# src/physics.py

"""
Módulo para todas las funciones relacionadas con el cálculo de fuerzas
según nuestro modelo físico.
"""

import numpy as np
from . import constants as const

def calcular_fuerzas_netas(posiciones):
    """
    Calcula la fuerza neta sobre cada eslabón de la cadena.

    Args:
        posiciones (np.ndarray): Array de forma (N, 2) con las posiciones actuales.

    Returns:
        np.ndarray: Array de forma (N, 2) con el vector de fuerza neta para cada eslabón.
    """
    num_eslabones = const.NUM_ESLABONES
    fuerzas_netas = np.zeros((num_eslabones, 2), dtype=float)

    # 1. Aplicar la Fuerza de Gravedad a todos los eslabones
    fuerza_gravedad = np.array([0.0, -const.MASA_ESLABON * 9.81])
    fuerzas_netas += fuerza_gravedad

    # 2. Aplicar la Fuerza de Conexión (Resorte) entre eslabones adyacentes
    # Iteramos desde el primer hasta el penúltimo eslabón para calcular la fuerza con el siguiente.
    for i in range(num_eslabones - 1):
        # Vector que va del eslabón i al i+1
        vector_r = posiciones[i+1] - posiciones[i]
        
        # Distancia actual entre los eslabones
        distancia = np.linalg.norm(vector_r)
        
        # Si la distancia es cero, no podemos normalizar, así que saltamos
        if distancia == 0:
            continue
            
        # Dirección del vector (vector unitario)
        direccion = vector_r / distancia
        
        # Magnitud de la fuerza de resorte (Ley de Hooke)
        # F = k * (distancia_actual - longitud_reposo)
        magnitud_fuerza = const.K_RESORTE * (distancia - const.LONGITUD_ESLABON)
        
        # Vector de la fuerza de resorte
        fuerza_resorte = magnitud_fuerza * direccion
        
        # Aplicamos las fuerzas según la tercera ley de Newton (acción y reacción)
        fuerzas_netas[i] += fuerza_resorte
        fuerzas_netas[i+1] -= fuerza_resorte

    return fuerzas_netas