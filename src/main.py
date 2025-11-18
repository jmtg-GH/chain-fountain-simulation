# src/main.py

"""
Punto de entrada principal para ejecutar la simulación de la fuente de cadena.
"""

# Importamos las funciones clave de nuestros otros módulos
from simulation import inicializar_sistema, ejecutar_bucle_simulacion
from visualization import animar_simulacion

def main():
    """
    Función principal que orquesta la simulación.
    """
    print("Iniciando el programa de simulación de la fuente de cadena.")
    
    # 1. Inicializar el estado del sistema
    posiciones_iniciales, velocidades_iniciales = inicializar_sistema()
    
    # 2. Ejecutar la simulación para obtener el historial de estados
    historial = ejecutar_bucle_simulacion(posiciones_iniciales, velocidades_iniciales)
    
    # 3. Animar el resultado
    if historial:
        animar_simulacion(historial)
    else:
        print("No se generaron datos para animar.")

    print("Programa finalizado.")

# Este es un modismo estándar de Python para ejecutar el código
if __name__ == "__main__":
    main()