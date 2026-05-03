import math as m
import folium
import webbrowser

# ------------------ COORDENADAS REALES ------------------
# (Estas se usan SOLO para el mapa)

# Punto A real
latA_real = 4.614525
lonA_real = -74.06283056

# Punto B real
latB_real = 4.613794
lonB_real = -74.06313611

# Punto P real
latP_real = 4.61125833
lonP_real = -74.069875

# ------------------ ENTRADA ------------------
def entradadenortesyestes():
    print("Dijite el valor N y E del punto A")
    Na = float(input("NORTE(A): "))
    Ea = float(input("ESTE(A): "))

    print("Dijite el valor N y E del punto B")
    Nb = float(input("NORTE(B): "))
    Eb = float(input("ESTE(B): "))

    print("Dijite el valor de α")
    a_g = float(input("α grados: "))
    a_m = float(input("α minutos: "))
    a_s = float(input("α segundos: "))

    print("Dijite el valor de β")
    b_g = float(input("β grados: "))
    b_m = float(input("β minutos: "))
    b_s = float(input("β segundos: "))

    alpha_dec = a_g + a_m/60 + a_s/3600
    beta_dec = b_g + b_m/60 + b_s/3600

    return Na, Ea, Nb, Eb, m.radians(alpha_dec), m.radians(beta_dec), alpha_dec, beta_dec

# ------------------ CÁLCULO ------------------
def calculo_p(Na, Ea, Nb, Eb, ar, br, ad, bd):
    hiang = abs(ad - bd)
    delta = 180 - (ad + bd)

    if hiang > delta:
        print("Método 1")
        ctg_a = 1 / m.tan(ar)
        ctg_b = 1 / m.tan(br)
        z = ctg_a + ctg_b

        Np = ((Eb - Ea) + Na * ctg_b + Nb * ctg_a) / z
        Ep = ((Na - Nb) + Ea * ctg_b + Eb * ctg_a) / z

    elif hiang < delta:
        print("Método 2")
        ctg_b = 1 / m.tan(ar)
        ctg_a = 1 / m.tan(br)
        z = ctg_a + ctg_b

        Np = ((Eb - Ea) + Nb * ctg_b + Na * ctg_a) / z
        Ep = ((Na - Nb) + Eb * ctg_b + Ea * ctg_a) / z
    else:
        print("NO VALIDO")
        return None, None

    print("Norte en p =", Np)
    print("Este en p =", Ep)

    return Np, Ep

# ------------------ MAPA ------------------
def generar_mapa():
    mapa = folium.Map(location=[latP_real, lonP_real], zoom_start=18)

    # Marcadores reales
    folium.Marker([latA_real, lonA_real], popup="Punto A", tooltip="A").add_to(mapa)
    folium.Marker([latB_real, lonB_real], popup="Punto B", tooltip="B").add_to(mapa)
    folium.Marker([latP_real, lonP_real], popup="Punto P", tooltip="P").add_to(mapa)

    # Triángulo
    puntos = [
        [latA_real, lonA_real],
        [latB_real, lonB_real],
        [latP_real, lonP_real],
        [latA_real, lonA_real]
    ]

    folium.PolyLine(puntos).add_to(mapa)

    mapa.save("mapa_triangulo.html")
    print("Mapa generado correctamente")

    webbrowser.open("mapa_triangulo.html")

# ------------------ MAIN ------------------
Na, Ea, Nb, Eb, ar, br, ad, bd = entradadenortesyestes()

Np, Ep = calculo_p(Na, Ea, Nb, Eb, ar, br, ad, bd)

# 👇 Se genera el mapa con coordenadas reales
generar_mapa()