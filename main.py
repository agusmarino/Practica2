import csv
import locale
from datetime import datetime
from pathlib import Path
import os
import json
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

fechas_vistas = set()
diasMAX={"lunes": 0, "martes": 0, "miércoles": 0, "jueves": 0, "viernes": 0, "sábado": 0, "domingo": 0}
dias_entrenamiento = []
totaldias = []
totalDiasSinRep = set()
campeonMax = {} #punto 5
totalDiasEntrenamiento = {} # punto 6
entrenamientoFinde = {} # punto 7
promedios = {}
data_json = {
    "total_registros": 0,
    "dias": {}
}
total_registros = 0
entrenamientos_dia = {}  # Diccionario anidado: {día: {campeon: cantidad}}

with open('Practica2/actividad_2.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for fila in reader:
        if fila["actividad"] == "entrenamiento individual":
            fecha = datetime.strptime(fila['timestamp'], "%Y-%m-%d %H:%M")
            dia = fecha.strftime("%A") 
            fecha_sola = fecha.date()
            totaldias.append(fecha) #punto 4
        
            if fecha_sola not in fechas_vistas:
                fechas_vistas.add(fecha_sola)
                dia_semana = dia
                fecha_texto = fecha.strftime("%d/%m/%Y")
                dias_entrenamiento.append((fecha_texto, dia)) #punto 2
                        
            diasMAX [dia]+=1 #punto 3
            
            campeon = fila["campeon"]#punto 5
            campeonMax[campeon] = campeonMax.get(campeon, 0) + 1#punto 5

            entrenamiento = datetime.strptime(fila["timestamp"],"%Y-%m-%d %H:%M") # punto 6
            diaSemana = entrenamiento.strftime("%A")
            totalDiasEntrenamiento[diaSemana] = totalDiasEntrenamiento.get(diaSemana, 0) + 1 # punto 6
            
            if dia in ("sábado", "domingo"):
                entrenamientoFinde[campeon] = entrenamientoFinde.get(campeon, 0) + 1
                
            total_registros += 1
            if dia not in entrenamientos_dia:
                entrenamientos_dia[dia] = {}

            # Si el campeón no está dentro del día, lo inicializo
            if campeon not in entrenamientos_dia[dia]:
                entrenamientos_dia[dia][campeon] = 0

            # Sumo 1 entrenamiento
            entrenamientos_dia[dia][campeon] += 1


                
#punto 2--------------------------------------------------------------------
print(dias_entrenamiento) # punto 2

#punto 3--------------------------------------------------------------------
max_valor = max(diasMAX.values()) # punto 3
dias_top = [d for d,v in diasMAX.items() if v == max_valor]
print("Días con más entrenamientos:", dias_top)

#punto 4--------------------------------------------------------------------
totaldias.sort() #punto 4
dias_entre = lambda f1, f2: abs((f2 - f1).days)
print("Días transcurridos:", dias_entre(totaldias[0], totaldias[-1]))

#punto5--------------------------------------------------------------------
campeonFrecuente = max(campeonMax, key=campeonMax.get)# punto 5
print ("El campeon que mas entreno es:",campeonFrecuente)# punto 5

#punto 5--------------------------------------------------------------------
cantidad_semanas = dias_entre(totaldias[0], totaldias[-1]) / 7
promedios = {d: round(v / cantidad_semanas, 2) for d, v in totalDiasEntrenamiento.items()}
print("El promedio de entrenamiento por día es:", promedios)

#punto 7--------------------------------------------------------------------
campeonFinde= max(entrenamientoFinde, key=entrenamientoFinde.get) #punto 7
print("El campeon que mas entreno los findes es: ",campeonFinde)

#punto 8--------------------------------------------------------------------
cwd = Path.cwd()
subdir = cwd / 'Practica2' / 'salida'
subdir.mkdir(parents=True, exist_ok=True)
print('Nueva carpeta creada en:', subdir)

ruta_csv = subdir / 'entrenamientos_por_campeon.csv'

with ruta_csv.open('w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['campeon', 'cantidad_entrenamientos'])
    for campeon, cantidad in campeonMax.items():
        writer.writerow([campeon, cantidad])

print('CSV generado en:', ruta_csv)

#punto 9--------------------------------------------------------------------
data_json["total_registros"] = total_registros
data_json["dias"] = entrenamientos_dia

ruta_json = subdir / "resumen_entrenamientos.json"

with ruta_json.open("w", encoding="utf-8") as f:
    json.dump(data_json, f, ensure_ascii=False, indent=4)

print("Archivo JSON generado en:", ruta_json)