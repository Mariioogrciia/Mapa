# 🚀 Barcelona Tactical Audit - Quick Start

## ¿Qué acabo de crear?

### 📦 Backend API (FastAPI)
- **Archivo**: `api.py` (305 líneas)
- **Tecnología**: Python + FastAPI + TensorFlow
- **Puerto**: 8000
- **Endpoints**:
  - `GET /api/health` - Health check
  - `GET /api/seasons` - Obtener temporadas
  - `GET /api/matches` - Obtener partidos
  - `POST /api/predict` - Predicción de anomalía
  - `GET /api/top-anomalies` - Top 15 anomalías
  - `GET /api/statistics` - Estadísticas del dataset

### 🎨 Frontend Dashboard (Next.js 14)
- **Carpeta**: `frontend/`
- **Tecnología**: React + TypeScript + Tailwind CSS
- **Puerto**: 3000
- **Diseño**: Rojo y amarillo (Barcelona), tema oscuro profesional
- **Componentes**:
  - `Header` - Encabezado con información
  - `MatchSelector` - Selector interactivo de partidos
  - `AnomalyScore` - Indicador de anomalía con animaciones
  - `HeatmapViewer` - Visualizador de mapas de calor
  - `TopAnomalies` - Ranking de 15 anomalías
  - `Statistics` - Estadísticas y arquitectura del modelo

---

## 📋 Setup Paso a Paso

### 1️⃣ Backend (FastAPI)

```bash
# Instalar dependencias (si aún no las tienes)
pip install -r requirements_api.txt

# Ejecutar API en puerto 8000
python api.py
```

✅ Verifica en: `http://localhost:8000/docs` (Swagger UI)

### 2️⃣ Frontend (Next.js)

```bash
# Navegar a carpeta frontend
cd frontend

# Instalar dependencias (primera vez)
npm install

# Ejecutar en desarrollo
npm run dev
```

✅ Accede a: `http://localhost:3000`

---

## 🎯 Flujo de Uso

### Dashboard Principal
1. **Selecciona temporada** → Se cargan los partidos
2. **Busca por Match ID** → Filtra partidos
3. **Haz click en un partido** → Se envía a API
4. **Visualiza resultados**:
   - 🔴 **Anomaly Score** - Porcentaje de anomalía
   - 📊 **Heatmaps** - Original, Reconstruido, Comparación
   - 📝 **Interpretación** - Mensaje táctico

### Tabs Adicionales
- **Top Anomalías** - Ranking de 15 partidos más raros
- **Estadísticas** - Info del dataset y arquitectura del modelo

---

## 🎨 Diseño Visual

### Colores Barcelona
```
- Rojo principal: #cb3b0c
- Amarillo: #ffc600
- Fondo oscuro: #0f1419
- Accento naranja: #ff4d00
```

### Efectos
- ✨ Animaciones pulse en anomalías
- 🎨 Gradient backgrounds
- 🔘 Botones con hover rojo
- 📊 Barra de progreso de anomalía

---

## 📊 Estructura de Archivos

```
Mapa/
├── api.py                          # FastAPI backend (NUEVO)
├── frontend/                       # Next.js frontend (NUEVO)
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx               # Dashboard principal
│   │   ├── globals.css            # Estilos globales
│   │   └── not-found.tsx
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── MatchSelector.tsx
│   │   ├── AnomalyScore.tsx
│   │   ├── HeatmapViewer.tsx
│   │   ├── TopAnomalies.tsx
│   │   └── Statistics.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── .env.local
├── DEPLOYMENT.md                   # Documentación completa (NUEVO)
├── SETUP.bat                       # Script de setup Windows (NUEVO)
├── SETUP.sh                        # Script de setup Unix (NUEVO)
├── requirements_api.txt            # Dependencias FastAPI (NUEVO)
├── entrenamiento.ipynb             # Notebook original
├── autoencoder_barca_model.h5      # Modelo entrenado
├── dataset_pases_barca_historico_completo.csv
├── streamlit_app.py                # (Se puede eliminar si usas solo Next.js)
└── ...
```

---

## 🔗 API Endpoints Completos

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Obtener Temporadas
```bash
curl http://localhost:8000/api/seasons
```

**Respuesta:**
```json
{
  "seasons": [
    {
      "id": 40,
      "name": "2013/2014",
      "matches": 38,
      "type": "train"
    },
    ...
  ]
}
```

### Obtener Partidos
```bash
curl http://localhost:8000/api/matches?season_id=25
```

### Predicción de Partido
```bash
curl -X POST http://localhost:8000/api/predict?match_id=123456
```

**Respuesta:**
```json
{
  "match_id": 123456,
  "season_name": "2011/2012",
  "mse": 0.085,
  "is_anomalous": true,
  "anomaly_score": 114.5,
  "original_image": "data:image/png;base64,...",
  "comparison_image": "data:image/png;base64,...",
  "interpretation": {
    "message": "Barcelona jugó diferente a su patrón histórico"
  }
}
```

### Top Anomalías
```bash
curl http://localhost:8000/api/top-anomalies?limit=15
```

### Estadísticas
```bash
curl http://localhost:8000/api/statistics
```

---

## 🚀 Comandos Rápidos

### Opción 1: Scripts automatizados
```bash
# Windows
SETUP.bat

# Linux/Mac
bash SETUP.sh
```

### Opción 2: Dos terminales

**Terminal 1 (Backend):**
```bash
python api.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm install
npm run dev
```

### Opción 3: VS Code (Recomendado)

1. **Abre 2 terminales integrados** (Ctrl+`)
2. **Terminal 1**: `python api.py`
3. **Terminal 2**: `cd frontend && npm install && npm run dev`

---

## ✨ Características Implementadas

- ✅ **Arquitectura moderna**: FastAPI + Next.js
- ✅ **TypeScript**: Type-safe en frontend
- ✅ **Responsive**: Mobile, tablet, desktop
- ✅ **Animaciones**: Smooth transitions y pulses
- ✅ **Dark mode**: Tema oscuro profesional
- ✅ **API REST**: Endpoints completos
- ✅ **Visualización**: Heatmaps en base64
- ✅ **Scores**: Indicadores visuales de anomalía
- ✅ **Tablas**: Ranking interactivo
- ✅ **Estadísticas**: Info completa del dataset

---

## 🐛 Troubleshooting

### Puerto 8000 ya en uso (Backend)
```bash
# Cambiar puerto en api.py (última línea):
uvicorn.run(app, host="0.0.0.0", port=8001)

# O desde línea de comandos:
python api.py --port 8001
```

### Port 3000 ya en uso (Frontend)
```bash
npm run dev -- -p 3001
```

### API no responde
```bash
# Verifica que FastAPI está corriendo:
curl http://localhost:8000/api/health

# Verifica CORS en navegador:
# Abre DevTools (F12) → Console → Network
```

### No se cargan imágenes de heatmaps
```bash
# Verifica que matplotlib está instalado:
pip install matplotlib seaborn

# Reinicia FastAPI:
python api.py
```

---

## 📚 Documentación Adicional

- Documentación completa: Ver `DEPLOYMENT.md`
- Frontend: Ver `frontend/README.md`
- Notebook análisis: Ver `entrenamiento.ipynb`

---

## 🎬 Próximos Pasos

1. **Ejecuta backend y frontend** 📡
2. **Selecciona un partido** 🎯
3. **Analiza heatmaps** 📊
4. **Explora anomalías** 🔴
5. **Comparte resultados** 🚀

---

**Made with ❤️ for Barcelona Tactical Analysis**

Enjoy! 🚀⚽
