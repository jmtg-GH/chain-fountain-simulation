# src/constants.py

"""
Módulo para definir todas las constantes físicas y de simulación del proyecto.
Centralizar las constantes aquí permite modificar los parámetros del experimento
fácilmente sin alterar la lógica del código.
"""

import numpy as np

# --- Constantes Físicas ---
GRAVEDAD = np.array([0.0, -9.778])  # Aceleración gravitacional en m/s^2 (vector 2D)

# --- Parámetros de la Cadena ---
NUM_ESLABONES = 50              # (N) Número de masas puntuales en la cadena
MASA_TOTAL = 0.5                # (M) Masa total de la cadena en kg
LONGITUD_TOTAL = 1.0            # (L) Longitud total de la cadena en m

# --- Parámetros Derivados (calculados a partir de los anteriores) ---
MASA_ESLABON = MASA_TOTAL / NUM_ESLABONES  # (m) Masa de un solo eslabón
LONGITUD_ESLABON = LONGITUD_TOTAL / (NUM_ESLABONES - 1) if NUM_ESLABONES > 1 else 0 # (L0) Longitud de reposo

# --- Parámetros de la Simulación ---
DT = 0.0001                     # (dt) Paso de tiempo en segundos. Un valor pequeño para estabilidad.
TIEMPO_TOTAL_SIM = 5.0          # Tiempo total a simular en segundos

# --- Parámetros del Modelo Físico ---
K_RESORTE = 1e4                 # Constante de rigidez del resorte (muy alta para simular un eslabón rígido)
COEF_AMORTIGUAMIENTO = 5.0      # (gamma) Coeficiente para disipar energía y estabilizar la simulación.

# --- Parámetros Derivados ---
MASA_ESLABON = MASA_TOTAL / NUM_ESLABONES
LONGITUD_ESLABON = LONGITUD_TOTAL / (NUM_ESLABONES - 1) if NUM_ESLABONES > 1 else 0
DENSIDAD_LINEAL = MASA_TOTAL / LONGITUD_TOTAL # (lambda) Densidad de masa lineal en kg/m

# ... (constantes existentes) ...

# --- Parámetros del Modelo Físico ---
K_RESORTE = 1e4
COEF_AMORTIGUAMIENTO = 5.0
# Umbral de altura para considerar que un eslabón está "en la pila"
ALTURA_PILA_UMBRAL = LONGITUD_ESLABON * 2.0

# --- Parámetros del Escenario ---
# Coordenadas 'x' de las paredes del recipiente
CONTENEDOR_X_MIN = 0.0
CONTENEDOR_X_MAX = 0.2