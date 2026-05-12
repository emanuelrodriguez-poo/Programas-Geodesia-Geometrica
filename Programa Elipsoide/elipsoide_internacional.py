import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


# CONSTANTES ELIPSOIDE INTERNACIONAL

a = 6378388.0
f = 1 / 297
b = a * (1 - f)
e2 = 2 * f - f**2
e = math.sqrt(e2)


# FUNCION PRINCIPAL

def geodesicas_a_rectangulares(phi_deg, lambda_deg, h):
    phi = math.radians(phi_deg)
    lamb = math.radians(lambda_deg)

    N = a / math.sqrt(1 - e2 * math.sin(phi)**2)

    X = (N + h) * math.cos(phi) * math.cos(lamb)
    Y = (N + h) * math.cos(phi) * math.sin(lamb)
    Z = (N * (1 - e2) + h) * math.sin(phi)

    return phi, lamb, N, X, Y, Z


def plot_visible_curve(ax, x, y, z, color):
    elev = math.radians(20)
    azim = math.radians(-55)

    view = np.array([
        math.cos(elev) * math.cos(azim),
        math.cos(elev) * math.sin(azim),
        math.sin(elev)
    ])

    normals = np.vstack((x / a**2, y / a**2, z / b**2)).T
    normals = normals / np.linalg.norm(normals, axis=1)[:, None]

    visible = normals @ view > 0

    start = None
    for i in range(len(x)):
        if visible[i] and start is None:
            start = i
        elif (not visible[i] or i == len(x) - 1) and start is not None:
            end = i if not visible[i] else i + 1
            ax.plot(x[start:end], y[start:end], z[start:end], color=color)
            start = None



# LOOP

while True:
    try:
        print("\nELIPSOIDE (Sistema Internacional)")
        print("-----------------------------------")

        phi_deg = float(input("Ingrese latitud φ: "))
        if phi_deg == -999:
            break

        lambda_deg = float(input("Ingrese longitud λ: "))
        h = float(input("Ingrese altura h (m): "))

        phi_rad, lambda_rad, N, Xp, Yp, Zp = geodesicas_a_rectangulares(
            phi_deg, lambda_deg, h
        )

        # MALLA
        u = np.linspace(0, 2 * np.pi, 150)
        v = np.linspace(-np.pi / 2, np.pi / 2, 100)
        U, V = np.meshgrid(u, v)

        X = a * np.cos(V) * np.cos(U)
        Y = a * np.cos(V) * np.sin(U)
        Z = b * np.sin(V)

        # FIGURA
        fig = plt.figure(figsize=(16, 9), facecolor="#0b1e3a")

        # =====================================================
        # ELIPSOIDE (IZQUIERDA)
        # =====================================================
        ax = fig.add_axes([0.03, 0.08, 0.60, 0.85], projection="3d")
        ax.set_facecolor("#0b1e3a")

        ax.plot_surface(X, Y, Z, alpha=0.6)

        # Meridianos
        for lon_deg in range(0, 360, 20):
            lon = math.radians(lon_deg)
            vv = np.linspace(-np.pi/2, np.pi/2, 200)
            xm = a * np.cos(vv) * math.cos(lon)
            ym = a * np.cos(vv) * math.sin(lon)
            zm = b * np.sin(vv)
            plot_visible_curve(ax, xm, ym, zm, "#4da6ff")

        # Paralelos
        for lat_deg in range(-75, 90, 15):
            lat = math.radians(lat_deg)
            uu = np.linspace(0, 2*np.pi, 200)
            xp = a * math.cos(lat) * np.cos(uu)
            yp = a * math.cos(lat) * np.sin(uu)
            zp = np.full_like(uu, b * math.sin(lat))
            plot_visible_curve(ax, xp, yp, zp, "#66ff99")

        # Punto P
        ax.scatter(Xp, Yp, Zp, color="red", s=80)

        # CONVENCIONES
        legend_elements = [
            Line2D([0], [0], color="#4da6ff", lw=2, label="Meridianos"),
            Line2D([0], [0], color="#66ff99", lw=2, label="Paralelos"),
            Line2D([0], [0], marker='o', color='w',
                   markerfacecolor='red', markersize=8,
                   label="Punto P (X,Y,Z)")
        ]

        ax.legend(handles=legend_elements,
                  loc="upper left",
                  fontsize=9,
                  facecolor="#0b1e3a",
                  edgecolor="white",
                  labelcolor="white")

        # Ejes
        lim = 8_000_000
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_zlim(-lim, lim)

        ax.set_xlabel("X (m)", color="white")
        ax.set_ylabel("Y (m)", color="white")
        ax.set_zlabel("Z (m)", color="white")
        ax.tick_params(colors='white')

        
        # PANEL DERECHO (AJUSTE FINAL PERFECTO)
       
        panel = fig.add_axes([0.67, 0.08, 0.30, 0.85])
        panel.set_facecolor("#0b1e3a")
        panel.set_xticks([])
        panel.set_yticks([])

        for spine in panel.spines.values():
            spine.set_visible(False)

        # TITULO
        panel.text(0.05, 0.95,
                   "ELIPSOIDE\n(SISTEMA INTERNACIONAL)",
                   color="#66ccff",
                   fontsize=16,
                   fontweight="bold",
                   va="top")

        # DATOS DE ENTRADA
        panel.text(0.05, 0.80, "DATOS DE ENTRADA",
                   color="#66ccff", fontsize=12, fontweight="bold")

        panel.text(0.05, 0.75,
                   f"φ = {phi_deg:.6f}°\n"
                   f"φ = {phi_rad:.6f} rad\n\n"
                   f"λ = {lambda_deg:.6f}°\n"
                   f"λ = {lambda_rad:.6f} rad\n\n"
                   f"h = {h:.2f} m",
                   color="white",
                   fontsize=11,
                   va="top")

        # RESULTADOS
        panel.text(0.05, 0.56, "RESULTADOS",
                   color="#66ccff", fontsize=12, fontweight="bold")

        panel.text(0.05, 0.48,
                   f"N = {N:.3f} m\n\n"
                   f"X = {Xp:.3f} m\n"
                   f"Y = {Yp:.3f} m\n"
                   f"Z = {Zp:.3f} m",
                   color="white",
                   fontsize=11,
                   va="top")

        # PARÁMETROS
        panel.text(0.05, 0.24, "PARÁMETROS",
                   color="#66ccff", fontsize=12, fontweight="bold")

        panel.text(0.05, 0.16,
                   f"a = {a:.3f} m\n"
                   f"f = 1 / 297\n"
                   f"b = {b:.3f} m\n"
                   f"e² = {e2:.10f}\n"
                   f"e = {e:.10f}",
                   color="white",
                   fontsize=11,
                   va="top")

        plt.show()

    except ValueError:
        print("Error: ingrese valores válidos")