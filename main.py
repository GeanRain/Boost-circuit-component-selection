# ============  setting  ============
v_i = 25.9  # Input voltage (V)
v_o = 48  # Output voltage (V)
v_d = 0.85  # Diode voltage drop (V)
I_o = 10  # Output current (A)
f = 150000  # Frequency (Hz)
v_i_del = 0.5  # Input ripple voltage (V)
v_o_del = 0.5  # Output ripple voltage (V)
L_list = [1, 1.5, 2.2, 3.3, 4.7, 5.6, 6.8, 10, 12, 15, 22, 33, 47, 56, 68, 100, 150, 180, 220, 330, 470, 560, 680, 1000] # Inductance value list in uH

# ============  calculate  ============
L_min = (v_i/(0.4*f*I_o)*(1-v_i/(v_o+v_d))*v_i/(v_o+v_d))*(10**6) * 0.9
L_max = (v_i/(0.2*f*I_o)*(1-v_i/(v_o+v_d))*v_i/(v_o+v_d))*(10**6) * 1.1

L_select = [x for x in L_list if L_min <= x <= L_max]
resp = {}
for l in L_select:
    l = l/(10**6)
    resp[l*(10**6)]={
        "i_max": (v_o+v_d)/v_i*I_o+v_i/(2*f*l)*(1-v_i/(v_o+v_d)),
        "c_i_mlcc": v_i/(8*(f**2)*l*v_i_del)*(1-v_i/(v_o+v_d))*(10**6),
        "c_i_esr": (v_i_del*f*l)/v_i*(v_o+v_d)/(v_o+v_d-v_i)*(10**3),
        "c_o_mlcc": I_o/(f*v_o_del)*(1-v_i/(v_o+v_d))*(10**6),
        "c_o_esr": v_o_del/((v_o+v_d)/v_i*I_o+v_i/(2*f*l)*(1-v_i/(v_o+v_d)))*(10**3)
    }

# ============  result  ============
print(f"L in {L_min:.2f}~{L_max:.2f} uH (add 10%)")
print("select value: {}".format(list(resp.keys())))
print(f"L value(uH)\tI Max(A)\tCap in mlcc Min(uF)\tCap in esr Max(mR@{f/1000.0}kHz)\tCap out mlcc Min(uF)\tCap out esr Max(mR@{f/1000.0}kHz)")
for l in resp.keys():
    print(f"{l}\t\t{resp[l]['i_max']:.2f}\t\t{resp[l]['c_i_mlcc']:.2f}\t\t\t{resp[l]['c_i_esr']:.2f}\t\t\t\t{resp[l]['c_o_mlcc']:.2f}\t\t\t{resp[l]['c_o_esr']:.2f}")

