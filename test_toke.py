import math


def time_dilation(distance, mass):
    # Gravitational constant
    G = 6.674 * 10 ** -11

    # Speed of light
    c = 299792458

    # Schwarzschild radius
    R = 2 * G * mass / (c ** 2)

    # Gravitational time dilation factor
    f = math.sqrt(1 - (R / distance))

    # Time dilation relative to the observer
    dilation = 1 / f

    # Convert dilation to earth years per 5 minutes
    dilation_years_per_5_minutes = dilation * (5 / 7)

    return dilation_years_per_5_minutes


import math


def time_dilation(distance):
    # Schwarzschild radius
    R = 2 * G * M / (c ** 2)

    # Gravitational time dilation factor
    f = math.sqrt(1 - (R / distance))

    # Time dilation relative to the observer
    dilation = 1 / f

    # Convert dilation to earth years per 5 minutes
    dilation_years_per_5_minutes = dilation * (5 / 7)

    return dilation_years_per_5_minutes
