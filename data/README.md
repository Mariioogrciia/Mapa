# data/ - Datos y Modelos

## 📁 Estructura

```
data/
├── raw/                                      # Datos sin procesar
│   └── dataset_pases_barca_historico_completo.csv
│       ├── Rows: 30,000+
│       ├── Columns: season_id, match_id, minute, player, x_inicio, y_inicio, pass_outcome
│       ├── Temporadas: 2007/2008 - 2020/2021 (14 seasons)
│       └── Peso: ~2-3 MB
│
└── models/                                   # Modelos entrenados
    └── autoencoder_barca_model.h5           # Autoencoder convolucional
        ├── Parámetros: 49,761
        ├── Input: (64, 64, 1)
        ├── Output: (64, 64, 1)
        ├── Loss: MSE
        ├── Optimizer: Adam (lr=1e-4)
        ├── Entrenado: 50 épocas
        └── Peso: ~1-2 MB
```

## 📊 Dataset

### Descripción
Barcelona pases históricos 2007-2021 con coordenadas inicio.

### Columnas
- `season_id`: Temporada (int)
- `match_id`: Partido único (int)
- `minute`: Minuto del partido (int)
- `player`: Jugador (string)
- `x_inicio`: Coordenada X inicio pase (float, 0-120)
- `y_inicio`: Coordenada Y inicio pase (float, 0-80)
- `pass_outcome`: Resultado (Successful, Unsuccessful)

### Uso en Pipeline

```python
# Carga
df = pd.read_csv("data/raw/dataset_pases_barca_historico_completo.csv")

# Separación (SIN data leakage)
train_ids = [40, 41, 21, 22, 23, 24, 26, 27]  # 2007-2017 (272 partidos)
test_ids = [2, 1, 4]                           # 2017-2019 (104 partidos)
explore_ids = [25, 42, 90]                     # 2019-2021 (99 partidos)

# Heatmaps
X = np.histogram2d(x_inicio, y_inicio, bins=64, range=[(0,120), (0,80)])
```

## 🤖 Modelo

### Arquitectura

```
Input (64, 64, 1)
    ↓
Conv2D(64) + ReLU + MaxPool(2×2)  [32×32]
    ↓
Conv2D(32) + ReLU + MaxPool(2×2)  [16×16]
    ↓
Conv2D(16) + ReLU + MaxPool(2×2)  [8×8]  ← LATENT SPACE
    ↓
UpSample(2×2) + Conv2D(16) + ReLU [16×16]
    ↓
UpSample(2×2) + Conv2D(32) + ReLU [32×32]
    ↓
UpSample(2×2) + Conv2D(64) + ReLU [64×64]
    ↓
Conv2D(1) + Sigmoid
    ↓
Output (64, 64, 1)
```

### Parámetros de Entrenamiento

```
Loss: Mean Squared Error (MSE)
Optimizer: Adam (learning_rate=1e-4)
Epochs: 50
Batch Size: 4
Validation Split: 15%
Seed: 42 (reproducibilidad)
```

### Resultados

```
Final Train Loss: 0.063352
Final Val Loss:   0.062706
→ Sin sobreajuste ✓

MSE Threshold (95%): 0.074042
Anomalías detectadas: 11/99 (11.1%)
```

## 📦 Cómo Usar

### Backend Python
```python
import tensorflow as tf

# Cargar modelo
modelo = tf.keras.models.load_model("data/models/autoencoder_barca_model.h5")

# Predicción
output = modelo.predict(X_input)
mse = np.mean((X_input - output) ** 2)
```

### FastAPI (recomendado)
```bash
POST /api/predict?match_id=123456
→ Retorna heatmaps + score + predicción
```

## 🔄 Pipeline Completo

```
Raw Datos
    ↓
Validación (columnas obligatorias)
    ↓
Separación Train/Test/Explore
    ↓
Construcción de heatmaps np.histogram2d()
    ↓
Transformación: √x
    ↓
Normalización: p99 = 1.414 (percentil 99)
    ↓
Clip: [0, 1]
    ↓
Reshape: (N, 64, 64, 1)
    ↓
Entrada a Autoencoder
    ↓
Reconstrucción
    ↓
Cálculo MSE
    ↓
Comparación vs Threshold (0.074042)
    ↓
Predicción Anomalía (Sí/No)
```

## 📝 Notas

- Los datos ya están procesados y listos para usar
- El modelo ya está entrenado (no requiere reentrenamiento)
- Las rutas se manejan automáticamente desde `backend/api.py`
- El percentil 99 (p99=1.414) está hardcodeado en todos los scripts

---

Ver documentación completa: [docs/](../docs/)
