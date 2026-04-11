     #Conical Nozzles

rt = dt / 2
re = de / 2 
e = ae / at

throat_angle = 17

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

# total length
l = l1 + ln

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
print("Total length =", l * 1000)


# --- PLOTTING CODE ---
fig, ax = plt.subplots(figsize=(16, 10)) 

ax.set_aspect('equal', adjustable='box')
ax.axis('off') 

pad = Re * 0.2

# GEOMETRY CALCULATIONS
x_chamber_start = -(cl + con_l + l1)
x_chamber_end = -(con_l + l1)
x_conv_end = -l1
y_conv_end = rt + r1 * (1 - np.cos(theta))

def plot_nozzle_side(sign=1):
    ax.plot([x_chamber_start, x_chamber_end], [sign*cr, sign*cr], 'k-', linewidth=2.5)
    ax.plot([x_chamber_end, x_conv_end], [sign*cr, sign*y_conv_end], 'k-', linewidth=2.5)
    t_vals_conv = np.linspace(-np.pi/2 - theta, -np.pi/2, 100)
    ax.plot(r1 * np.cos(t_vals_conv), sign*(r1 * np.sin(t_vals_conv) + (rt + r1)), 'k-', linewidth=2.5)
    t_vals = np.linspace(-np.pi/2, -np.pi/2 + theta, 100)
    ax.plot(r1 * np.cos(t_vals), sign*(r1 * np.sin(t_vals) + (rt + r1)), 'k-', linewidth=2.5)
    ax.plot([l1, l], [sign*rn, sign*Re], 'k-', linewidth=2.5)

plot_nozzle_side(sign=1)
plot_nozzle_side(sign=-1)

ax.plot([x_chamber_start - pad, l + pad], [0, 0], color='gray', linestyle='-.', linewidth=1.5)
ax.text(l + pad*1.2, 0, r'$\mathbb{CL}$', fontsize=20, fontweight='bold', va='center')

# CONSTRUCTION LINES
ax.plot([0, 0], [-(rt+pad), rt+pad], 'k--', linewidth=0.8, alpha=0.5) 
ax.plot([l1, l1], [0, rn + pad], 'k--', linewidth=0.8, alpha=0.5)      
ax.plot([l, l], [0, Re + pad], 'k--', linewidth=0.8, alpha=0.5)        

ax.plot([0, l1], [rt + r1, rn], 'k-', linewidth=1, alpha=0.6)
ax.text(l1/2, rt + r1/2, r'$R_1$', fontsize=15, ha='right')

arc_alpha = patches.Arc((l1, rn), l*0.15, l*0.15, theta1=0, theta2=np.degrees(theta), color='red', linewidth=1.5)
ax.add_patch(arc_alpha)
ax.text(l1 + l*0.08, rn + pad*0.2, r'$\alpha$', fontsize=16, color='red', fontweight='bold')

def draw_dim(x1, y1, x2, y2, text, color='blue', off=0):
    ax.annotate('', xy=(x1, y1), xytext=(x2, y2), arrowprops=dict(arrowstyle='<->', color=color, lw=1.5))
    if x1 == x2: 
        ax.text(x1 - pad*0.3, (y1+y2)/2, text, color=color, fontsize=14, va='center', ha='right', fontweight='bold')
    else: 
        ax.text((x1+x2)/2, y1 - off, text, color=color, fontsize=14, ha='center', va='top', fontweight='bold', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

draw_dim(-pad*0.5, 0, -pad*0.5, rt, r'$R_t$')
draw_dim(l1 - pad*0.2, 0, l1 - pad*0.2, rn, r'$R_N$')
draw_dim(l + pad*0.5, 0, l + pad*0.5, Re, r'$R_e$')

draw_dim(0, -pad*1.5, l1, -pad*1.5, r'$L_1$', off=pad*0.2)
draw_dim(l1, -pad*1.5, l, -pad*1.5, r'$L_N$', off=pad*0.2)
draw_dim(0, -pad*3.0, l, -pad*3.0, r'$L_{total}$', off=pad*0.2)

ax.plot(l1, rn, 'ro', markersize=6)
ax.text(l1, rn + pad*0.3, 'N', color='red', fontsize=16, fontweight='bold', ha='center')


# DATA SUMMARY TABLE ON THE DIAGRAM
stats_text = (
    f"DIMENSIONS (mm):\n"
    f"r1    : {r1*1000:.2f} MM\n"
    f"cl    : {cl*1000:.2f} MM\n"
    f"cr    : {cr*1000:.2f} MM\n"
    f"Con L: {con_l*1000:.2f} MM\n"
    f"rt    : {rt*1000:.2f} MM\n"
    f"re    : {re*1000:.2f} MM\n"
    f"L1    : {l1*1000:.2f} MM\n"
    f"Re    : {Re*1000:.2f} MM\n"
    f"rn    : {rn*1000:.2f} MM\n"
    f"ln    : {ln*1000:.2f} MM\n"
    f"Tot L : {l*1000:.2f} MM\n"
)

# Place the text box in the upper left corner
ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=12,
        verticalalignment='top', family='monospace', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='none', edgecolor='black', alpha=0.5))

ax.set_xlim(x_chamber_start - pad*2, l + pad*3)
ax.set_ylim(-(Re + pad*4), max(cr, rt + r1) + pad*2)

plt.tight_layout()
plt.show() 