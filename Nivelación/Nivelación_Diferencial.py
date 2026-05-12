import math
import os
import webbrowser
import folium
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# =========================================================
# FUNCIONES
# =========================================================

def promedio(lista):
    return sum(lista) / len(lista)


def calcular_sube_baja(cota_anterior, cota_actual):

    diferencia = cota_actual - cota_anterior

    if diferencia > 0:
        return diferencia, 0.0

    elif diferencia < 0:
        return 0.0, abs(diferencia)

    else:
        return 0.0, 0.0


def gms_a_decimal(grados, minutos, segundos):

    signo = -1 if grados < 0 else 1

    return signo * (abs(grados) + minutos / 60 + segundos / 3600)


def leer_coordenada(nombre):

    print(f"\nCoordenada {nombre}")

    grados = float(input("Grados: "))
    minutos = float(input("Minutos: "))
    segundos = float(input("Segundos: "))

    return gms_a_decimal(grados, minutos, segundos)


# =========================================================
# MAPA SATELITAL
# =========================================================

def mostrar_mapa_satelital(puntos):

    if len(puntos) == 0:
        return

    lat_centro = sum(p["lat"] for p in puntos) / len(puntos)
    lon_centro = sum(p["lon"] for p in puntos) / len(puntos)

    mapa = folium.Map(
        location=[lat_centro, lon_centro],
        zoom_start=18,
        control_scale=True,
        prefer_canvas=True
    )

    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/'
              'World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri World Imagery',
        name='Satélite',
        overlay=False,
        control=True
    ).add_to(mapa)

    folium.TileLayer(
        'OpenStreetMap',
        name='Mapa'
    ).add_to(mapa)

    ruta = []

    for p in puntos:

        coord = [p["lat"], p["lon"]]

        ruta.append(coord)

        popup = f"""
        <b>{p['nombre']}</b><br>
        Cota = {p['cota']:.4f} m<br>
        Lat = {p['lat']:.8f}<br>
        Lon = {p['lon']:.8f}
        """

        folium.Marker(
            location=coord,
            popup=popup,
            tooltip=p["nombre"],
            icon=folium.Icon(
                color="red",
                icon="info-sign"
            )
        ).add_to(mapa)

    folium.PolyLine(
        locations=ruta,
        color="yellow",
        weight=5,
        opacity=0.9
    ).add_to(mapa)

    mapa.fit_bounds(ruta)

    folium.LayerControl().add_to(mapa)

    archivo = "mapa_nivelacion_satelital.html"

    ruta_archivo = os.path.abspath(archivo)

    mapa.save(ruta_archivo)

    print("\nMapa satelital generado correctamente.")

    webbrowser.open("file://" + ruta_archivo)


# =========================================================
# PROGRAMA PRINCIPAL
# =========================================================

while True:

    try:

        print("\nPROGRAMA 5 - NIVELACIÓN GEODÉSICA")
        print("---------------------------------")
        print("Cálculo por altura instrumental, subes y bajas, perfil y mapa.")
        print("Para salir escriba -999 como cota inicial.\n")

        cota_inicial = float(input("Ingrese cota conocida inicial: "))

        if cota_inicial == -999:

            print("Programa finalizado.")
            break

        nombre_inicial = input("Nombre del punto inicial: ")

        print("\nCoordenadas geodésicas del punto inicial")

        lat_ini = leer_coordenada("latitud")
        lon_ini = leer_coordenada("longitud")

        h_ini = float(input("Altura elipsoidal h: "))

        numero_estaciones = int(
            input("\nNúmero de estaciones / armados: ")
        )

        registros = []

        puntos_mapa = []

        puntos_perfil = []

        cota_referencia = cota_inicial

        cota_anterior = cota_inicial

        distancia_acumulada = 0.0

        # =====================================================
        # PUNTO INICIAL
        # =====================================================

        puntos_mapa.append({

            "nombre": nombre_inicial,

            "lat": lat_ini,

            "lon": lon_ini,

            "h": h_ini,

            "cota": cota_inicial

        })

        puntos_perfil.append({

            "nombre": nombre_inicial,

            "distancia": distancia_acumulada,

            "cota": cota_inicial,

            "lat": lat_ini,

            "lon": lon_ini

        })

        # =====================================================
        # ESTACIONES
        # =====================================================

        for i in range(numero_estaciones):

            print(f"\n========== ESTACIÓN / ARMADO {i + 1} ==========")

            estacion = input("Estación (Δ): ")

            punto_visado = input("Punto visado (O): ")

            # =================================================
            # V+
            # =================================================

            n_vmas = int(input("Cantidad de lecturas V+: "))

            lecturas_vmas = []

            for k in range(n_vmas):

                valor = float(input(f"V+ lectura {k + 1}: "))

                lecturas_vmas.append(valor)

            v_mas = promedio(lecturas_vmas)

            # =================================================
            # V-
            # =================================================

            n_vmenos = int(input("Cantidad de lecturas V-: "))

            lecturas_vmenos = []

            for k in range(n_vmenos):

                valor = float(input(f"V- lectura {k + 1}: "))

                lecturas_vmenos.append(valor)

            v_menos = promedio(lecturas_vmenos)

            # =================================================
            # DISTANCIAS
            # =================================================

            n_dist = int(input("Cantidad de distancias medidas: "))

            distancias = []

            for k in range(n_dist):

                valor = float(input(f"Distancia {k + 1}: "))

                distancias.append(valor)

            distancia_prom = promedio(distancias)

            distancia_acumulada += distancia_prom

            # =================================================
            # COORDENADAS
            # =================================================

            print(f"\nCoordenadas geodésicas de {punto_visado}")

            lat = leer_coordenada("latitud")

            lon = leer_coordenada("longitud")

            h = float(input("Altura elipsoidal h: "))

            # =================================================
            # CALCULOS
            # =================================================

            cota_hi = cota_referencia + v_mas

            cota_punto = cota_hi - v_menos

            sube, baja = calcular_sube_baja(
                cota_anterior,
                cota_punto
            )

            registros.append({

                "estacion": estacion,

                "punto": punto_visado,

                "v_mas": v_mas,

                "v_menos": v_menos,

                "distancia": distancia_prom,

                "dist_acum": distancia_acumulada,

                "lat": lat,

                "lon": lon,

                "h": h,

                "cota_hi": cota_hi,

                "cota": cota_punto,

                "sube": sube,

                "baja": baja

            })

            puntos_mapa.append({

                "nombre": punto_visado,

                "lat": lat,

                "lon": lon,

                "h": h,

                "cota": cota_punto

            })

            puntos_perfil.append({

                "nombre": punto_visado,

                "distancia": distancia_acumulada,

                "cota": cota_punto,

                "lat": lat,

                "lon": lon

            })

            cota_anterior = cota_punto

            cota_referencia = cota_punto

        # =====================================================
        # RESULTADOS
        # =====================================================

        cota_final = registros[-1]["cota"]

        suma_sube = sum(r["sube"] for r in registros)

        suma_baja = sum(r["baja"] for r in registros)

        diferencia_total = cota_final - cota_inicial

        # =====================================================
        # MAPA SATELITAL
        # =====================================================

        mostrar_mapa_satelital(puntos_mapa)

        # =====================================================
        # DATOS GRAFICAS
        # =====================================================

        nombres = [p["nombre"] for p in puntos_perfil]

        distancias_plot = [p["distancia"] for p in puntos_perfil]

        cotas_plot = [p["cota"] for p in puntos_perfil]

        estes = distancias_plot

        nortes = [
            8 * math.sin(i * 0.75)
            for i in range(len(distancias_plot))
        ]

        # =====================================================
        # FIGURA GENERAL
        # =====================================================

        fig = plt.figure(
            figsize=(16, 9),
            facecolor="#061726"
        )

        # =====================================================
        # TITULO GENERAL
        # =====================================================

        fig.suptitle(
            "NIVELACIÓN GEODÉSICA",
            fontsize=30,
            fontweight="bold",
            color="#59d8ff",
            y=0.965
        )

        # =====================================================
        # PANEL DERECHO
        # =====================================================

        panel = fig.add_axes([0.76, 0.08, 0.22, 0.84])

        panel.set_facecolor("#081f33")

        panel.set_xticks([])

        panel.set_yticks([])

        panel.set_xlim(0, 1)

        panel.set_ylim(0, 1)

        for spine in panel.spines.values():

            spine.set_edgecolor("#1f4e79")

            spine.set_linewidth(2)

        # =====================================================
        # TITULO PANEL
        # =====================================================

        panel.text(
            0.05,
            0.93,
            "NIVELACIÓN GEODÉSICA",
            color="#59d8ff",
            fontsize=16,
            fontweight="bold"
        )

        # =====================================================
        # DATOS GENERALES
        # =====================================================

        panel.text(
            0.05,
            0.82,
            "DATOS GENERALES:",
            color="#59d8ff",
            fontsize=14,
            fontweight="bold"
        )

        panel.text(
            0.05,
            0.73,
            f"Punto inicial     : {nombre_inicial}",
            color="white",
            fontsize=11,
            family="monospace"
        )

        panel.text(
            0.05,
            0.66,
            f"Cota inicial      : {cota_inicial:.4f} m",
            color="white",
            fontsize=11,
            family="monospace"
        )

        panel.text(
            0.05,
            0.59,
            f"Cota final        : {cota_final:.4f} m",
            color="white",
            fontsize=11,
            family="monospace"
        )

        panel.text(
            0.05,
            0.52,
            f"Estaciones        : {numero_estaciones}",
            color="white",
            fontsize=11,
            family="monospace"
        )

        # =====================================================
        # LINEA DIVISORIA
        # =====================================================

        panel.plot(
            [0.05, 0.95],
            [0.46, 0.46],
            color="#59d8ff",
            linewidth=1.5
        )

        # =====================================================
        # RESULTADOS
        # =====================================================

        panel.text(
            0.05,
            0.40,
            "RESULTADOS:",
            color="#59d8ff",
            fontsize=14,
            fontweight="bold"
        )

        panel.text(
            0.05,
            0.31,
            f"Σ Sube           : {suma_sube:.4f} m",
            color="white",
            fontsize=11,
            family="monospace"
        )

        panel.text(
            0.05,
            0.24,
            f"Σ Baja           : {suma_baja:.4f} m",
            color="white",
            fontsize=11,
            family="monospace"
        )

        panel.text(
            0.05,
            0.17,
            f"Δ total          : {diferencia_total:.4f} m",
            color="white",
            fontsize=11,
            family="monospace"
        )

        panel.text(
            0.05,
            0.10,
            f"Cota máxima      : {max(cotas_plot):.4f} m",
            color="white",
            fontsize=11,
            family="monospace"
        )

        panel.text(
            0.05,
            0.03,
            f"Cota mínima      : {min(cotas_plot):.4f} m",
            color="white",
            fontsize=11,
            family="monospace"
        )

        # =====================================================
        # PERFIL
        # =====================================================

        ax_perfil = fig.add_axes([0.05, 0.67, 0.66, 0.22])

        ax_perfil.set_facecolor("#edf4fb")

        ax_perfil.plot(
            distancias_plot,
            cotas_plot,
            color="#0033cc",
            linewidth=2.5,
            marker="o",
            markerfacecolor="#ff2b2b",
            markeredgecolor="black"
        )

        for i, nombre in enumerate(nombres):

            ax_perfil.text(
                distancias_plot[i],
                cotas_plot[i],
                f" {nombre}",
                fontsize=8.5,
                color="black"
            )

        ax_perfil.set_title(
            "Perfil de Nivelación",
            fontsize=20,
            fontweight="bold",
            color="white"
        )

        ax_perfil.set_xlabel(
            "Distancia acumulada (m)",
            fontsize=15,
            color="white"
        )

        ax_perfil.set_ylabel(
            "Cota (m)",
            fontsize=15,
            color="white"
        )

        ax_perfil.tick_params(colors="white")

        ax_perfil.grid(True, linestyle="--", alpha=0.5)

        # =====================================================
        # MAPA 3D
        # =====================================================

        ax_mapa = fig.add_axes(
            [0.05, 0.18, 0.50, 0.38],
            projection="3d"
        )

        ax_mapa.set_facecolor("#edf4fb")

        ax_mapa.plot(
            estes,
            nortes,
            cotas_plot,
            color="#3aa657",
            linewidth=2.5
        )

        ax_mapa.scatter(
            estes,
            nortes,
            cotas_plot,
            color="#ff2b2b",
            edgecolor="black",
            s=65
        )

        for i, nombre in enumerate(nombres):

            ax_mapa.text(
                estes[i],
                nortes[i],
                cotas_plot[i],
                f" {nombre}",
                fontsize=8.5
            )

        ax_mapa.set_title(
            "Mapa 3D",
            fontsize=20,
            fontweight="bold",
            color="white"
        )

        ax_mapa.set_xlabel(
            "Distancia acumulada (m)",
            color="white",
            fontsize=13
        )

        ax_mapa.set_ylabel(
            "Norte gráfico",
            color="white",
            fontsize=13
        )

        ax_mapa.set_zlabel(
            "Cota (m)",
            color="white",
            fontsize=13
        )

        ax_mapa.tick_params(colors="white")

        ax_mapa.view_init(elev=30, azim=-55)

        ax_mapa.grid(True)

        # =====================================================
        # CONVENCIONES
        # =====================================================

        conv_panel = fig.add_axes([0.57, 0.24, 0.14, 0.17])

        conv_panel.set_facecolor("#0b2238")

        conv_panel.set_xticks([])

        conv_panel.set_yticks([])

        for spine in conv_panel.spines.values():

            spine.set_edgecolor("#59d8ff")

            spine.set_linewidth(1.5)

        conv_panel.text(
            0.10,
            0.88,
            "CONVENCIONES",
            fontsize=12,
            color="#59d8ff",
            fontweight="bold",
            va="top"
        )

        conv_panel.legend(
            handles=[

                Line2D(
                    [0], [0],
                    color="#0033cc",
                    lw=2.5,
                    label="Perfil"
                ),

                Line2D(
                    [0], [0],
                    color="#3aa657",
                    lw=2.5,
                    label="Mapa 3D"
                ),

                Line2D(
                    [0], [0],
                    marker="o",
                    color="w",
                    markerfacecolor="#ff2b2b",
                    markeredgecolor="black",
                    markersize=7,
                    label="Puntos"
                )

            ],

            loc="upper left",

            bbox_to_anchor=(0.02, 0.72),

            fontsize=10,

            frameon=False,

            labelcolor="white"
        )

        # =====================================================
        # FOOTER
        # =====================================================

        footer = fig.add_axes([0.02, 0.01, 0.96, 0.04])

        footer.set_facecolor("#08233a")

        footer.set_xticks([])

        footer.set_yticks([])

        for spine in footer.spines.values():

            spine.set_edgecolor("#1f4e79")

        footer.text(
            0.5,
            0.5,
            "Nivelación Geodésica | Perfil Longitudinal | Mapa 3D",
            ha="center",
            va="center",
            fontsize=10,
            color="#59d8ff",
            fontweight="bold"
        )

        plt.show()

    except ValueError:

        print("Error: ingrese un valor numérico válido.")

    except Exception as error:

        print("Error:", error)