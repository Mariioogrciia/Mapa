import pandas as pd
from statsbombpy import sb
from tqdm import tqdm

# ==========================================
# FASE 1: DESCARGAR Y GUARDAR LOS DATOS EN BRUTO (CSV)
# ==========================================
print("Iniciando conexión con StatsBomb para descargar la historia completa...\n")

# Lista de IDs de las temporadas (Desde 2007/2008 hasta 2020/2021)
# 40: 07/08 | 41: 08/09 | 21: 09/10 | 22: 10/11 | 23: 11/12 | 24: 12/13 | 25: 13/14
# 26: 14/15 | 27: 15/16 |  2: 16/17 |  1: 17/18 |  4: 18/19 | 42: 19/20 | 90: 20/21
temporadas_ids = [40, 41, 21, 22, 23, 24, 25, 26, 27, 2, 1, 4, 42, 90]

# Lista vacía para ir guardando todos los pases de todas las temporadas
lista_pases_totales = []

# Bucle externo: Iteramos por cada temporada elegida
for season_id in temporadas_ids:
    print(f"--- Procesando temporada ID: {season_id} ---")
    
    # Obtenemos los partidos de esa temporada
    partidos = sb.matches(competition_id=11, season_id=season_id)
    
    # Filtramos solo los partidos donde jugó el Barcelona
    partidos_barca = partidos[(partidos['home_team'] == 'Barcelona') | (partidos['away_team'] == 'Barcelona')]
    print(f"Partidos del Barça encontrados: {len(partidos_barca)}")

    # Bucle interno: Iteramos sobre todos los IDs de los partidos con una barra de progreso
    for match_id in tqdm(partidos_barca['match_id'], desc=f"Descargando pases (Temp {season_id})"):
        
        # 1. Descargar eventos del partido
        eventos = sb.events(match_id=match_id)
        
        # 2. Filtrar pases del Barça
        if 'type' in eventos.columns and 'team' in eventos.columns:
            pases = eventos[(eventos['type'] == 'Pass') & (eventos['team'] == 'Barcelona')]
            
            # Limpiar filas donde falta la ubicación
            pases = pases.dropna(subset=['location', 'pass_end_location'])
            
            # 3. Extraer solo las columnas que nos interesan
            for index, row in pases.iterrows():
                loc_inicio = row['location']
                loc_fin = row['pass_end_location']
                
                # Guardamos cada pase como un pequeño diccionario
                pase_limpio = {
                    'season_id': season_id, # Añadimos el año para tenerlo clasificado
                    'match_id': match_id,
                    'minute': row['minute'],
                    'player': row.get('player', 'Desconocido'),
                    'x_inicio': loc_inicio[0],
                    'y_inicio': loc_inicio[1],
                    'x_fin': loc_fin[0],
                    'y_fin': loc_fin[1],
                    'pass_outcome': row.get('pass_outcome', 'Completado') # Nos dice si el pase fue bueno o malo
                }
                lista_pases_totales.append(pase_limpio)
    
    print("\n") # Salto de línea entre temporadas para que quede limpio en consola

# 4. Convertimos la inmensa lista de pases en un DataFrame de Pandas
df_dataset_final = pd.DataFrame(lista_pases_totales)

# 5. ¡GUARDAMOS EL ARCHIVO EN TU CARPETA!
nombre_archivo = 'dataset_pases_barca_historico_completo.csv'
df_dataset_final.to_csv(nombre_archivo, index=False)

print(f"==========================================")
print(f"¡HECHO HISTÓRICO! Se han guardado {len(df_dataset_final)} pases en tu disco duro.")
print(f"Archivo generado: {nombre_archivo}")
print("==========================================")