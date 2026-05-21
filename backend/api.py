"""
FastAPI backend para auditoría táctica con autoencoder
Expone endpoints para predicción, análisis y visualización
"""

from fastapi import FastAPI, HTTPException, Body
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import models, layers
import base64
import math
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


def build_default_autoencoder(input_shape=(64, 64, 1)):
    """Construye la misma arquitectura del notebook para usar como fallback.
    Este modelo NO está entrenado; sirve para permitir que la API arranque y responda."""
    inputs = layers.Input(shape=input_shape, name="heatmap_input")

    # Encoder
    x = layers.Conv2D(64, (3, 3), activation="relu", padding="same")(inputs)
    x = layers.MaxPooling2D((2, 2), padding="same")(x)

    x = layers.Conv2D(32, (3, 3), activation="relu", padding="same")(x)
    x = layers.MaxPooling2D((2, 2), padding="same")(x)

    x = layers.Conv2D(16, (3, 3), activation="relu", padding="same")(x)
    latent = layers.MaxPooling2D((2, 2), padding="same", name="latent_space")(x)

    # Decoder
    x = layers.Conv2D(16, (3, 3), activation="relu", padding="same")(latent)
    x = layers.UpSampling2D((2, 2))(x)

    x = layers.Conv2D(32, (3, 3), activation="relu", padding="same")(x)
    x = layers.UpSampling2D((2, 2))(x)

    x = layers.Conv2D(64, (3, 3), activation="relu", padding="same")(x)
    x = layers.UpSampling2D((2, 2))(x)

    outputs = layers.Conv2D(1, (3, 3), activation="sigmoid", padding="same", name="reconstruction")(x)

    m = models.Model(inputs, outputs, name="conv_autoencoder_barca_fallback")
    m.compile(optimizer=tf.keras.optimizers.Adam(1e-4), loss="mse")
    return m

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

# Cargar modelo con manejo seguro de errores de deserialización.
# Si no existe el archivo, construimos un autoencoder de fallback (sin entrenar)
MODEL_LOADED = False
if os.path.exists(MODEL_PATH):
    try:
        modelo = models.load_model(MODEL_PATH, compile=False)
        MODEL_LOADED = True
    except Exception:
        try:
            modelo = models.load_model(
                MODEL_PATH,
                custom_objects={
                    'mse': tf.keras.losses.MeanSquaredError(),
                    'mae': tf.keras.metrics.MeanAbsoluteError(),
                    'mape': tf.keras.metrics.MeanAbsolutePercentageError(),
                    'cosine_similarity': tf.keras.metrics.CosineSimilarity(),
                }
            )
            MODEL_LOADED = True
        except Exception:
            # Intentar cargar solo los pesos en la arquitectura conocida (compatibilidad HDF5 antigua)
            try:
                modelo = build_default_autoencoder()
                modelo.load_weights(MODEL_PATH)
                MODEL_LOADED = True
                print("INFO: Cargados pesos en la arquitectura local desde HDF5 (load_weights).")
            except Exception:
                modelo = None
                MODEL_LOADED = False
else:
    modelo = None
    MODEL_LOADED = False


if not MODEL_LOADED:
    # Construimos un modelo fallback no entrenado para que la API pueda iniciar.
    modelo = build_default_autoencoder()
    print("WARNING: modelo preentrenado no encontrado en data/models/. Usando modelo fallback sin entrenar.")
else:
    modelo.compile(optimizer=tf.keras.optimizers.Adam(1e-4), loss="mse")

# Configuración de normalización (intentamos reproducir el p99 calculado en el notebook)
def estimate_p99_from_train(df, season_train_ids, bins=64):
    """Estima el percentil 99 usado en el notebook a partir de los partidos de entrenamiento.
    Si falla o no hay datos, devuelve None.
    """
    try:
        train_df = df[df['season_id'].isin(season_train_ids)]
        if train_df.empty:
            return None

        X_raw_train, _ = build_heatmaps_from_df(train_df, bins=bins)
        if X_raw_train.size == 0:
            return None

        X_train_proc = np.sqrt(X_raw_train)
        p99_val = float(np.percentile(X_train_proc, 99))
        if p99_val <= 0:
            return None
        return p99_val
    except Exception:
        return None


# Valor por defecto; intentaremos estimar más abajo cuando SEASON_TRAIN_IDS esté definido
p99 = 1.414

# IDs de temporadas para separación train/test/explore
SEASON_TRAIN_IDS = [40, 41, 21, 22, 23, 24, 26, 27, 25, 42]
# Mantener test como estaba
SEASON_TEST_IDS = [2, 1]
# Explore explícito: 2019/2020 (4) y 2020/2021 (90)
SEASON_EXPLORE_IDS = [4, 90]

SEASON_NAMES = {
    1: "2017/2018", 2: "2018/2019", 4: "2019/2020",
    21: "2007/2008", 22: "2008/2009", 23: "2009/2010",
    24: "2010/2011", 25: "2011/2012", 26: "2011/2012",
    27: "2012/2013", 40: "2013/2014", 41: "2014/2015",
    42: "2015/2016", 90: "2020/2021"
}

# Umbral de anomalía (percentil 95 del train, calculado durante entrenamiento)
ANOMALY_THRESHOLD = 0.074042

# Si existe un summary generado por el notebook, usar su umbral y registrar metadata
try:
    diag_path = os.path.join(BASE_DIR, 'data', 'models', 'diagnostic_summary.json')
    if os.path.exists(diag_path):
        import json
        with open(diag_path, 'r', encoding='utf-8') as _f:
            diag = json.load(_f)
        thr = diag.get('threshold_95_train') or diag.get('threshold') or None
        if thr is not None:
            ANOMALY_THRESHOLD = float(thr)
            print(f"INFO: ANOMALY_THRESHOLD cargado desde diagnostic_summary.json = {ANOMALY_THRESHOLD}")
        # Cargar estadísticas del train (mean/std) para z-score y percentil
        train_stats = diag.get('train', {}) if isinstance(diag, dict) else {}
        TRAIN_MSE_MEAN = float(train_stats.get('mse_mean')) if train_stats.get('mse_mean') is not None else None
        TRAIN_MSE_STD = float(train_stats.get('mse_std')) if train_stats.get('mse_std') is not None else None
        if TRAIN_MSE_MEAN is not None and TRAIN_MSE_STD is not None:
            print(f"INFO: TRAIN_MSE_MEAN={TRAIN_MSE_MEAN:.6f} TRAIN_MSE_STD={TRAIN_MSE_STD:.6f}")
        else:
            TRAIN_MSE_MEAN = None
            TRAIN_MSE_STD = None
except Exception:
    pass

# Ahora que `SEASON_TRAIN_IDS` está definido, intentar estimar `p99` desde los datos de train
try:
    p99_est = estimate_p99_from_train(df, SEASON_TRAIN_IDS, bins=64)
    if p99_est is not None:
        p99 = p99_est
        print(f"INFO: p99 estimado desde datos de entrenamiento: {p99:.6f}")
    else:
        print(f"INFO: no se pudo estimar p99 desde datos de entrenamiento; usando fallback p99={p99}")
except Exception:
    print(f"INFO: error al estimar p99; usando fallback p99={p99}")

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


def mse_to_percentile(mse, mean, std):
    """Aproxima el percentil del MSE asumiendo distribución normal con media y std del train.
    Devuelve valor en 0..100. Si mean/std no disponibles, devuelve None.
    """
    try:
        if mean is None or std is None or std <= 0:
            return None
        z = (mse - mean) / std
        # CDF normal usando erf
        cdf = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
        return float(cdf * 100.0)
    except Exception:
        return None


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
    model_info = None
    try:
        model_info = {
            "loaded": MODEL_LOADED,
            "name": modelo.name if modelo is not None else None
        }
    except Exception:
        model_info = {"loaded": False, "name": None}

    return {"status": "ok", "model": model_info}


@app.post("/api/reload_model")
def reload_model():
    """Intenta recargar el modelo desde `MODEL_PATH` en la instancia en ejecución.
    Útil para cargar pesos sin reiniciar el servidor.
    """
    global modelo, MODEL_LOADED
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=404, detail=f"MODEL_PATH no encontrado: {MODEL_PATH}")

    try:
        modelo = models.load_model(MODEL_PATH, compile=False)
        MODEL_LOADED = True
        modelo.compile(optimizer=tf.keras.optimizers.Adam(1e-4), loss="mse")
        return {"loaded": True, "method": "load_model", "name": modelo.name}
    except Exception as e1:
        try:
            modelo = models.load_model(
                MODEL_PATH,
                custom_objects={
                    'mse': tf.keras.losses.MeanSquaredError(),
                    'mae': tf.keras.metrics.MeanAbsoluteError(),
                    'mape': tf.keras.metrics.MeanAbsolutePercentageError(),
                    'cosine_similarity': tf.keras.metrics.CosineSimilarity(),
                }
            )
            MODEL_LOADED = True
            modelo.compile(optimizer=tf.keras.optimizers.Adam(1e-4), loss="mse")
            return {"loaded": True, "method": "load_model_custom", "name": modelo.name}
        except Exception:
            try:
                modelo = build_default_autoencoder()
                modelo.load_weights(MODEL_PATH)
                MODEL_LOADED = True
                modelo.compile(optimizer=tf.keras.optimizers.Adam(1e-4), loss="mse")
                return {"loaded": True, "method": "load_weights_into_fallback", "name": modelo.name}
            except Exception as e:
                MODEL_LOADED = False
                raise HTTPException(status_code=500, detail=str(e))


@app.get('/api/debug_model')
def debug_model():
    """Devuelve información sobre el path del modelo para debugging remoto."""
    try:
        models_dir = os.path.join(BASE_DIR, 'data', 'models')
        listing = []
        if os.path.exists(models_dir):
            listing = os.listdir(models_dir)
        return {
            'MODEL_PATH': MODEL_PATH,
            'model_exists': os.path.exists(MODEL_PATH),
            'models_dir': models_dir,
            'models_dir_listing': listing,
            'cwd': os.getcwd(),
            'p99_used': float(p99),
            'anomaly_threshold_used': float(ANOMALY_THRESHOLD)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@app.get("/api/unused_matches")
def get_unused_matches():
    """Devuelve partidos que pertenecen explícitamente a `SEASON_EXPLORE_IDS`.
    Esto garantiza que `explore` contenga solo las temporadas que queremos usar
    para pruebas (no entrenadas ni testeadas)."""
    explore_df = df[df['season_id'].isin(SEASON_EXPLORE_IDS)]
    match_ids = []
    for season_id, group in explore_df.groupby('season_id', sort=False):
        ids = group['match_id'].unique().tolist()
        match_ids.extend([{"match_id": int(i), "season_id": int(season_id)} for i in ids])

    return {"total": len(match_ids), "matches": match_ids}


@app.get("/api/used_data")
def get_used_data():
    """Devuelve qué `season_id` y `match_id` se usaron para train y test."""
    train_df = df[df['season_id'].isin(SEASON_TRAIN_IDS)]
    test_df = df[df['season_id'].isin(SEASON_TEST_IDS)]

    train_matches = sorted(train_df['match_id'].unique().tolist())
    test_matches = sorted(test_df['match_id'].unique().tolist())

    return {
        "season_train_ids": SEASON_TRAIN_IDS,
        "season_test_ids": SEASON_TEST_IDS,
        "train_match_count": len(train_matches),
        "test_match_count": len(test_matches),
        "train_matches_sample": train_matches[:50],
        "test_matches_sample": test_matches[:50]
    }


@app.post("/api/predict")
def predict_match(match_id: int = None, body: dict = Body(None)):
    """Predice anomalía para un partido específico.
    Acepta `match_id` como query param (`?match_id=...`) o en el body JSON `{ "match_id": ... }`.
    """
    try:
        # permitir match_id en body JSON además de query params
        if match_id is None and body and isinstance(body, dict) and 'match_id' in body:
            try:
                match_id = int(body.get('match_id'))
            except Exception:
                raise HTTPException(status_code=400, detail='match_id inválido en body')
        # Validar match_id
        if match_id is None:
            raise HTTPException(status_code=400, detail="match_id requerido")

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
        # anomaly_score: mostrar directamente el MSE (más informativo y no siempre 0)
        anomaly_score = float(mse)
        # z-score y percentil aproximado respecto a la distribución del train (si disponible)
        z_score = None
        mse_percentile = None
        anomaly_score_percentile = None
        try:
            if 'TRAIN_MSE_MEAN' in globals() and TRAIN_MSE_MEAN is not None and TRAIN_MSE_STD is not None:
                z_score = float((mse - TRAIN_MSE_MEAN) / TRAIN_MSE_STD)
                mse_percentile = mse_to_percentile(mse, TRAIN_MSE_MEAN, TRAIN_MSE_STD)
                anomaly_score_percentile = float(mse_percentile) if mse_percentile is not None else None
        except Exception:
            z_score = None
            mse_percentile = None
            anomaly_score_percentile = None
        
        # Generar imágenes
        original_img = map_to_base64_image(X_proc[0])
        reconstructed_img = map_to_base64_image(recon[0])
        comparison_img = compute_comparison_image(X_proc[0], recon[0])

        # Imagen de diferencia absoluta (heatmap) y hotspots (coords donde diff > 90pct)
        diff_map = np.abs(X_proc[0].squeeze() - recon[0].squeeze())
        diff_img = map_to_base64_image(diff_map, cmap='seismic')
        thr_hot = float(np.percentile(diff_map, 90))
        hotspots_arr = np.argwhere(diff_map > thr_hot)
        hotspots = hotspots_arr.tolist()
        # Zonas resumidas: porcentaje vertical/horizontal concentrado
        alto, ancho = diff_map.shape
        if len(hotspots_arr):
            vert_pct = 100 * (hotspots_arr[:, 0].mean() / alto)
            horiz_pct = 100 * (hotspots_arr[:, 1].mean() / ancho)
        else:
            vert_pct = None
            horiz_pct = None
        
        return {
            "match_id": match_id,
            "season_id": season_id,
            "season_name": SEASON_NAMES.get(season_id, f"Season {season_id}"),
            "mse": mse,
            "threshold": ANOMALY_THRESHOLD,
            "is_anomalous": is_anomalous,
            "anomaly_score": anomaly_score,
            "anomaly_score_percentile": anomaly_score_percentile,
            "z_score": z_score,
            "mse_percentile": mse_percentile,
            "original_image": original_img,
            "reconstructed_image": reconstructed_img,
            "comparison_image": comparison_img,
            "diff_image": diff_img,
            "hotspots": hotspots,
            "hotspot_summary": {"vertical_pct": vert_pct, "horizontal_pct": horiz_pct},
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


@app.post("/api/predict_batch")
def predict_batch(match_ids: List[int] = Body(...)):
    """Predicciones para una lista de `match_id`. Devuelve resumen por partido (mse, is_anomalous, anomaly_score)."""
    results = []
    for mid in match_ids:
        match_data = df[df['match_id'] == mid]
        if match_data.empty:
            results.append({"match_id": int(mid), "error": "not found"})
            continue

        X_raw, _ = build_heatmaps_from_df(match_data)
        if X_raw.size == 0:
            results.append({"match_id": int(mid), "error": "no heatmap"})
            continue

        X_proc = preprocess_maps(X_raw, p99=p99)
        recon = modelo.predict(X_proc, verbose=0)
        mse = float(np.mean((X_proc - recon) ** 2))
        is_anom = mse > ANOMALY_THRESHOLD
        # anomaly_score: mostrar directamente el MSE (más informativo y no siempre 0)
        anom_score = float(mse)
        z_score = None
        mse_percentile = None
        anomaly_score_percentile = None
        try:
            if 'TRAIN_MSE_MEAN' in globals() and TRAIN_MSE_MEAN is not None and TRAIN_MSE_STD is not None:
                z_score = float((mse - TRAIN_MSE_MEAN) / TRAIN_MSE_STD)
                mse_percentile = mse_to_percentile(mse, TRAIN_MSE_MEAN, TRAIN_MSE_STD)
                anomaly_score_percentile = float(mse_percentile) if mse_percentile is not None else None
        except Exception:
            z_score = None
            mse_percentile = None
            anomaly_score_percentile = None

        results.append({
            "match_id": int(mid),
            "mse": mse,
            "is_anomalous": bool(is_anom),
            "anomaly_score": float(anom_score),
            "anomaly_score_percentile": anomaly_score_percentile,
            "z_score": z_score,
            "mse_percentile": mse_percentile
        })

    return {"total": len(results), "results": results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
