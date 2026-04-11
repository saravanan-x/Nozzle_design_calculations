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



# ploting the graph
fig = plt.figure(figsize=(22, 10)) 

# --- 2D PLOT  ---
ax1 = fig.add_subplot(121)
ax1.set_aspect('equal', adjustable='box')
ax1.grid(True, linestyle='--', alpha=0.6) 

pad = Re * 0.5

# PRESERVED CONVERGENT GEOMETRY
r1_conv = 1.5 * rt
l1_conv = r1_conv * np.sin(theta)
y_conv_end = rt + r1_conv * (1 - np.cos(theta))

# Geometry anchors
x_chamber_end = -(con_l + l1_conv)
x_conv_end = -l1_conv

# CORRECTED ARC RADIANS: Ensuring they meet perfectly at x=0
# Convergent Arc: ends exactly at -90 degrees (x=0)
t_vals_conv = np.linspace(-np.pi/2 - theta, -np.pi/2, 100)
# Divergent Arc: starts exactly at -90 degrees (x=0)
t_vals_div = np.linspace(-np.pi/2, -np.pi/2 + tita_n, 100)

def plot_nozzle_side(sign=1):
    # --- CONVERGENT SECTION  ---
    # 2. Convergent Wall
    ax1.plot([x_chamber_end, x_conv_end], [sign*cr, sign*y_conv_end], 'r-', linewidth=2.5)
    
    # 3. Convergent Arc - Center is at x=0, y=sign*(rt + r1_conv)
    ax1.plot(r1_conv * np.cos(t_vals_conv), sign*(r1_conv * np.sin(t_vals_conv) + (rt + r1_conv)), 'r-', linewidth=2.5)
    
    # --- DIVERGENT SECTION ---
    # 4. Divergent Arc (Throat to N) - Center is at x=0, y=sign*(rt + r1)
    ax1.plot(r1 * np.cos(t_vals_div), sign*(r1 * np.sin(t_vals_div) + (rt + r1)), 'r-', linewidth=2.5)
    
    # 5. Bell Curve (N to Exit) 
    bell_mask = x >= xn
    ax1.plot(x[bell_mask], sign*rx[bell_mask], 'r-', linewidth=2.5)

# Plot top and bottom on 2D axis
plot_nozzle_side(sign=1)
plot_nozzle_side(sign=-1)

# CENTERLINE
ax1.plot([x_chamber_end - pad, l + pad], [0, 0], color='gray', linestyle='-.', linewidth=1.5)
ax1.text(l + pad*1.2, 0, r'$\mathbb{CL}$', fontsize=20, fontweight='bold', va='center')

# CONSTRUCTION LINES
ax1.plot([0, 0], [-(rt+pad), rt+pad], 'k--', linewidth=0.8, alpha=0.5)  # Throat
ax1.plot([xn, xn], [0, yn + pad], 'k--', linewidth=0.8, alpha=0.5)      # Point N
ax1.plot([l, l], [0, Re + pad], 'k--', linewidth=0.8, alpha=0.5)        # Exit

# Radius Construction for R1 
ax1.plot([0, xn], [rt + r1, yn], 'k-', linewidth=1, alpha=0.6)
ax1.text(xn/2, rt + r1/2, r'$R_1 (div)$', fontsize=12, ha='right')

# DIMENSIONING
def draw_dim(x1, y1, x2, y2, text, color='black', off=0):
    ax1.annotate('', xy=(x1, y1), xytext=(x2, y2), arrowprops=dict(arrowstyle='<->', color=color, lw=1.5))
    if x1 == x2: 
        ax1.text(x1 - pad*0.3, (y1+y2)/2, text, color=color, fontsize=12, va='center', ha='right', fontweight='bold')
    else: 
        ax1.text((x1+x2)/2, y1 - off, text, color=color, fontsize=12, ha='center', va='top', fontweight='bold')

draw_dim(-pad*0.5, 0, -pad*0.5, rt, r'$R_t$')
draw_dim(xn - pad*0.2, 0, xn - pad*0.2, yn, r'$R_N$')
draw_dim(l + pad*0.5, 0, l + pad*0.5, Re, r'$R_e$')
draw_dim(0, -pad*1.5, xn, -pad*1.5, r'$L_N$', off=pad*0.2)
draw_dim(xn, -pad*1.5, l, -pad*1.5, r'$L_{Bell}$', off=pad*0.2)

# DATA SUMMARY TABLE
stats_text = (
    f"FIXED THROAT GEOMETRY (mm):\n"
    f"rt       : {rt*1000:.2f} \n"
    f"re       : {re*1000:.2f} \n"
    f"Tot L    : {l*1000:.2f} \n"
    f"Angle N  : {θn}°\n"
)
ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes, fontsize=11,
        verticalalignment='top', family='monospace', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', alpha=0.8))

ax1.set_xlim(x_chamber_end - pad*2, l + pad*3)
ax1.set_ylim(-(Re + pad*2), max(cr, rt + r1_conv) + pad*2)
ax1.set_title("2D Fixed Throat Profile", fontsize=16, fontweight='bold')

#  3D PLOT 
ax2 = fig.add_subplot(122, projection='3d')

# Generate arrays for 3D rotation
x_conv_wall_arr = np.linspace(x_chamber_end, x_conv_end, 20)
y_conv_wall_arr = np.linspace(cr, y_conv_end, 20)

x_conv_arc_arr = r1_conv * np.cos(t_vals_conv)
y_conv_arc_arr = r1_conv * np.sin(t_vals_conv) + (rt + r1_conv)

x_div_arc_arr = r1 * np.cos(t_vals_div)
y_div_arc_arr = r1 * np.sin(t_vals_div) + (rt + r1)


X_full = np.concatenate([x_conv_wall_arr, x_conv_arc_arr, x_div_arc_arr[1:], x[x > xn]])
Y_full = np.concatenate([y_conv_wall_arr, y_conv_arc_arr, y_div_arc_arr[1:], rx[x > xn]])

Theta_rot = np.linspace(0, 2*np.pi, 60)
X_mesh, T_mesh = np.meshgrid(X_full, Theta_rot)
Y_mesh = Y_full * np.cos(T_mesh)
Z_mesh = Y_full * np.sin(T_mesh)

ax2.plot_surface(X_mesh, Y_mesh, Z_mesh, color='darkgray', alpha=0.6, 
                 edgecolor='darkgray', linewidth=0.1)

ax2.set_title("3D Nozzle Surface", fontsize=16, fontweight='bold')
ax2.view_init(elev=15, azim=-60)

plt.tight_layout()
plt.show()