# src/physics.py

"""
Módulo para todas las funciones relacionadas con el cálculo de fuerzas
según nuestro modelo físico.
"""

import numpy as np
from . import constants as const

def calcular_fuerzas_netas(posiciones, velocidades):
    """
    Calcula la fuerza neta sobre cada eslabón de la cadena, incluyendo
    gravedad, fuerza de resorte y amortiguamiento.

    Args:
        posiciones (np.ndarray): Array de forma (N, 2) con las posiciones actuales.
        velocidades (np.ndarray): Array de forma (N, 2) con las velocidades actuales.

    Returns:
        np.ndarray: Array de forma (N, 2) con el vector de fuerza neta para cada eslabón.
    """
    num_eslabones = const.NUM_ESLABONES
    fuerzas_netas = np.zeros((num_eslabones, 2), dtype=float)

    # --- 1. Aplicar la Fuerza de Gravedad ---
    # Se aplica a todos los eslabones por igual.
    fuerza_gravedad = const.GRAVEDAD * const.MASA_ESLABON
    fuerzas_netas += fuerza_gravedad

    # --- 2. Aplicar la Fuerza de Conexión (Resorte) ---
    # Se calcula para cada par de eslabones adyacentes.
    for i in range(num_eslabones - 1):
        # Vector que va del eslabón i al i+1
        vector_r = posiciones[i+1] - posiciones[i]
        distancia = np.linalg.norm(vector_r)
        
        # Evitar división por cero si los eslabones están en el mismo punto
        if distancia == 0:
            continue
            
        # Dirección del vector (vector unitario)
        direccion = vector_r / distancia
        
        # Magnitud de la fuerza de resorte (Ley de Hooke)
        magnitud_fuerza = const.K_RESORTE * (distancia - const.LONGITUD_ESLABON)
        
        # **AQUÍ SE DEFINE LA VARIABLE CORRECTAMENTE**
        # Se calcula el vector completo de la fuerza del resorte
        fuerza_resorte = magnitud_fuerza * direccion
        
        # Se aplica la fuerza a ambos eslabones (3ra Ley de Newton: acción y reacción)
        fuerzas_netas[i] += fuerza_resorte
        fuerzas_netas[i+1] -= fuerza_resorte

    # --- 3. Aplicar la Fuerza de Amortiguamiento (Fricción) ---
    # Esta fuerza se opone a la velocidad para disipar energía y estabilizar el sistema.
    fuerza_amortiguamiento = -const.COEF_AMORTIGUAMIENTO * velocidades
    fuerzas_netas += fuerza_amortiguamiento
    
    # --- 4. APLICAR LA FUERZA DE LA FUENTE (REACCIÓN ANÓMALA) ---
    # Esta es la física clave del proyecto.
    # Buscamos el primer eslabón que está siendo levantado de la pila.
    # Iteramos desde el final de la cadena hacia el principio.
    for i in range(num_eslabones - 1, 0, -1):
        # Condición: El eslabón está en la pila Y se está moviendo hacia arriba.
        if posiciones[i, 1] < const.ALTURA_PILA_UMBRAL and velocidades[i, 1] > 0:
            
            # Calcular la magnitud de la velocidad al cuadrado
            v_squared = np.linalg.norm(velocidades[i])**2
            
            # Calcular la magnitud de la fuerza de la fuente
            magnitud_fuerza_fuente = const.DENSIDAD_LINEAL * v_squared
            
            # Aplicar la fuerza como un empuje puramente vertical
            fuerzas_netas[i] += np.array([0.0, magnitud_fuerza_fuente])
            
            # Esta fuerza solo actúa en un eslabón a la vez, así que salimos del bucle
            break

    return fuerzas_netas