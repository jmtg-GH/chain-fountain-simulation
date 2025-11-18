# src/visualization.py

"""
Módulo para la visualización y animación de los resultados de la simulación.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from . import constants as const

def animar_simulacion(historial_posiciones):
    """
    Crea y muestra una animación de la simulación de la cadena.

    Args:
        historial_posiciones (list): Lista de arrays de posiciones a lo largo del tiempo.
    """
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    
    # Configurar los límites de los ejes para que la cadena se vea bien
    ax.set_xlim(-const.LONGITUD_TOTAL * 0.5, const.LONGITUD_TOTAL * 1.5)
    ax.set_ylim(-const.LONGITUD_TOTAL * 1.2, const.LONGITUD_TOTAL * 0.8)
    ax.grid()
    ax.set_title("Simulación de la Fuente de Cadena")

    # El objeto que dibujaremos (la cadena) se inicializa vacío
    line, = ax.plot([], [], 'o-', lw=2, label="Cadena")
    
    # Función de inicialización para la animación
    def init():
        line.set_data([], [])
        return line,

    # Función que se llama en cada fotograma de la animación
    def update(frame):
        # frame es el array de posiciones en un instante de tiempo
        x_data = frame[:, 0]
        y_data = frame[:, 1]
        line.set_data(x_data, y_data)
        return line,

    # Crear la animación
    ani = animation.FuncAnimation(fig, update, frames=historial_posiciones,
                                  init_func=init, blit=True, interval=20)

    plt.legend()
    plt.show()