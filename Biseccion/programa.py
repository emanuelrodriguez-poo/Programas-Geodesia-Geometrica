import math as m
import folium
import webbrowser

# =========================================================
# COORDENADAS REALES 
# =========================================================

# Punto A
latA_real = 4.614525
lonA_real = -74.06283056

# Punto B
latB_real = 4.613794
lonB_real = -74.06313611

# Punto P
latP_real = 4.61125833
lonP_real = -74.069875


# =========================================================
# ENTRADA DE DATOS
# =========================================================

def entradadenortesyestes():

    print("\n--- PUNTO A ---")
    Na = float(input("NORTE(A): "))
    Ea = float(input("ESTE(A): "))

    print("\n--- PUNTO B ---")
    Nb = float(input("NORTE(B): "))
    Eb = float(input("ESTE(B): "))

    print("\n--- ANGULO α ---")
    a_g = float(input("Grados: "))
    a_m = float(input("Minutos: "))
    a_s = float(input("Segundos: "))

    print("\n--- ANGULO β ---")
    b_g = float(input("Grados: "))
    b_m = float(input("Minutos: "))
    b_s = float(input("Segundos: "))

    # Conversión a grados decimales
    alpha_dec = a_g + a_m/60 + a_s/3600
    beta_dec = b_g + b_m/60 + b_s/3600

    # Conversión a radianes
    ar = m.radians(alpha_dec)
    br = m.radians(beta_dec)

    return Na, Ea, Nb, Eb, ar, br, alpha_dec, beta_dec


# =========================================================
# CALCULO DEL PUNTO P
# =========================================================

def calculo_p(Na, Ea, Nb, Eb, ar, br):

    # Cotangentes
    ctg_a = 1 / m.tan(ar)
    ctg_b = 1 / m.tan(br)

    z = ctg_a + ctg_b

    # =====================================================
    # ECUACIONES CORREGIDAS
    # =====================================================

    Np = (
        (Eb - Ea) +
        Na * ctg_b +
        Nb * ctg_a
    ) / z

    Ep = (
        (Nb - Na) +
        Ea * ctg_b +
        Eb * ctg_a
    ) / z

    return Np, Ep


# =========================================================
# MAPA
# =========================================================

def generar_mapa():

    mapa = folium.Map(
        location=[latP_real, lonP_real],
        zoom_start=18
    )

    # Punto A
    folium.Marker(
        [latA_real, lonA_real],
        popup="Punto A",
        tooltip="A"
    ).add_to(mapa)

    # Punto B
    folium.Marker(
        [latB_real, lonB_real],
        popup="Punto B",
        tooltip="B"
    ).add_to(mapa)

    # Punto P
    folium.Marker(
        [latP_real, lonP_real],
        popup="Punto P",
        tooltip="P"
    ).add_to(mapa)

    # Triángulo
    puntos = [
        [latA_real, lonA_real],
        [latB_real, lonB_real],
        [latP_real, lonP_real],
        [latA_real, lonA_real]
    ]

    folium.PolyLine(
        puntos,
        color="blue",
        weight=3
    ).add_to(mapa)

    mapa.save("mapa_triangulo.html")

    print("\nMapa generado correctamente")

    webbrowser.open("mapa_triangulo.html")


# =========================================================
# PROGRAMA PRINCIPAL
# =========================================================

Na, Ea, Nb, Eb, ar, br, ad, bd = entradadenortesyestes()

Np, Ep = calculo_p(
    Na,
    Ea,
    Nb,
    Eb,
    ar,
    br
)

print("\n===== RESULTADOS =====")
print(f"Norte P = {Np:.3f}")
print(f"Este  P = {Ep:.3f}")

# Generar mapa
generar_mapa()