import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargar los datos desde el archivo Excel
# Asegúrate de que el archivo 'temperature_voltage_data_corrected2.xlsx' esté en el mismo directorio que este script
archivo_excel = 'temperature_voltage_data_corrected.xlsx'

try:
    # Leer el archivo Excel
    datos = pd.read_excel(archivo_excel)

    # Verificar que las columnas A y C existen
    # Asumiendo que la columna A es 'Temperatura' y la columna C es 'Voltaje'
    # Puedes ajustar los nombres de las columnas según tu archivo
    temperatura = datos.iloc[:, 0]  # Columna A (índice 0)
    voltaje = datos.iloc[:, 2]       # Columna C (índice 2)

    # Convertir a numpy arrays
    voltaje_np = voltaje.values * 1e6  # Convertir V a µV
    temperatura_np = temperatura.values

    # Ajustar un polinomio de 4º grado: T = f(µV)
    grado = 4
    coeficientes = np.polyfit(voltaje_np, temperatura_np, grado)
    polinomio = np.poly1d(coeficientes)

    print("Polinomio ajustado (Temperatura = f(Microvoltaje)):")
    print(polinomio)

    # Definir una función para obtener la temperatura dado un microvoltaje
    def obtener_temperatura_microvoltios(microvoltaje_valor):
        """
        Calcula la temperatura correspondiente a un valor de microvoltaje utilizando el polinomio ajustado.

        Parámetros:
            microvoltaje_valor (float): Valor del microvoltaje en µV.

        Retorna:
            float: Temperatura estimada en °C.
        """
        return polinomio(microvoltaje_valor)

    # Ejemplo de uso:
    # Solicitar al usuario un valor de microvoltaje y mostrar la temperatura correspondiente
    while True:
        try:
            entrada = input("Introduce un valor de microvoltaje en µV (o 'salir' para terminar): ")
            if entrada.lower() == 'salir':
                break
            microvoltaje_input = float(entrada)
            temperatura_resultado = obtener_temperatura_microvoltios(microvoltaje_input)
            print(f"Temperatura estimada: {temperatura_resultado:.2f} °C\n")
        except ValueError:
            print("Por favor, introduce un número válido o 'salir' para terminar.\n")

    # (Opcional) Visualizar el ajuste polinomial
    visualizar = input("¿Deseas visualizar el ajuste polinomial? (s/n): ").lower()
    if visualizar == 's':
        plt.scatter(voltaje_np, temperatura_np, label='Datos Reales', color='blue')

        # Crear un rango de microvoltajes para graficar el polinomio
        microvoltaje_rango = np.linspace(min(voltaje_np), max(voltaje_np), 500)
        temperatura_rango = polinomio(microvoltaje_rango)

        plt.plot(microvoltaje_rango, temperatura_rango, label='Polinomio de 4º grado', color='red')
        plt.xlabel('Microvoltaje (µV)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Ajuste Polinomial de Temperatura vs. Microvoltaje')
        plt.legend()
        plt.grid(True)
        plt.show()

except FileNotFoundError:
    print(f"El archivo '{archivo_excel}' no se encontró. Asegúrate de que esté en el directorio correcto.")
except Exception as e:
    print(f"Ocurrió un error: {e}")
