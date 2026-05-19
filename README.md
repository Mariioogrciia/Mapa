# Interfaz Streamlit para Auditoría Táctica (Autoencoder)

Instrucciones rápidas:

1. Coloca `autoencoder_barca_model.h5` y `dataset_pases_barca_historico_completo.csv` en la carpeta del proyecto.
2. Crea un entorno virtual e instala dependencias:

```bash
python -m venv env
env\Scripts\activate    # Windows
pip install -r requirements.txt
```

3. Ejecuta la app Streamlit:

```bash
streamlit run streamlit_app.py
```

La interfaz permite seleccionar una temporada y un `match_id`, evaluar el partido con el autoencoder entrenado, visualizar el mapa original y la reconstrucción, y calcular MSE/MAE. También muestra un ranking de partidos ordenado por MSE.
