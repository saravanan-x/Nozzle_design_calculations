import math
import numpy as np

# Envinomental values

def get_atmosphere_data(h):
    """
    Calculates atmospheric properties based on altitude (h) in meters.
    Returns: temperature (C), pressure (kPa), density (kg/m³)
    """

    if h < 11000:
        # Troposphere 
        temp = 15.04 - 0.00649 * h
        pressure = 101.29 * ((temp + 273.1) / 288.08)**5.256

    elif 11000 <= h <= 25000:
        # Lower Stratosphere
        temp = -56.46
        pressure = 22.65 * math.exp(1.73 - 0.000157 * h)

    else:
        # Upper Stratosphere
        temp = -131.21 + 0.00299 * h
        pressure = 2.488 * ((temp + 273.1) / 216.6)**-11.388

    density = pressure / (0.2869 * (temp + 273.1))

    return temp, pressure, density


# Example
Target_height = 10 #KM
altitude = Target_height * 1000   # Requuired KM of rocket

t, p, rho = get_atmosphere_data(altitude)

temp_k = t + 273.15
pressure_pa = p * 1000
pressure_mpa = pressure_pa / 1e6

print(f"Altitude: {altitude} m")
print(f"Temperature: {t:.2f} °C")
print(f"Temperature: {temp_k:.2f} K")
print(f"Pressure: {p:.2f} kPa")
print(f"Pressure: {pressure_pa:.2f} Pa")
print(f"Pressure: {pressure_mpa:.6f} MPa")
print(f"Density: {rho:.4f} kg/m³")