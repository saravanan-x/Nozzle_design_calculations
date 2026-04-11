import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import importlib
import atmosphere_data as at_data
import pandas as pd
from matplotlib.patches import Arc

# Parameters

g = 9.80665
pi = np.pi

def geometry(g, f, pc, pe, tc, y, r, sy, SF):

    # angles
    divergent_angle = 15 #(12 - 18)
    convergent_a = 30 #(30 - 45)

    da = np.radians(divergent_angle)
    ca = np.radians(convergent_a)

    # characteristic length
    length = 0.5 #(0.5 - 1)M

    # Exit velocity
    ve = np.sqrt((2*y/(y-1))*r*tc*(1-(pe/pc)**((y-1)/y)))

    # mass flow
    m = f/ve

    # throat area
    at = (m/pc)* np.sqrt( ((r*tc) / y) * (((y+1) / 2)**((y+1) / (2*(y-1)))))
    #at = (m/pc) * np.sqrt((r*tc)/y)

    # throat diameter
    dt = np.sqrt((4*at)/pi)

    #  Exit Mach
    me = np.sqrt((2/(y-1))*(((pc/pe)**((y-1)/y))-1))

    #  Area ratio (A/A*)
    # Ar = ((y+1)/2)**(-(y+1)/(2*(y-1))) * ((1 + ((y-1)/2)*me**2)**((y+1)/(2*(y-1))) / me )
    # print(f"ratio of area: {Ar:.4f}")

    # Exit area 
    # ae = at * Ar
    ae = (at/me) * (((1+((y-1)/2)*(me**2)) / ((y+1)/2))**((y+1)/(2*(y-1))))

    #exit diameter
    de = np.sqrt((4*ae)/pi)

    # chamber diameter
    cd = 3*dt

    # chamber area
    ac = (pi*(cd**2))/4

    # chamber length
    lc = (length*at)/ac

    # convergent length
    convergent_length = (cd-dt)/(2*np.tan(ca))

    # divergent length
    divergent_length = (de-dt)/(2*np.tan(da))

    # total length
    total_length = lc + convergent_length + divergent_length

    # Chamber wall thickness
    tw = (pc*cd)/16000
    s = (pc*cd)/(2*tw)

    # thickness
    t = (pc * cd * SF) / (2 * sy)

    # convert to mm
    dt_mm = dt*1000
    de_mm = de*1000
    cd_mm = cd*1000
    lc_mm = lc*1000
    conv_mm = convergent_length*1000
    div_mm = divergent_length*1000
    total_mm = total_length*1000
    s_mm = t*1000


    return ve, m, at, me, ae, cd_mm, lc_mm, conv_mm, dt_mm, div_mm, de_mm, total_mm, s_mm



