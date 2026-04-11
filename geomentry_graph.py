import matplotlib.pyplot as plt
import main as mn 

def geomentry_graphs(cd_mm, dt_mm, de_mm, lc_mm, conv_mm, div_mm):

    # Convert to radius 
    rc = cd_mm / 2
    rt = dt_mm / 2
    re = de_mm / 2

    # X positions
    x0 = 0
    x1 = lc_mm
    x2 = x1 + conv_mm
    x3 = x2 + div_mm

    # Upper wall
    x_upper = [x0, x1, x2, x3]
    y_upper = [rc, rc, rt, re]

    # Lower wall
    y_lower = [-y for y in y_upper]

    # Plot
    plt.figure(figsize=(12,4))

    plt.plot(x_upper, y_upper, linewidth=3)
    plt.plot(x_upper, y_lower, linewidth=3)

    # throat
    plt.plot([x2,x2],[rt,-rt],'r--')

    plt.title("Rocket Combustion Chamber and Nozzle Geometry")
    plt.xlabel("Length (mm)")
    plt.ylabel("Radius (mm)")
    plt.axis("equal")
    plt.grid(True)

    # Labels
    plt.text(mn.lc_mm/2, rc+3, f"Chamber: {mn.lc_mm:.2f} mm")
    plt.text(x1+mn.conv_mm/4, rc+1, f"Convergent: {mn.conv_mm:.2f} mm")
    plt.text(x2, rt+3, f"Throat: {mn.dt_mm:.2f} mm")
    plt.text(x2+mn.div_mm/2, re+3, f"Divergent: {mn.div_mm:.2f} mm")

    return plt.show()