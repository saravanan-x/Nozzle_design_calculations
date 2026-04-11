import math
import numpy as np

# Envinomental values

def get_atmosphere_data(h):
    """
    Calculates atmospheric properties based on altitude (h) in meters.
    Returns: temperature (C), pressure (kPa), density (kg/m³),h
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
       
       
    return temp, pressure, density, h

