import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "6d1a6f44-213b-4d21-a528-a6893b21afd4"



def geocoding(ubicación, key):
    while ubicación == "":
        ubicación = input("Ingresa la ubicación nuevamente: ")

    geo_url = "https://graphhopper.com/api/1/geocode?"
    url = geo_url + urllib.parse.urlencode({"q":ubicación, "limit":"1", "key":key})



    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    # aquí iba el print con el url y la ubicación? va a aparecer más abajo

    if json_status == 200:
        json_data = requests.get(url).json()
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        nombre = json_data["hits"][0]["name"]
        valor = json_data["hits"][0]["osm_value"]

        if "country" in json_data["hits"][0]:
            país = json_data["hits"][0]["country"]
        else:
            país = ""

        if len(país) !=0:
            nueva_ubi = nombre + ", " + país
        else:
            nueva_ubi = nombre
        
        #print("Información de: " + nueva_ubi + " (Tipo de ubicación: " + valor + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        nueva_ubi = ubicación
    return json_status,lat,lng,nueva_ubi



while True:
    lugar1 = input("Ingrese un lugar de salida: ")
    if lugar1 == "q":
        break
    origen = geocoding(lugar1, key)

    lugar2 = input("Ingrese un lugar de destino: ")
    if lugar2 == "q":
        break
    destino = geocoding(lugar2, key)

    # en el siguiente bloque:
    # coordOrigen: lat y long del origen
    # coordDestino: lat y long del destino
    # paths_url: url para obtener ruta entre origen y destino
    # paths_status: el código de estado que devuelve url_camino
    # paths_data: datos JSON devueltos por el url_camino

    print("================================")
    print("Indicaciones de " + origen[3] + " a " + destino[3])
    print("================================")
    

    if origen[0] == 200 and destino[0] == 200:
        coordOrigen = "&point="+str(origen[1])+"%2C"+str(origen[2])
        coordDestino = "&point="+str(destino[1])+"%2C"+str(destino[2])
        paths_url = route_url + urllib.parse.urlencode({"key":key}) + coordOrigen + coordDestino
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        #print("Estado del API de Ruta: " + str(paths_status) + "\nURL del API de Ruta:\n" + paths_url)
    
    if paths_status == 200:
        km = (paths_data["paths"][0]["distance"])/1000          # Conversión de m a km
        kMxL = float(km)/10                                       # Se asume rendimiento de 10km/L
        hora = int(paths_data["paths"][0]["time"]/1000/60/60)
        minuto = int(paths_data["paths"][0]["time"]/1000/60%60)
        segundo = int(paths_data["paths"][0]["time"]/1000%60)
        print("Distancia recorrida: {0:.2f} km".format(km))
        print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hora, minuto, segundo))
        print("Combustible requerido (litros): {0:.2f} Litros".format(kMxL))

        for each in range(len(paths_data["paths"][0]["instructions"])):
            path = paths_data["paths"][0]["instructions"][each]["text"]
            distance = paths_data["paths"][0]["instructions"][each]["distance"]
            print("{0} ({1:.2f} km)".format(path, distance/1000))
            print("================================")




#    print(origen)
#    print("--------------------------------")
#    print(destino)
#    print("================================")






