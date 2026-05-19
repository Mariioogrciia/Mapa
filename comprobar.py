from statsbombpy import sb

# Descargar la lista de todas las competiciones disponibles
competiciones = sb.competitions()

# Filtrar solo La Liga (España)
la_liga = competiciones[competiciones['competition_id'] == 11]

# Mostrar el nombre de la temporada y su ID secreto
print(la_liga[['season_name', 'season_id']])