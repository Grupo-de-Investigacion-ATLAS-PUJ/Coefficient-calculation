import pandas as pd
import numpy as np

# Define the temperature range and intervals
temperature_range = np.arange(-80, 60.1, 0.1)

# Define the Callendar-Van Dusen equation in reverse to find the corresponding resistance for given temperature
def temperature_to_ohms(temperature):
    if temperature >= 0:
        # Use the inverse of the equation for positive temperatures
        resistance = (temperature * 100 + 24536.24) / (0.02350289 + 0.000000001034084 * temperature * 100)
    else:
        # Use the inverse of the equation for negative temperatures
        resistance = (temperature * 100 + 24564.58) / (0.02353718 + 0.000000001027502 * temperature * 100)
    return resistance / 100  # Divide by 100 to match original scale

# Convert resistance to voltage based on provided relationship
def ohms_to_volts(resistance, Vref=0.79932, RV=10e3):
    return Vref * RV / (resistance + Vref)

# Calculate resistance and voltage for each temperature
data = []
for temp in temperature_range:
    resistance = temperature_to_ohms(temp)
    voltage = ohms_to_volts(resistance)
    data.append([temp, voltage])

# Create a DataFrame and export it to Excel
df = pd.DataFrame(data, columns=["Temperature (°C)", "Voltage (V)"])
file_path = "temperature_voltage_data.xlsx"
df.to_excel(file_path, index=False)

print(f"Archivo generado: {file_path}")
