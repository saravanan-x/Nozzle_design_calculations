                                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~BELL NOZZLE GEOMETRY~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# CONVERGENT & CONICAL SETUP CALCULATIONS

rt = dt / 2
re = de / 2 
e = ae / at

throat_angle = 25
theta = np.radians(throat_angle) 

r1 = 1.5 * rt
Re = np.sqrt(e) * rt
rn = rt + r1 * (1 - np.cos(theta))

# arc length
l1 = r1 * np.sin(theta)

# CONVERTING MILLIMETERS TO METERS FOR PLOTTING
cl = lc_mm / 1000              # Chamber length converted to meters
cr = (cd_mm / 2) / 1000        # Chamber radius converted to meters
con_l = (conv_mm / 1000) - l1  # Convergent length converted to meters

# conical length
ln = (rt * (np.sqrt(e) - 1) + r1 * (np.cos(theta) - 1)) / np.tan(theta)

print("--- CONICAL / CONVERGENT DATA ---")
print("r1 =", r1 * 1000)
print("cl =", cl * 1000)
print("cr =", cr * 1000)
print("covergen length =", con_l * 1000)
print("e =", e * 1000)
print("rt =", rt * 1000)
print("re =", re * 1000)
print("l1 =", l1 * 1000)
print("Re =", Re * 1000)
print("rn =", rn * 1000)
print("ln =", ln * 1000)


# BELL NOZZLE DESIGN (AFTER N POINT)

# OVERWRITING r1 for the Bell throat downstream radius
r1 = 0.382 * rt

# Slop Angles
θn = 30
θe = 8.5

# angles (convert to radians)
tita_n = np.radians(θn)
tita_e = np.radians(θe)

# Point N
xn = r1 * np.sin(tita_n)
yn = rt + r1 * (1 - np.cos(tita_n))

# LENGTH (Rao method) 
f = 0.8   # length factor (60%–80%)
l = f * (rt / np.tan(np.radians(15))) * (
        np.sqrt(e - 1) + 1.5 * ((1 / np.cos(np.radians(15))) - 1))

# ---- PARABOLIC BELL EQUATION ----
# r(x) from Rao
x = np.linspace(xn, l, 100)
rx = yn + np.tan(tita_n) * (x - xn) \
         + ((np.tan(tita_e) - np.tan(tita_n)) / (2 * (l - xn))) * (x - xn)**2

# 4 BOUNDARY CONDITION CHECKS
r_start = yn
r_exit = yn + np.tan(tita_n) * (l - xn) \
             + ((np.tan(tita_e) - np.tan(tita_n)) / (2 * (l - xn))) * (l - xn)**2
slope_N = np.tan(tita_n)
slope_exit = np.tan(tita_n) + \
                 ((np.tan(tita_e) - np.tan(tita_n)) / (l - xn)) * (l - xn)

print("\n---- BELL BOUNDARY CHECK ----")
print("At N (radius)      :", r_start)
print("At Exit (radius)   :", r_exit, "Expected:", re)
print("Slope at N         :", slope_N, "Expected:", np.tan(tita_n))
print("Slope at Exit      :", slope_exit, "Expected:", np.tan(tita_e))
print(f"LENGTH (Rao method) :{l*1000}")



# DIAGRAM SHEET PLOTTING

fig, ax = plt.subplots(figsize=(20, 10)) 

ax.set_aspect('equal', adjustable='box')
ax.axis('off') 

pad = Re * 0.5

# PRESERVED CONVERGENT GEOMETRY (Using the 1.5 * rt logic)
r1_conv = 1.5 * rt
l1_conv = r1_conv * np.sin(theta)
y_conv_end = rt + r1_conv * (1 - np.cos(theta))

x_chamber_start = -(cl + con_l + l1_conv)
x_chamber_end = -(con_l + l1_conv)
x_conv_end = -l1_conv

def plot_nozzle_side(sign=1):
    # 1. Chamber
    ax.plot([x_chamber_start, x_chamber_end], [sign*cr, sign*cr], 'k-', linewidth=2.5)
    # 2. Convergent Wall
    ax.plot([x_chamber_end, x_conv_end], [sign*cr, sign*y_conv_end], 'k-', linewidth=2.5)
    # 3. Convergent Arc (uses the 1.5*rt radius)
    t_vals_conv = np.linspace(-np.pi/2 - theta, -np.pi/2, 100)
    ax.plot(r1_conv * np.cos(t_vals_conv), sign*(r1_conv * np.sin(t_vals_conv) + (rt + r1_conv)), 'k-', linewidth=2.5)
    
    # 4. Divergent Arc (Throat to N) - Uses Bell r1 (0.382*rt) & tita_n
    t_vals_div = np.linspace(-np.pi/2, -np.pi/2 + tita_n, 100)
    ax.plot(r1 * np.cos(t_vals_div), sign*(r1 * np.sin(t_vals_div) + (rt + r1)), 'k-', linewidth=2.5)
    
    # 5. Bell Curve (N to Exit) - Uses Rao Parabolic array
    ax.plot(x, sign*rx, 'k-', linewidth=2.5)

# Plot top and bottom
plot_nozzle_side(sign=1)
plot_nozzle_side(sign=-1)

# CENTERLINE
ax.plot([x_chamber_start - pad, l + pad], [0, 0], color='gray', linestyle='-.', linewidth=1.5)
ax.text(l + pad*1.2, 0, r'$\mathbb{CL}$', fontsize=20, fontweight='bold', va='center')

# CONSTRUCTION LINES (Updated to use xn, yn for Point N)
ax.plot([0, 0], [-(rt+pad), rt+pad], 'k--', linewidth=0.8, alpha=0.5)  # Throat
ax.plot([xn, xn], [0, yn + pad], 'k--', linewidth=0.8, alpha=0.5)      # Point N
ax.plot([l, l], [0, Re + pad], 'k--', linewidth=0.8, alpha=0.5)        # Exit

# Radius Construction for R1 (Bell downstream)
ax.plot([0, xn], [rt + r1, yn], 'k-', linewidth=1, alpha=0.6)
ax.text(xn/2, rt + r1/2, r'$R_1 (div)$', fontsize=12, ha='right')

# ANGLE LABEL for Theta_N
arc_alpha = patches.Arc((xn, yn), l*0.15, l*0.15, theta1=0, theta2=np.degrees(tita_n), color='red', linewidth=1.5)
ax.add_patch(arc_alpha)
ax.text(xn + l*0.05, yn + pad*0.2, r'$\theta_N$', fontsize=16, color='red', fontweight='bold')

# DIMENSIONING FUNCTION
def draw_dim(x1, y1, x2, y2, text, color='blue', off=0):
    ax.annotate('', xy=(x1, y1), xytext=(x2, y2), arrowprops=dict(arrowstyle='<->', color=color, lw=1.5))
    if x1 == x2: 
        ax.text(x1 - pad*0.3, (y1+y2)/2, text, color=color, fontsize=14, va='center', ha='right', fontweight='bold')
    else: 
        ax.text((x1+x2)/2, y1 - off, text, color=color, fontsize=14, ha='center', va='top', fontweight='bold', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

# Vertical Dimensions (Radii)
draw_dim(-pad*0.5, 0, -pad*0.5, rt, r'$R_t$')
draw_dim(xn - pad*0.2, 0, xn - pad*0.2, yn, r'$R_N$')
draw_dim(l + pad*0.5, 0, l + pad*0.5, Re, r'$R_e$')

# Horizontal Dimensions (Lengths) - Updated to Bell dimensions
draw_dim(0, -pad*1.5, xn, -pad*1.5, r'$L_N$', off=pad*0.2)
draw_dim(xn, -pad*1.5, l, -pad*1.5, r'$L_{Bell}$', off=pad*0.2)
draw_dim(0, -pad*3.0, l, -pad*3.0, r'$L_{total}$', off=pad*0.2)

# Label Point N
ax.plot(xn, yn, 'ro', markersize=6)
ax.text(xn, yn + pad*0.3, 'N', color='red', fontsize=16, fontweight='bold', ha='center')

# DATA SUMMARY TABLE (Updated with Bell Data)
stats_text = (
    f"BELL NOZZLE DIMENTIONS (mm):\n"
    f"cl       : {cl*1000:.2f} \n"
    f"cr       : {cr*1000:.2f} \n"
    f"Con L    : {con_l*1000:.2f} \n"
    f"rt       : {rt*1000:.2f} \n"
    f"re       : {re*1000:.2f} \n"
    f"xn(LN)   : {xn*1000:.2f} \n"
    f"yn(RN)   : {yn*1000:.2f} \n"
    f"Re       : {Re*1000:.2f} \n"
    f"Tot L    : {l*1000:.2f} \n"
    f"f-fact   : {f}\n"
)

ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=12,
        verticalalignment='top', family='monospace', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='none', edgecolor='black', alpha=0.5))

ax.set_xlim(x_chamber_start - pad*2, l + pad*3)
ax.set_ylim(-(Re + pad*4), max(cr, rt + r1_conv) + pad*2)

plt.tight_layout()
plt.show()