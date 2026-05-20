# Barcelona Tactical Audit - Full Stack Deployment

## 📋 Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                   Frontend (Next.js)                        │
│              http://localhost:3000                          │
│  React + TypeScript + Tailwind CSS                          │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   Backend (FastAPI)                         │
│              http://localhost:8000                          │
│  Python + TensorFlow + Pandas + NumPy                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   Data & Models                             │
│  - CSV: dataset_pases_barca_historico_completo.csv         │
│  - Model: autoencoder_barca_model.h5                        │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Instalación y Ejecución

### 1️⃣ Backend (Python FastAPI)

```bash
# En la raíz del proyecto
cd c:\Users\Alumno_AI\Desktop\Mapa

# Activar virtual environment
.venv\Scripts\activate

# Instalar dependencias FastAPI
pip install fastapi uvicorn

# Ejecutar API
python api.py
```

API estará disponible en `http://localhost:8000`
Documentación Swagger: `http://localhost:8000/docs`

### 2️⃣ Frontend (Next.js)

```bash
# En la carpeta frontend
cd frontend

# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev
```

Frontend estará disponible en `http://localhost:3000`

## 📊 Endpoints API

### Health Check
```bash
GET http://localhost:8000/api/health
```

### Obtener Temporadas
```bash
GET http://localhost:8000/api/seasons
```

### Obtener Partidos de una Temporada
```bash
GET http://localhost:8000/api/matches?season_id=25
```

### Predecir Anomalía de un Partido
```bash
POST http://localhost:8000/api/predict?match_id=123456
```

Respuesta:
```json
{
  "match_id": 123456,
  "season_id": 25,
  "season_name": "2011/2012",
  "mse": 0.085,
  "threshold": 0.074042,
  "is_anomalous": true,
  "anomaly_score": 114.5,
  "original_image": "data:image/png;base64,...",
  "reconstructed_image": "data:image/png;base64,...",
  "comparison_image": "data:image/png;base64,...",
  "interpretation": {
    "mse_level": "Alto (anómalo)",
    "message": "Barcelona jugó de forma diferente a su patrón histórico"
  }
}
```

### Obtener Top Anomalías
```bash
GET http://localhost:8000/api/top-anomalies?limit=15&season_id=25
```

### Obtener Estadísticas
```bash
GET http://localhost:8000/api/statistics
```

## 🎯 Características

### Dashboard Principal
- ✅ Selector de partidos por temporada
- ✅ Búsqueda por Match ID
- ✅ Visualización de heatmaps (Original, Reconstruido, Comparación)
- ✅ Score de anomalía con barra de progreso
- ✅ Indicador visual de anomalía (rojo/verde)
- ✅ Mensaje interpretativo táctico

### Rankings
- ✅ Top 15 partidos más anómalos
- ✅ Tabla interactiva con scores
- ✅ Filtros por temporada
- ✅ Descarga de imágenes

### Estadísticas
- ✅ Distribución del dataset (Train/Test/Explore)
- ✅ Información arquitectónica del modelo
- ✅ Detalles técnicos (filtros, optimizador, etc.)
- ✅ Explicación paso a paso del sistema

## 🎨 Diseño

**Colores**:
- Rojo Barcelona: `#cb3b0c`
- Amarillo Barcelona: `#ffc600`
- Fondo oscuro: `#0f1419`

**Componentes**:
- Cards con efecto glass
- Botones con hover rojo
- Iconos de Lucide
- Gráficos responsive
- Animaciones sutiles

## 📱 Responsiveness

- Desktop: Grid 3 columnas
- Tablet: Grid 2 columnas
- Mobile: Stack vertical con scroll

## 🔧 Variables de Entorno

Frontend (`.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Backend (Python):
- `CSV_PATH`: Ruta al dataset
- `MODEL_PATH`: Ruta al modelo HDF5
- `ANOMALY_THRESHOLD`: 0.074042 (percentil 95 del train)

## 🚀 Deployment

### Deploy en Vercel (Frontend)
```bash
cd frontend
vercel deploy
```

### Deploy en Heroku/Railway (Backend)
```bash
# Crear Dockerfile para API
# Configurar variables de entorno
# Push a Heroku/Railway
```

## 📚 Documentación Interactiva

- API Docs: `http://localhost:8000/docs` (Swagger UI)
- ReDoc: `http://localhost:8000/redoc`

## 🐛 Troubleshooting

**Frontend no conecta con API**:
```bash
# Verificar que FastAPI está corriendo
curl http://localhost:8000/api/health

# Verificar variable de entorno
echo $NEXT_PUBLIC_API_URL
```

**Error en predicción**:
```bash
# Verificar que el modelo existe
ls -la autoencoder_barca_model.h5

# Verificar que el CSV está cargado
ls -la dataset_pases_barca_historico_completo.csv
```

**Puerto ya en uso**:
```bash
# Cambiar puerto FastAPI
python api.py --port 8001

# Cambiar puerto Next.js
npm run dev -- -p 3001
```

## 📞 Support

Para problemas o preguntas:
1. Revisa los logs de FastAPI: `http://localhost:8000/docs`
2. Revisa la consola del navegador (F12)
3. Verifica conectividad de red: `ping localhost:8000`

---

**Made with ❤️ for Barcelona Tactical Analysis**
