# Envinomental values
pa = pressure_pa  
ta = temp_k        

#Throat Radius
Trs = 3.6837
tr = (2*Trs)/1000

#Exit Radius
Er = 0.0807
er = (Er*2)/1000

#outside air pressure and tempreture
p = 24.5
t = 245

# Exit Mach
me = np.sqrt((2/(y-1))*((pc/pe)**((y-1)/y)-1))
print(f"Exit Mach number: {me:.2f}")

# General mass flow rate (check)
mg = ((at * pc) / np.sqrt(tc)) * np.sqrt(y / r) * (
    me * (1 + ((y - 1) / 2) * me**2)**(-(y + 1) / (2 * (y - 1))))

print(f"General mass flow rate: {mg:.4f} kg/s")

# Choked mass flow rate:
mc = ((at * pc) / np.sqrt(tc)) * (np.sqrt(y / r)) * (((y + 1) / 2)**(-((y + 1) / (2 * (y - 1)))))

print(f"Choked mass flow rate: {mc:.4f} kg/s")

# ratio of area
Ar = ((y+1)/2)**(- (y+1)/(2 * (y-1))) * (((1 + ((y-1)/2) * me**2)**((y+1)/(2 * (y-1)))) / me)
print(f"Ratio of area   :{Ar}")


# Nozzle area ratio
ar = ae/at
print(f"Nozzle area ratio   :{ar}")

# Stagnation Density
ρ0 = pc / (r * tc)
print(f"Stagnation Density  :{ρ0:.2f} kg/m^3")

# Throart Velocity (where mach = 1)
vt = np.sqrt( (2*y*r*tc) / (y+1) )
print(f"Throart Velocity    :{vt:.2f} m/s")

# Throat Density
ρt = ρ0 * (2/(y+1))**(1/(y-1))
print(f"Throat density      :{ρt:.2f} kg/m^3")

#Exit Pressure
ep = pc * (1+((y-1)/2)*(me**2))**(-(y/(y-1)))
print(f"Exit Pressure       :{ep:.2f} pa")

# Exit Tempreture
et = tc * (1 + (((y-1)/2) * (me**2)))**-1
print(f"Exit Tempreture     :{et:.2f} K")

# Exit Vlecity 
v_e = np.sqrt(y * r * et) * me
print(f"EXit velocity       :{v_e:.2f} m/s")

#Exit Mass flow
#m0 = ρt * vt * at 
m0 = ((pc*at)/np.sqrt(tc)) * np.sqrt((y/r) * (2/(y+1))**((y+1)/(2*(y-1))))
print(f"Exit Mass flow rate :{m0} kg/s")

#FORCE
F = m0 * v_e + (ep - pa) * ae
print(f"Thrust Final        :{F:.2f} N")

isp = v_e / g
print(f"specific impluse    :{isp} S")
