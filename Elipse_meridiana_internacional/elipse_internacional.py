import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# =========================================================
# ELIPSOIDE INTERNACIONAL
# =========================================================
a = 6378388.0
f = 1 / 297
b = a * (1 - f)
e2 = 2 * f - f**2
e = math.sqrt(e2)

# =========================================================
def elipse_meridiana(phi_deg):
    phi = math.radians(phi_deg)
    N = a / math.sqrt(1 - e2 * math.sin(phi)**2)

    x = N * math.cos(phi)
    y = 0.0
    z = N * (1 - e2) * math.sin(phi)

    return phi, N, x, y, z

# =========================================================
def plot_visible_curve(ax, x, y, z, color):
    elev = math.radians(20)
    azim = math.radians(-55)

    view = np.array([
        math.cos(elev)*math.cos(azim),
        math.cos(elev)*math.sin(azim),
        math.sin(elev)
    ])

    normals = np.vstack((x/a**2, y/a**2, z/b**2)).T
    normals = normals / np.linalg.norm(normals, axis=1)[:, None]

    visible = normals @ view > 0

    start = None
    for i in range(len(x)):
        if visible[i] and start is None:
            start = i
        elif (not visible[i] or i == len(x)-1) and start is not None:
            end = i if not visible[i] else i+1
            ax.plot(x[start:end], y[start:end], z[start:end], color=color)
            start = None

# =========================================================
while True:
    try:
        phi_deg = float(input("Ingrese latitud φ (-999 para salir): "))
        if phi_deg == -999:
            break

        phi_rad, N, x_p, y_p, z_p = elipse_meridiana(phi_deg)

        # MALLA
        u = np.linspace(0, 2*np.pi, 150)
        v = np.linspace(-np.pi/2, np.pi/2, 100)
        U, V = np.meshgrid(u, v)

        X = a*np.cos(V)*np.cos(U)
        Y = a*np.cos(V)*np.sin(U)
        Z = b*np.sin(V)

        fig = plt.figure(figsize=(16,9), facecolor="#0b1c3d")

        # =====================================================
        # PANEL IZQUIERDO (ORDENADO)
        # =====================================================
        panel = fig.add_axes([0.03,0.05,0.30,0.9])
        panel.set_facecolor("#102a54")
        panel.set_xticks([])
        panel.set_yticks([])

        # TITULO
        panel.text(0.05,0.95,"ELIPSE MERIDIANA\n(SISTEMA INTERNACIONAL)",
                   color="white", fontsize=18, fontweight="bold")

        # -----------------------------
        # DATO DE ENTRADA
        # -----------------------------
        panel.text(0.05,0.80,"DATO DE ENTRADA", color="#00e5ff", fontsize=14)

        panel.text(0.05,0.74,f"φ = {phi_deg:.6f}°", color="yellow", fontsize=13)
        panel.text(0.05,0.70,f"φ = {phi_rad:.6f} rad", color="white", fontsize=13)

        # -----------------------------
        # RESULTADOS (BIEN SEPARADO)
        # -----------------------------
        panel.text(0.05,0.60,"RESULTADOS", color="#00e5ff", fontsize=14)

        panel.text(0.05,0.54,f"N = {N:.3f} m", color="white", fontsize=12)
        panel.text(0.05,0.50,f"x = {x_p:.3f} m", color="white", fontsize=12)
        panel.text(0.05,0.46,f"y = {y_p:.3f} m", color="white", fontsize=12)
        panel.text(0.05,0.42,f"z = {z_p:.3f} m", color="white", fontsize=12)

        # -----------------------------
        # PARAMETROS (MAS ABAJO)
        # -----------------------------
        panel.text(0.05,0.30,"PARÁMETROS", color="#00e5ff", fontsize=14)

        panel.text(0.05,0.24,f"a = {a:.3f} m", color="white", fontsize=12)
        panel.text(0.05,0.20,f"f = 1/297", color="white", fontsize=12)
        panel.text(0.05,0.16,f"b = {b:.3f} m", color="white", fontsize=12)
        panel.text(0.05,0.12,f"e² = {e2:.10f}", color="white", fontsize=12)
        panel.text(0.05,0.08,f"e = {e:.10f}", color="white", fontsize=12)

        # =====================================================
        # GRAFICA DERECHA
        # =====================================================
        ax = fig.add_axes([0.38,0.1,0.55,0.8], projection='3d')
        ax.plot_surface(X,Y,Z, alpha=0.6)

        # MERIDIANOS
        for lon in range(0,360,20):
            vv = np.linspace(-np.pi/2,np.pi/2,200)
            xm = a*np.cos(vv)*math.cos(math.radians(lon))
            ym = a*np.cos(vv)*math.sin(math.radians(lon))
            zm = b*np.sin(vv)
            plot_visible_curve(ax,xm,ym,zm,"cyan")

        # PARALELOS
        for lat in range(-60,90,20):
            uu = np.linspace(0,2*np.pi,300)
            xp = a*np.cos(math.radians(lat))*np.cos(uu)
            yp = a*np.cos(math.radians(lat))*np.sin(uu)
            zp = np.full_like(uu,b*np.sin(math.radians(lat)))
            plot_visible_curve(ax,xp,yp,zp,"green")

        # ELIPSE
        phis = np.linspace(-90,90,400)
        x_m=[]; y_m=[]; z_m=[]
        for p in phis:
            _,_,x,y,z = elipse_meridiana(p)
            x_m.append(x); y_m.append(y); z_m.append(z)

        ax.plot(x_m,y_m,z_m,color="blue",linewidth=3)

        ax.scatter(x_p,y_p,z_p,color="red",s=80)

        # =====================================================
        # CONVENCIONES (AL LADO DERECHO)
        # =====================================================
        conv = fig.add_axes([0.82,0.15,0.15,0.2])
        conv.set_xticks([])
        conv.set_yticks([])

        conv.legend(handles=[
            Line2D([0],[0],color="blue",lw=3,label="Elipse"),
            Line2D([0],[0],marker='o',color='w',markerfacecolor='red',label="Punto P"),
            Line2D([0],[0],color="cyan",lw=2,label="Meridianos"),
            Line2D([0],[0],color="green",lw=2,label="Paralelos"),
        ])

        plt.show()

    except:
        print("Error")