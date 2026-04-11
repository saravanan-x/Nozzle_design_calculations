import numpy as np
import math
import nozzle_geomentry as noz_geo
import importlib
import geomentry_graph as gg

importlib.reload(noz_geo)

g = 9.80665
f  = 3000    # N
pc = 3.468e6 # mpa - pa (e6) Chamber pressure
pe = 0.02e6  # mpa - pa (e6) (Expantions Ratio) for Liquid engine if Solid (0.1e6)
tc = 3300    # K  - Chamber Tempreture
y  = 1.22     # or K Specific heat ratio
r  = 355.4    # J/Kgh   gas constant
pi = np.pi
sy = 250e6  # Pa sigma_yield for thickness
SF = 2

#    1.nozzle_geomentry

ve, m, at, me, ae, cd_mm, lc_mm, conv_mm, dt_mm, div_mm, de_mm, total_mm, s_mm = noz_geo.geometry(
    g, f, pc, pe, tc, y, r, sy, SF
)





#     2.geomentry graph
globals().update(locals())

gg.geomentry_graphs(cd_mm, dt_mm, de_mm, lc_mm, conv_mm, div_mm)


print(f"Exit velocity: {ve:.2f} m/s")
print(f"Required Mass flow rate: {m:.4f} kg/s")
print(f"Area of throat: {at:.6f} m^2")
print(f"Exit Mach number: {me:.2f}")
print(f"Area of Exit: {ae:.6f} m^2")

print(f"Chamber diameter: {cd_mm:.2f} mm")
print(f"Chamber length: {lc_mm:.2f} mm")
print(f"Convergent length: {conv_mm:.2f} mm")
print(f"Throat diameter: {dt_mm:.2f} mm")
print(f"Divergent length: {div_mm:.2f} mm")
print(f"Exit diameter: {de_mm:.2f} mm")
print(f"Total length: {total_mm:.2f} mm")
print(f"Chamber wall thickness : {s_mm:.2f} mm")

