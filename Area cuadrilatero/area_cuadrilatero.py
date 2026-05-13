import math
import os
import webbrowser
import numpy as np
import matplotlib.pyplot as plt
import folium


# FUNCIONES


def seleccionar_elipsoide():

    print("\nSELECCIÓN DE ELIPSOIDE")
    print("----------------------")
    print("0 = Salir")
    print("1 = Clarke 1866")
    print("2 = Internacional 1924")
    print("3 = GRS80")
    print("4 = WGS84")

    opcion = int(input("Seleccione opción: "))

    if opcion == 0:
        return None, None, None

    elipsoides = {

        1: {
            "nombre": "Clarke 1866",
            "a": 6378206.4,
            "f": 0.003390075304
        },

        2: {
            "nombre": "Internacional 1924",
            "a": 6378388.0,
            "f": 0.003367003387
        },

        3: {
            "nombre": "GRS80",
            "a": 6378137.0,
            "f": 0.003352810688
        },

        4: {
            "nombre": "WGS84",
            "a": 6378137.0,
            "f": 0.003352810672
        }
    }

    if opcion not in elipsoides:
        raise ValueError("Opción no válida.")

    elip = elipsoides[opcion]

    print("\nELIPSOIDE SELECCIONADO")
    print("----------------------")
    print(f"Nombre = {elip['nombre']}")
    print(f"a      = {elip['a']} m")
    print(f"f      = {elip['f']}")
    print(f"1/f    = {1/elip['f']}")

    return elip["nombre"], elip["a"], elip["f"]


def gms_a_grados(g, m, s, hemisferio):

    valor = abs(g) + m / 60 + s / 3600

    if hemisferio.upper() in ["S", "W"]:
        valor *= -1

    return valor


def leer_latitud(nombre):

    print(f"\nLATITUD {nombre}")

    g = float(input(f"Grados Lat{nombre}: "))
    m = float(input(f"Minutos Lat{nombre}: "))
    s = float(input(f"Segundos Lat{nombre}: "))
    h = input(f"Hemisferio Lat{nombre} (N/S): ").upper()

    if h not in ["N", "S"]:
        raise ValueError("El hemisferio debe ser N o S.")

    valor = gms_a_grados(g, m, s, h)

    texto = f"{int(g)}° {int(m)}' {s}\" {h}"

    return valor, texto


def leer_longitud(nombre):

    print(f"\nLONGITUD {nombre}")

    g = float(input(f"Grados Lon{nombre}: "))
    m = float(input(f"Minutos Lon{nombre}: "))
    s = float(input(f"Segundos Lon{nombre}: "))
    h = input(f"Hemisferio Lon{nombre} (E/W): ").upper()

    if h not in ["E", "W"]:
        raise ValueError("El hemisferio debe ser E o W.")

    valor = gms_a_grados(g, m, s, h)

    texto = f"{int(g)}° {int(m)}' {s}\" {h}"

    return valor, texto



# CÁLCULO DE ÁREA


def calcular_area_cuadrilatero(
    latA, lonA,
    latB, lonB,
    latC, lonC,
    latD, lonD,
    a, f
):

    puntos = [

        (lonA, latA),
        (lonB, latB),
        (lonC, latC),
        (lonD, latD)

    ]

    area = 0

    for i in range(4):

        x1, y1 = puntos[i]
        x2, y2 = puntos[(i + 1) % 4]

        area += (x1 * y2) - (x2 * y1)

    area_grados = abs(area) / 2

    # Conversión aproximada
    area_m2 = area_grados * (111320 ** 2)

    return {

        "area": area_m2,
        "area_km2": area_m2 / 1_000_000

    }



# MAPA

def generar_mapa_area(
    latA, lonA,
    latB, lonB,
    latC, lonC,
    latD, lonD,
    area
):

    puntos = [

        [latA, lonA],
        [latB, lonB],
        [latC, lonC],
        [latD, lonD],
        [latA, lonA]

    ]

    latitudes = [latA, latB, latC, latD]
    longitudes = [lonA, lonB, lonC, lonD]

    lat_c = sum(latitudes) / 4
    lon_c = sum(longitudes) / 4

    mapa = folium.Map(

        location=[lat_c, lon_c],
        zoom_start=7,
        tiles=None

    )

    folium.TileLayer(

        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/"
              "World_Imagery/MapServer/tile/{z}/{y}/{x}",

        attr="Esri World Imagery",
        name="Imagen Satelital"

    ).add_to(mapa)

    # POLÍGONO

    folium.Polygon(

        locations=puntos,
        color="purple",
        weight=4,
        fill=True,
        fill_color="purple",
        fill_opacity=0.25,
        popup=f"Área = {area:.3f} m²"

    ).add_to(mapa)

    # POLILÍNEA

    folium.PolyLine(

        locations=puntos,
        color="yellow",
        weight=3

    ).add_to(mapa)

    # MARCADORES

    nombres = ["A", "B", "C", "D"]

    for i, punto in enumerate(puntos[:-1]):

        folium.Marker(

            punto,

            popup=f"""
            Punto {nombres[i]}<br>
            Latitud = {punto[0]:.8f}<br>
            Longitud = {punto[1]:.8f}
            """,

            tooltip=f"Punto {nombres[i]}",

            icon=folium.Icon(color="blue")

        ).add_to(mapa)

    # CENTRO DEL POLÍGONO

    folium.Marker(

        [lat_c, lon_c],

        popup=f"Área = {area:.3f} m²",

        tooltip="Área",

        icon=folium.Icon(color="purple")

    ).add_to(mapa)

    folium.LayerControl().add_to(mapa)

    archivo = "mapa_area_cuadrilatero.html"

    ruta = os.path.abspath(archivo)

    mapa.save(ruta)

    webbrowser.open("file://" + ruta)

    print(f"\nMapa generado: {ruta}")



# LOOP PRINCIPAL

while True:

    try:

        print("\nPROGRAMA")
        print("------------------------------------------")
        print("ÁREA DE UN CUADRILÁTERO SOBRE EL ELIPSOIDE")
        print("------------------------------------------")

        nombre_elipsoide, a, f = seleccionar_elipsoide()

        if nombre_elipsoide is None:

            print("Programa finalizado.")
            break

        
        # PUNTO A
        

        latA, latA_txt = leer_latitud("A")
        lonA, lonA_txt = leer_longitud("A")

        
        # PUNTO B
        

        latB, latB_txt = leer_latitud("B")
        lonB, lonB_txt = leer_longitud("B")

        
        # PUNTO C
        

        latC, latC_txt = leer_latitud("C")
        lonC, lonC_txt = leer_longitud("C")

        
        # PUNTO D
        

        latD, latD_txt = leer_latitud("D")
        lonD, lonD_txt = leer_longitud("D")

        
        # CÁLCULO DE ÁREA
        

        resultado = calcular_area_cuadrilatero(

            latA, lonA,
            latB, lonB,
            latC, lonC,
            latD, lonD,
            a, f

        )

        area = resultado["area"]
        area_km2 = resultado["area_km2"]

        
        # SALIDA
        

        print("\nRESULTADOS")
        print("--------------------------")

        print(f"Área = {area:.3f} m²")
        print(f"Área = {area_km2:.3f} km²")

        
        # MAPA
        

        generar_mapa_area(

            latA, lonA,
            latB, lonB,
            latC, lonC,
            latD, lonD,
            area

        )

        
        # FIGURA SIMPLE
        

        fig = plt.figure(figsize=(10, 8))

        ax = fig.add_subplot(111)

        x = [lonA, lonB, lonC, lonD, lonA]
        y = [latA, latB, latC, latD, latA]

        ax.plot(

            x,
            y,

            color="purple",
            linewidth=2.5,
            marker="o"

        )

        ax.fill(

            x,
            y,

            color="purple",
            alpha=0.25

        )

        ax.text(lonA, latA, "A")
        ax.text(lonB, latB, "B")
        ax.text(lonC, latC, "C")
        ax.text(lonD, latD, "D")

        ax.set_title(
            "CUADRILÁTERO FORMADO POR LOS 4 VÉRTICES"
        )

        ax.set_xlabel("Longitud")
        ax.set_ylabel("Latitud")

        ax.grid(True)

        plt.show()

    except ValueError as error:

        print("Error:", error)

    except Exception as error:

        print("Error:", error)