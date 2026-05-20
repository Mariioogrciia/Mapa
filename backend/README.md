# Barcelona Tactical Audit - Backend

API REST para análisis táctico automático con autoencoder.

## 📁 Contenido

```
backend/
├── api.py                    # Servidor FastAPI (305 líneas)
├── requirements.txt          # Dependencias Python
└── README.md                 # Este archivo
```

## 🚀 Inicio Rápido

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar API
python api.py

# Acceder a Swagger UI
http://localhost:8000/docs
```

## 🔌 Endpoints Disponibles

```bash
GET  /api/health              # Health check
GET  /api/seasons             # Obtener temporadas
GET  /api/matches             # Obtener partidos
POST /api/predict             # Predicción de anomalía
GET  /api/top-anomalies       # Top 15 anomalías
GET  /api/statistics          # Estadísticas
```

## ⚙️ Configuración

Las rutas a datos y modelos se buscan automáticamente:
- CSV: `../data/raw/dataset_pases_barca_historico_completo.csv`
- Model: `../data/models/autoencoder_barca_model.h5`

## 📚 Más Info

Ver documentación completa en [docs/](../docs/)
