import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# =========================================================
# CONSTANTES WGS84
# =========================================================
a = 6378137.0
f = 1 / 298.257223563
b = a * (1 - f)
e2 = 2 * f - f**2
e = math.sqrt(e2)

# =========================================================
# FUNCION
# =========================================================
def rectangulares_a_geodesicas(X, Y, Z):
    p = math.sqrt(X**2 + Y**2)
    lambda_rad = math.atan2(Y, X)

    phi_rad = math.atan2(Z, p * (1 - e2))

    for _ in range(10):
        N = a / math.sqrt(1 - e2 * math.sin(phi_rad)**2)
        h = p / math.cos(phi_rad) - N
        phi_rad = math.atan2(Z, p * (1 - e2 * N / (N + h)))

    N = a / math.sqrt(1 - e2 * math.sin(phi_rad)**2)
    h = p / math.cos(phi_rad) - N

    return phi_rad, lambda_rad, math.degrees(phi_rad), math.degrees(lambda_rad), h, N, p

# =========================================================
# LOOP
# =========================================================
while True:
    try:
        print("\nPROBLEMA INVERSO")
        Xp = float(input("Ingrese X (-999 para salir): "))
        if Xp == -999:
            break

        Yp = float(input("Ingrese Y: "))
        Zp = float(input("Ingrese Z: "))

        phi_rad, lambda_rad, phi_deg, lambda_deg, h, N, p = rectangulares_a_geodesicas(Xp, Yp, Zp)

        # =====================================================
        # MALLA
        # =====================================================
        u = np.linspace(0, 2*np.pi, 120)
        v = np.linspace(-np.pi/2, np.pi/2, 80)
        U, V = np.meshgrid(u, v)

        X = a*np.cos(V)*np.cos(U)
        Y = a*np.cos(V)*np.sin(U)
        Z = b*np.sin(V)

        fig = plt.figure(figsize=(16,9), facecolor="#0a1a2f")

        # =====================================================
        # ELIPSOIDE
        # =====================================================
        ax = fig.add_axes([0.03, 0.1, 0.55, 0.8], projection='3d')
        ax.set_facecolor("#0a1a2f")

        ax.plot_surface(X, Y, Z, alpha=0.3)

        # MERIDIANO
        lon = lambda_rad
        vv = np.linspace(-np.pi/2, np.pi/2, 300)

        x_mer = a * np.cos(vv) * np.cos(lon)
        y_mer = a * np.cos(vv) * np.sin(lon)
        z_mer = b * np.sin(vv)

        ax.plot(x_mer, y_mer, z_mer, color="blue", linewidth=2)

        # PARALELO
        lat = phi_rad
        uu = np.linspace(0, 2*np.pi, 300)

        x_par = a * np.cos(lat) * np.cos(uu)
        y_par = a * np.cos(lat) * np.sin(uu)
        z_par = np.full_like(uu, b * np.sin(lat))

        ax.plot(x_par, y_par, z_par, color="orange", linewidth=2)

        # PUNTO
        ax.scatter(Xp, Yp, Zp, color="red", s=100)

        # CONFIG
        lim = 8_000_000
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_zlim(-lim, lim)

        ax.set_xlabel("X", color="white")
        ax.set_ylabel("Y", color="white")
        ax.set_zlabel("Z", color="white")
        ax.tick_params(colors='white')

        # =====================================================
        # CONVENCIONES
        # =====================================================
        conv = fig.add_axes([0.03, 0.02, 0.25, 0.1])
        conv.set_facecolor("#0a1a2f")
        conv.axis("off")

        conv.legend(
            handles=[
                Line2D([0],[0],color="blue", lw=2, label="Meridiano"),
                Line2D([0],[0],color="orange", lw=2, label="Paralelo"),
                Line2D([0],[0],marker='o',color='w',markerfacecolor='red',label="Punto")
            ],
            loc="center",
            frameon=False,
            fontsize=9,
            labelcolor="white"
        )

        # =====================================================
        # PANEL DERECHO (ORDENADO PERFECTO)
        # =====================================================
        panel = fig.add_axes([0.65, 0.1, 0.32, 0.8])
        panel.set_facecolor("#0a1a2f")
        panel.axis("off")

        azul = "#4cc9f0"
        blanco = "white"

        y = 0.95

        # TITULO
        panel.text(0.05, y,
            "Problema inverso\n(coordenadas rectangulares)",
            color=azul, fontsize=16, weight='bold', va='top')

        y -= 0.10

        # =========================
        # DATOS
        # =========================
        panel.text(0.05, y, "Datos", color=azul, fontsize=13, weight='bold')
        y -= 0.05

        panel.text(0.05, y, "Datos de entrada", color=azul, fontsize=11)
        y -= 0.05

        panel.text(0.05, y, f"X = {Xp:.3f}", color=blanco); y -= 0.04
        panel.text(0.05, y, f"Y = {Yp:.3f}", color=blanco); y -= 0.04
        panel.text(0.05, y, f"Z = {Zp:.3f}", color=blanco)

        y -= 0.07

        # =========================
        # RESULTADOS
        # =========================
        panel.text(0.05, y, "Resultados", color=azul, fontsize=13, weight='bold')
        y -= 0.05

        panel.text(0.05, y, f"φ: {phi_deg:.6f}°", color=blanco); y -= 0.04
        panel.text(0.05, y, f"λ: {lambda_deg:.6f}°", color=blanco); y -= 0.04
        panel.text(0.05, y, f"h: {h:.3f} m", color=blanco); y -= 0.05

        panel.text(0.05, y, f"φ: {phi_rad:.8f} rad", color=blanco); y -= 0.04
        panel.text(0.05, y, f"λ: {lambda_rad:.8f} rad", color=blanco); y -= 0.04
        panel.text(0.05, y, f"N: {N:.3f} m", color=blanco); y -= 0.04
        panel.text(0.05, y, f"p: {p:.3f} m", color=blanco)

        y -= 0.07

        # =========================
        # PARAMETROS
        # =========================
        panel.text(0.05, y, "Parámetros", color=azul, fontsize=13, weight='bold')
        y -= 0.05

        panel.text(0.05, y, f"a: {a:.3f} m", color=blanco); y -= 0.04
        panel.text(0.05, y, f"b: {b:.3f} m", color=blanco); y -= 0.04
        panel.text(0.05, y, f"f: 1 / 298.257223563", color=blanco); y -= 0.04
        panel.text(0.05, y, f"e²: {e2:.10f}", color=blanco)

        plt.show()

    except Exception as e:
        print("Error:", e)