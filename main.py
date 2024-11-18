import geoip2.database
import subprocess
import folium
import re

def mostrar_ubicacion_y_traza(ip_destino):
    # Geolocalización
    lector = geoip2.database.Reader("GeoLite2-City.mmdb") # Asegúrate de tener la base de datos
    respuesta = lector.city(ip_destino)
    latitud = respuesta.location.latitude
    longitud = respuesta.location.longitude

    # Crear el mapa antes del bucle
    mapa = folium.Map(location=[latitud, longitud], zoom_start=5)
    folium.Marker([latitud, longitud], popup="Destino").add_to(mapa)

    # Trazado de Ruta
    resultado_traceroute = subprocess.run(["tracert", ip_destino], capture_output=True, text=True)
    saltos = resultado_traceroute.stdout.splitlines()[1:]  # Ignora la primera línea

    for salto in saltos:
        # Extraer la dirección IP del salto (puede haber varias formas de hacerlo, 
        # dependiendo del formato exacto de la salida de tracert)
        match = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', salto)

        try:
            if match:
                ip_salto = match.group()

                # Geolocalización del salto
                respuesta_salto = lector.city(ip_salto)
                latitud_salto = respuesta_salto.location.latitude
                longitud_salto = respuesta_salto.location.longitude

                # Agregar marcador al mapa
                folium.Marker([latitud_salto, longitud_salto], popup=f"Salto: {ip_salto}").add_to(mapa)

                print(f"Salto: {ip_salto}, Ubicación: {respuesta_salto.city.name}, {respuesta_salto.country.name}")

        except geoip2.errors.AddressNotFoundError:
                    # Ignorar si la dirección no se encuentra en la base de datos
                    print(f"Salto: {ip_salto}, Ubicación: No disponible (dirección privada o local)")

    # Visualización
    mapa = folium.Map(location=[latitud, longitud], zoom_start=5)
    folium.Marker([latitud, longitud], popup="Destino").add_to(mapa)
    mapa.save("mapa.html")

    print("Saltos de la Traza:")
    for salto in saltos:
        print(salto)

# Ejemplo de uso
ip_destino = "213.140.39.119"  # Reemplaza con la IP de destino real
mostrar_ubicacion_y_traza(ip_destino)