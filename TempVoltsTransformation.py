import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Define the temperature range and intervals (adjusted step size)
temperature_range = np.arange(-80, 60.01, 0.01)  # Step size of 0.01°C

# Vectorized Callendar-Van Dusen equation to find resistance
def temperature_to_ohms(temperature):
    """
    Convert temperature to resistance using the Callendar-Van Dusen equation.
    This function is vectorized to handle NumPy arrays.
    """
    # Coefficients for Callendar-Van Dusen equation
    R0 = 10000  # Resistance at 0°C (Ohms)
    A = 3.9083e-3
    B = -5.775e-7
    # For temperatures >= 0°C
    resistance_positive = R0 * (1 + A * temperature)
    # For temperatures < 0°C
    resistance_negative = R0 * (1 + A * temperature + B * temperature**2)
    # Use numpy.where to apply the correct formula based on temperature
    resistance = np.where(temperature >= 0, resistance_positive, resistance_negative)
    return resistance

# Constants from the image and calculations
Vref = 0.79932  # Reference voltage (V)
Vo_max = 2.5    # Maximum output voltage (V)
R_V = 10e3      # Resistance value (Ω) selected based on commercial availability
R_Pt_min = 6.8e3  # Minimum sensor resistance at -80°C (Ω)

# RV <= R_Pt_min * (Vo_max / Vref - 1)
RV_limit = R_Pt_min * (Vo_max / Vref - 1)
print(f"RV limit: {RV_limit:.2f} Ω, Selected RV: {R_V:.2f} Ω")

# Convert resistance to voltage based on the corrected relationship from the image
def ohms_to_volts(resistance, Vref=0.79932, RV=1e4):
    """
    Convert resistance to voltage.
    """
    return Vref * ((RV / resistance) + 1)

# Calculate resistance and voltage for each temperature
resistances = temperature_to_ohms(temperature_range)
voltages = ohms_to_volts(resistances)

# Save voltages and temperatures to an Excel file
try:
    data = pd.DataFrame({
        "Temperature (°C)": temperature_range,
        "Resistance (Ohms)": resistances,
        "Voltage (V)": voltages
    })
    data.to_excel("temperature_voltage_data_corrected.xlsx", index=False)
    print("Data successfully saved to 'temperature_voltage_data_corrected.xlsx'.")
except Exception as e:
    print(f"An error occurred while saving the file: {e}")

# Perform polynomial regression to fit temperature to voltage with degree 4
coefficients = np.polyfit(voltages, temperature_range, 4)

# Create the polynomial function using the coefficients
poly_func = np.poly1d(coefficients)

# Display the polynomial equation
# Note: poly1d automatically orders coefficients from highest degree to constant
equation_terms = [f"{coef:.5e} * x^{i}" for i, coef in enumerate(coefficients[::-1])]
equation_str = " + ".join(equation_terms).replace("* x^0", "").replace("x^1", "x")
print("\nPolynomial equation for voltage to temperature:")
print("Temperature = " + equation_str)

# Evaluate the fit quality
temperature_from_fit = poly_func(voltages)
ss_res = np.sum((temperature_range - temperature_from_fit) ** 2)
ss_tot = np.sum((temperature_range - np.mean(temperature_range)) ** 2)
r_squared = 1 - (ss_res / ss_tot)
print(f"R-squared: {r_squared:.4f}")

# Plot to visualize the fit
plt.figure(figsize=(10, 6))
plt.plot(voltages, temperature_range, label="Original data", alpha=0.5)
plt.plot(voltages, poly_func(voltages), label="Polynomial fit", linestyle='--', color='red')
plt.xlabel("Voltage (V)")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.title("Voltage-Temperature Fit")
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot the error between the original and the polynomial fit
error = temperature_range - temperature_from_fit

plt.figure(figsize=(10, 6))
plt.plot(voltages, error, label="Error (Original - Fit)", color='r')
plt.xlabel("Voltage (V)")
plt.ylabel("Error (°C)")
plt.title("Error between Original Temperature and Polynomial Fit")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Example calculation for a given voltage
test_voltage = 1.457007  # Original voltage without scaling

# Using the polynomial function
temperature_from_poly = poly_func(test_voltage)

# Using the original equations by finding the closest temperature
closest_temp_index = (np.abs(voltages - test_voltage)).argmin()
temperature_from_equation = temperature_range[closest_temp_index]

print(f"\nFor a voltage of {test_voltage:.6f} V:")
print(f"Temperature (using polynomial coefficients): {temperature_from_poly:.2f} °C")

# Example calculation for a given temperature to find resistance
test_temperature = 60  # Example temperature in °C
resistance_from_temperature = temperature_to_ohms(test_temperature)
print(f"\nFor a temperature of {test_temperature} °C:")
print(f"Resistance: {resistance_from_temperature:.2f} Ohms")

test_temperature2 = -80 # Example temperature in °C
resistance_from_temperature2 = temperature_to_ohms(test_temperature2)
print(f"\nFor a temperature of {test_temperature2} °C:")
print(f"Resistance: {resistance_from_temperature2:.2f} Ohms")

# Conditional pause
if __name__ == "__main__":
    input("Press Enter to exit...")