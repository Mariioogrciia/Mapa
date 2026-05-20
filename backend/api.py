"""
FastAPI backend para auditoría táctica con autoencoder
Expone endpoints para predicción, análisis y visualización
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import models
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

app = FastAPI(title="Barcelona Tactical Audit API", version="1.0")

# Configurar CORS para Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# CARGA DE DATOS Y MODELO
# ============================================================================

import os

# Rutas relativas (se ejecuta desde la raíz del proyecto)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "raw", "dataset_pases_barca_historico_completo.csv")
MODEL_PATH = os.path.join(BASE_DIR, "data", "models", "autoencoder_barca_model.h5")

# Cargar CSV
df = pd.read_csv(CSV_PATH)

# Cargar modelo con manejo seguro de errores de deserialización
try:
    modelo = models.load_model(MODEL_PATH, compile=False)
except Exception:
    modelo = models.load_model(
        MODEL_PATH,
        custom_objects={
            'mse': tf.keras.losses.MeanSquaredError(),
            'mae': tf.keras.metrics.MeanAbsoluteError(),
            'mape': tf.keras.metrics.MeanAbsolutePercentageError(),
            'cosine_similarity': tf.keras.metrics.CosineSimilarity(),
        }
    )

modelo.compile(optimizer=tf.keras.optimizers.Adam(1e-4), loss="mse")

# Configuración de normalización (mismo p99 usado en entrenamiento)
p99 = 1.414

# IDs de temporadas para separación train/test/explore
SEASON_TRAIN_IDS = [40, 41, 21, 22, 23, 24, 26, 27]
SEASON_TEST_IDS = [2, 1, 4]
SEASON_EXPLORE_IDS = [25, 42, 90]

SEASON_NAMES = {
    1: "2017/2018", 2: "2018/2019", 4: "2019/2020",
    21: "2007/2008", 22: "2008/2009", 23: "2009/2010",
    24: "2010/2011", 25: "2011/2012", 26: "2011/2012",
    27: "2012/2013", 40: "2013/2014", 41: "2014/2015",
    42: "2015/2016", 90: "2020/2021"
}

# Umbral de anomalía (percentil 95 del train, calculado durante entrenamiento)
ANOMALY_THRESHOLD = 0.074042

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def build_heatmaps_from_df(dataframe, bins=64, x_range=(0, 120), y_range=(0, 80)):
    """Convierte cada partido en una matriz 64x64 con np.histogram2d."""
    heatmaps = []
    match_ids = []

    for match_id, match_df in dataframe.groupby("match_id", sort=False):
        coords = match_df[["x_inicio", "y_inicio"]].dropna()
        if coords.empty:
            continue

        histogram, _, _ = np.histogram2d(
            coords["x_inicio"].to_numpy(),
            coords["y_inicio"].to_numpy(),
            bins=bins,
            range=[list(x_range), list(y_range)],
        )

        heatmaps.append(histogram.T.astype(np.float32))
        match_ids.append(match_id)

    if not heatmaps:
        return np.empty((0, bins, bins), dtype=np.float32), []

    return np.stack(heatmaps, axis=0), match_ids


def preprocess_maps(X_raw, p99=1.414):
    """Preprocesa mapas crudos: raíz cuadrada + normalización."""
    X_proc = np.sqrt(X_raw)
    X = np.clip(X_proc / p99, 0.0, 1.0).astype(np.float32)
    return X[..., np.newaxis]


def map_to_base64_image(heatmap, cmap='inferno'):
    """Convierte una matriz a imagen PNG en base64."""
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(heatmap.squeeze(), cmap=cmap, origin='lower', vmin=0, vmax=1)
    ax.axis('off')
    plt.colorbar(im, ax=ax)
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    img_base64 = base64.b64encode(buf.read()).decode()
    return f"data:image/png;base64,{img_base64}"


def compute_comparison_image(original, reconstruction):
    """Crea imagen de comparación lado a lado."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    axes[0].imshow(original.squeeze(), cmap='inferno', origin='lower', vmin=0, vmax=1)
    axes[0].set_title('Original')
    axes[0].axis('off')
    
    axes[1].imshow(reconstruction.squeeze(), cmap='inferno', origin='lower', vmin=0, vmax=1)
    axes[1].set_title('Reconstruido')
    axes[1].axis('off')
    
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    img_base64 = base64.b64encode(buf.read()).decode()
    return f"data:image/png;base64,{img_base64}"


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/api/health")
def health():
    """Health check."""
    return {"status": "ok", "model": "loaded"}


@app.get("/api/matches")
def get_matches(season_id: int = None):
    """Obtiene lista de partidos, opcionalmente filtrada por temporada."""
    if season_id:
        matches = df[df['season_id'] == season_id]['match_id'].unique().tolist()
    else:
        matches = df['match_id'].unique().tolist()
    
    return {
        "total": len(matches),
        "matches": sorted(matches)[:100]  # Límite de 100 para no saturar
    }


@app.get("/api/seasons")
def get_seasons():
    """Obtiene lista de temporadas con información."""
    seasons_data = []
    for season_id in sorted(df['season_id'].unique()):
        count = len(df[df['season_id'] == season_id]['match_id'].unique())
        season_type = "train" if season_id in SEASON_TRAIN_IDS else \
                      "test" if season_id in SEASON_TEST_IDS else \
                      "explore"
        
        seasons_data.append({
            "id": int(season_id),
            "name": SEASON_NAMES.get(season_id, f"Season {season_id}"),
            "matches": count,
            "type": season_type
        })
    
    return {"seasons": seasons_data}


@app.post("/api/predict")
def predict_match(match_id: int):
    """Predice anomalía para un partido específico."""
    try:
        # Obtener datos del partido
        match_data = df[df['match_id'] == match_id]
        if match_data.empty:
            raise HTTPException(status_code=404, detail="Partido no encontrado")
        
        season_id = int(match_data.iloc[0]['season_id'])
        
        # Construir heatmap
        X_raw, _ = build_heatmaps_from_df(match_data)
        if X_raw.size == 0:
            raise HTTPException(status_code=400, detail="No se pudo procesar el heatmap")
        
        X_proc = preprocess_maps(X_raw, p99=p99)
        
        # Predicción
        recon = modelo.predict(X_proc, verbose=0)
        mse = float(np.mean((X_proc - recon) ** 2))
        
        is_anomalous = mse > ANOMALY_THRESHOLD
        # anomaly_score: 0% si es normal, porcentaje sobre umbral si es anómalo
        anomaly_score = min(100, ((mse - ANOMALY_THRESHOLD) / ANOMALY_THRESHOLD) * 100) if is_anomalous else 0
        
        # Generar imágenes
        original_img = map_to_base64_image(X_proc[0])
        reconstructed_img = map_to_base64_image(recon[0])
        comparison_img = compute_comparison_image(X_proc[0], recon[0])
        
        return {
            "match_id": match_id,
            "season_id": season_id,
            "season_name": SEASON_NAMES.get(season_id, f"Season {season_id}"),
            "mse": mse,
            "threshold": ANOMALY_THRESHOLD,
            "is_anomalous": is_anomalous,
            "anomaly_score": anomaly_score,
            "original_image": original_img,
            "reconstructed_image": reconstructed_img,
            "comparison_image": comparison_img,
            "interpretation": {
                "mse_level": "Alto (anómalo)" if is_anomalous else "Normal",
                "message": "Barcelona jugó de forma diferente a su patrón histórico" if is_anomalous 
                          else "Barcelona mantuvo su identidad táctica histórica"
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/statistics")
def get_statistics():
    """Obtiene estadísticas generales del dataset."""
    total_matches = len(df['match_id'].unique())
    total_seasons = len(df['season_id'].unique())
    
    train_count = len(df[df['season_id'].isin(SEASON_TRAIN_IDS)]['match_id'].unique())
    test_count = len(df[df['season_id'].isin(SEASON_TEST_IDS)]['match_id'].unique())
    explore_count = len(df[df['season_id'].isin(SEASON_EXPLORE_IDS)]['match_id'].unique())
    
    return {
        "total_matches": total_matches,
        "total_seasons": total_seasons,
        "training_matches": train_count,
        "test_matches": test_count,
        "explore_matches": explore_count,
        "anomaly_threshold": ANOMALY_THRESHOLD,
        "model_info": {
            "name": "Convolutional Autoencoder",
            "input_shape": [64, 64, 1],
            "encoder_filters": [64, 32, 16],
            "decoder_filters": [16, 32, 64],
            "loss_function": "MSE",
            "optimizer": "Adam (lr=1e-4)"
        }
    }


@app.get("/api/top-anomalies")
def get_top_anomalies(limit: int = 10, season_id: int = None):
    """Obtiene los partidos más anómalos."""
    anomalies = []
    
    # Filtrar temporadas
    if season_id:
        seasons_to_check = [season_id]
    else:
        seasons_to_check = SEASON_EXPLORE_IDS  # Por defecto, temporadas nuevas
    
    for season in seasons_to_check:
        season_data = df[df['season_id'] == season]
        match_ids = season_data['match_id'].unique()
        
        for match_id in match_ids:
            match_data = season_data[season_data['match_id'] == match_id]
            X_raw, _ = build_heatmaps_from_df(match_data)
            
            if X_raw.size > 0:
                X_proc = preprocess_maps(X_raw, p99=p99)
                recon = modelo.predict(X_proc, verbose=0)
                mse = float(np.mean((X_proc - recon) ** 2))
                
                is_anom = mse > ANOMALY_THRESHOLD
                anom_score = min(100, ((mse - ANOMALY_THRESHOLD) / ANOMALY_THRESHOLD) * 100) if is_anom else 0
                anomalies.append({
                    "match_id": int(match_id),
                    "season_id": int(season),
                    "season_name": SEASON_NAMES.get(season, f"Season {season}"),
                    "mse": mse,
                    "is_anomalous": is_anom,
                    "anomaly_score": anom_score
                })
    
    # Ordenar por MSE descendente y tomar los top
    anomalies.sort(key=lambda x: x['mse'], reverse=True)
    
    return {
        "total": len(anomalies),
        "limit": limit,
        "anomalies": anomalies[:limit]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
