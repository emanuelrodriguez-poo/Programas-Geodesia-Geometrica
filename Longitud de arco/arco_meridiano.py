import numpy as np
import matplotlib.pyplot as plt


# ENTRADA DE DATOS

a = float(input("Ingrese el semieje mayor a (m): "))
f = float(input("Ingrese el achatamiento f: "))

lat1 = float(input("Ingrese latitud φ1 (grados): "))
lat2 = float(input("Ingrese latitud φ2 (grados): "))

lam1 = float(input("Ingrese longitud λ1 (grados): "))
lam2 = float(input("Ingrese longitud λ2 (grados): "))

# Conversión a radianes
phi1 = np.radians(lat1)
phi2 = np.radians(lat2)
lam = np.radians(lam1)  # meridiano


# PARÁMETROS

b = a * (1 - f)
e2 = 2*f - f**2


# COEFICIENTES

A = 1 + (3/4)*e2 + (45/64)*e2**2 + (175/256)*e2**3 + (11025/16384)*e2**4
B = (3/4)*e2 + (15/16)*e2**2 + (525/512)*e2**3 + (2205/2048)*e2**4
C = (15/64)*e2**2 + (105/256)*e2**3 + (2205/4096)*e2**4
D = (35/512)*e2**3 + (315/2048)*e2**4
E = (315/16384)*e2**4


# LONGITUD ARCO MERIDIANO

s = a * (1 - e2) * (
    A * (phi2 - phi1)
    - (B/2) * (np.sin(2*phi2) - np.sin(2*phi1))
    + (C/4) * (np.sin(4*phi2) - np.sin(4*phi1))
    - (D/6) * (np.sin(6*phi2) - np.sin(6*phi1))
    + (E/8) * (np.sin(8*phi2) - np.sin(8*phi1))
)


# CONSOLA


print("   DATOS DE ENTRADA")
print(f"a = {a}")
print(f"f = {f}")
print(f"Latitud A = {lat1}")
print(f"Latitud B = {lat2}")
print(f"Longitud A = {lam1}")
print(f"Longitud B = {lam2}")

print("       RESULTADOS")
print(f"s = {s:.3f} m")


# GRÁFICO 3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Fondo
fig.patch.set_facecolor('#0b1a2a')
ax.set_facecolor('#0b1a2a')

# Elipsoide
u = np.linspace(0, 2*np.pi, 60)
v = np.linspace(-np.pi/2, np.pi/2, 60)

x = a * np.outer(np.cos(v), np.cos(u))
y = a * np.outer(np.cos(v), np.sin(u))
z = b * np.outer(np.sin(v), np.ones_like(u))

ax.plot_surface(x, y, z, alpha=0.15)


# PARALELOS

paralelos = []
for phi in np.linspace(-np.pi/2, np.pi/2, 10):
    xp = a * np.cos(phi) * np.cos(u)
    yp = a * np.cos(phi) * np.sin(u)
    zp = b * np.sin(phi) * np.ones_like(u)
    linea, = ax.plot(xp, yp, zp, linewidth=0.7)
    paralelos.append(linea)


# MERIDIANOS

meridianos = []
for lam_m in np.linspace(0, 2*np.pi, 12):
    xm = a * np.cos(v) * np.cos(lam_m)
    ym = a * np.cos(v) * np.sin(lam_m)
    zm = b * np.sin(v)
    linea, = ax.plot(xm, ym, zm, linewidth=0.7)
    meridianos.append(linea)


# ARCO MERIDIANO

phi_curve = np.linspace(phi1, phi2, 200)

x_curve = a * np.cos(phi_curve) * np.cos(lam)
y_curve = a * np.cos(phi_curve) * np.sin(lam)
z_curve = b * np.sin(phi_curve)

arco, = ax.plot(x_curve, y_curve, z_curve, linewidth=3)


# PUNTOS

xA = a * np.cos(phi1) * np.cos(lam)
yA = a * np.cos(phi1) * np.sin(lam)
zA = b * np.sin(phi1)

xB = a * np.cos(phi2) * np.cos(lam)
yB = a * np.cos(phi2) * np.sin(lam)
zB = b * np.sin(phi2)

ax.scatter(xA, yA, zA)
ax.scatter(xB, yB, zB)

ax.text(xA, yA, zA, " A", color='white')
ax.text(xB, yB, zB, " B", color='white')


# LEYENDA (CONVENCIONES)

legend = ax.legend(
    [meridianos[0], paralelos[0], arco],
    ['Meridianos', 'Paralelos', 'Arco meridiano'],
    loc='upper left',
    facecolor='#0b1a2a',
    edgecolor='white'
)

for t in legend.get_texts():
    t.set_color('white')


# CUADRO DE DATOS

texto = (
    "DATOS DE ENTRADA\n"
    f"a = {a}\n"
    f"f = {f}\n"
    f"φ1 = {lat1}°\n"
    f"φ2 = {lat2}°\n"
    f"λ1 = {lam1}°\n"
    f"λ2 = {lam2}°\n\n"
    "RESULTADO\n"
    f"s = {s:.3f} m"
)

ax.text2D(
    1.05, 0.5, texto,
    transform=ax.transAxes,
    color='white',
    bbox=dict(facecolor='#0b1a2a', edgecolor='white')
)


# ESTILO

ax.set_title("ARCO MERIDIANO EN EL ELIPSOIDE", color='#66ccff')

ax.set_xlabel("X", color='white')
ax.set_ylabel("Y", color='white')
ax.set_zlabel("Z", color='white')

ax.tick_params(colors='white')

plt.show()