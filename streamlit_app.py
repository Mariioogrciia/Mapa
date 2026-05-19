import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.models import load_model

sns.set_theme(style="whitegrid")

@st.cache_data
def load_dataset(path="dataset_pases_barca_historico_completo.csv"):
    df = pd.read_csv(path)
    return df

@st.cache_data
def build_heatmaps_from_df(dataframe, bins=64, x_range=(0, 120), y_range=(0, 80)):
    heatmaps = []
    match_ids = []
    season_map = []
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
        season_map.append(match_df["season_id"].iloc[0])
    if not heatmaps:
        return np.empty((0, bins, bins), dtype=np.float32), [], []
    return np.stack(heatmaps, axis=0), match_ids, season_map

@st.cache_data
def load_model_safe(path="autoencoder_barca_model.h5"):
    try:
        m = load_model(path)
        return m
    except Exception as e:
        st.error(f"No se pudo cargar el modelo: {e}")
        return None

def preprocess_maps(maps_raw, p99=None):
    proc = np.sqrt(maps_raw)
    if p99 is None:
        p99 = float(np.percentile(proc, 99)) if proc.size>0 else 1.0
        if p99<=0:
            p99 = 1.0
    proc = np.clip(proc / p99, 0.0, 1.0).astype(np.float32)
    proc = proc[..., np.newaxis]
    return proc, p99

def show_heatmaps(original, reconstructed, title_orig="Original", title_recon="Reconstruido"):
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    axes[0].imshow(original.squeeze(), cmap='inferno', origin='lower', vmin=0, vmax=1)
    axes[0].set_title(title_orig)
    axes[0].axis('off')
    axes[1].imshow(reconstructed.squeeze(), cmap='inferno', origin='lower', vmin=0, vmax=1)
    axes[1].set_title(title_recon)
    axes[1].axis('off')
    st.pyplot(fig)

# --- Streamlit UI ---
st.title("Auditoría táctica - Autoencoder de mapas de pases (FC Barcelona)")
st.markdown("Cargue el dataset y el modelo entrenado para evaluar partidos individuales y detectar anomalías tácticas.")

# Load data and model
with st.spinner("Cargando dataset..."):
    df = load_dataset()

with st.spinner("Construyendo mapas..."):
    X_all_raw, all_match_ids, all_seasons = build_heatmaps_from_df(df)

model = load_model_safe()

# Compute train p99 and threshold using the same train seasons as notebook
season_train_ids = [41, 21, 22, 23, 24, 26, 27, 2, 1, 4]
train_df = df[df["season_id"].isin(season_train_ids)]
X_train_raw, train_match_ids, train_seasons = build_heatmaps_from_df(train_df)
if X_train_raw.size==0:
    st.warning("No se pudieron generar mapas de entrenamiento para calcular p99/umbral.")

X_train_proc, p99 = preprocess_maps(X_train_raw)
# compute reconstructions on train to set threshold
if model is not None and X_train_proc.size>0:
    recon_train = model.predict(X_train_proc, verbose=0)
    mse_train = np.mean((X_train_proc - recon_train)**2, axis=(1,2,3))
    anomaly_threshold = float(np.percentile(mse_train, 95))
else:
    anomaly_threshold = None

st.sidebar.header("Selector de partido")
season_selected = st.sidebar.selectbox("Season", sorted(df["season_id"].unique()))
match_options = df[df["season_id"]==season_selected]["match_id"].unique().tolist()
match_selected = st.sidebar.selectbox("Match ID", match_options)

if st.sidebar.button("Evaluar partido seleccionado"):
    # Build heatmap for this match
    match_df = df[df["match_id"]==match_selected]
    if match_df.empty:
        st.warning("No hay datos para ese match_id.")
    else:
        hist, _, _ = build_heatmaps_from_df(match_df)
        if hist.size==0:
            st.warning("No se pudo construir el mapa para ese partido.")
        else:
            X_raw = hist
            X_proc, _ = preprocess_maps(X_raw, p99=p99)
            if model is None:
                st.error("Modelo no cargado. Coloca `autoencoder_barca_model.h5` en la carpeta.")
            else:
                recon = model.predict(X_proc, verbose=0)
                mse = float(np.mean((X_proc - recon)**2))
                mae = float(np.mean(np.abs(X_proc - recon)))
                st.subheader(f"Resultados para match_id {match_selected} (season {season_selected})")
                st.write(f"MSE = {mse:.8f}")
                st.write(f"MAE = {mae:.8f}")
                if anomaly_threshold is not None:
                    st.write(f"Umbral 95% (train) = {anomaly_threshold:.8f}")
                    st.write("Etiqueta: ", "ANÓMALO" if mse>anomaly_threshold else "NORMAL")
                show_heatmaps(X_proc[0], recon[0])

st.sidebar.markdown("---")
if st.sidebar.button("Mostrar ranking de test (mayor MSE)"):
    # compute reconstructions for all matches and ranking
    if model is None:
        st.error("Modelo no cargado.")
    else:
        X_all_proc, _ = preprocess_maps(X_all_raw, p99=p99)
        if X_all_proc.size==0:
            st.warning("No hay mapas disponibles para evaluar.")
        else:
            recon_all = model.predict(X_all_proc, verbose=0)
            mse_all = np.mean((X_all_proc - recon_all)**2, axis=(1,2,3))
            df_ranking = pd.DataFrame({"match_id": all_match_ids, "season_id": all_seasons, "mse": mse_all})
            df_ranking = df_ranking.sort_values("mse", ascending=False).reset_index(drop=True)
            st.dataframe(df_ranking.head(20))

st.sidebar.markdown("---")
st.sidebar.write("p99 usado para normalización (train): ")
st.sidebar.write(f"{p99:.6f}" if p99 is not None else "n/a")
if anomaly_threshold is not None:
    st.sidebar.write("Umbral 95% train:")
    st.sidebar.write(f"{anomaly_threshold:.6f}")

st.markdown("---")
st.markdown("**Notas:** Asegúrate de tener `autoencoder_barca_model.h5` y `dataset_pases_barca_historico_completo.csv` en la carpeta del proyecto.")
