# 🔴⚽ Barcelona Tactical Audit

**Advanced Autoencoder Anomaly Detection for Football Tactical Analysis**

Detección automática de desviaciones tácticas del FC Barcelona usando autoencoder convolucional. Dashboard moderno con React + Next.js y API REST con FastAPI.

---

## 📁 Estructura del Proyecto

```
Mapa/
├── frontend/                          # 🎨 Next.js + React UI
│   ├── app/
│   │   ├── page.tsx                   # Dashboard principal
│   │   ├── layout.tsx                 # Wrapper global
│   │   └── globals.css                # Estilos
│   ├── components/                    # Componentes React
│   │   ├── Header.tsx
│   │   ├── MatchSelector.tsx
│   │   ├── AnomalyScore.tsx
│   │   ├── HeatmapViewer.tsx
│   │   ├── TopAnomalies.tsx
│   │   └── Statistics.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── README.md
│
├── backend/                           # ⚙️ FastAPI Python API
│   ├── api.py                         # Servidor principal (305 líneas)
│   ├── requirements.txt               # Dependencias Python
│   └── README.md
│
├── notebook/                          # 📊 Análisis y entrenamiento
│   ├── entrenamiento.ipynb            # Pipeline completo (39 celdas)
│   └── README.md
│
├── data/                              # 💾 Datos y modelos
│   ├── raw/
│   │   └── dataset_pases_barca_historico_completo.csv  (30,000+ registros)
│   └── models/
│       └── autoencoder_barca_model.h5 (Modelo entrenado, 49,761 parámetros)
│
├── docs/                              # 📚 Documentación
│   ├── QUICK_START.md                 # Guía rápida
│   ├── DEPLOYMENT.md                  # Documentación completa
│
├── scripts/                           # 🛠️ Scripts utilitarios
│   ├── SETUP.bat                      # Setup para Windows
│   ├── SETUP.sh                       # Setup para Unix
│   └── README.md
│
├── .gitignore                         # Archivos ignorados
└── README.md                          # Este archivo
├── .gitignore                         # Archivos ignorados
└── README.md                          # Este archivo
```

---

## 🚀 Inicio Rápido

### Opción 1: Automático (Windows)
```bash
scripts/SETUP.bat
```

### Opción 2: Dos Terminales

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
python api.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 🌐 Acceso

| Componente | URL | Puerto |
|-----------|-----|--------|
| **Dashboard** | http://localhost:3000 | 3000 |
| **API** | http://localhost:8000 | 8000 |
| **Swagger Docs** | http://localhost:8000/docs | 8000 |
| **ReDoc** | http://localhost:8000/redoc | 8000 |

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│             Frontend (React + Next.js 14)                   │
│            http://localhost:3000                            │
│         TypeScript + Tailwind CSS + Lucide Icons            │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST (axios)
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Backend (FastAPI + Python)                     │
│            http://localhost:8000                            │
│     TensorFlow + Pandas + NumPy + Matplotlib                │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│            Data & Models (data/)                            │
│  - CSV: 30,000+ pases del Barcelona 2007-2021              │
│  - Model: Autoencoder convolucional (64×64×1 → 64×64×1)    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Requisitos

- **Python 3.9+** (para backend)
- **Node.js 18+** (para frontend)
- **npm** o **yarn**
- **TensorFlow 2.15+**
- **Next.js 14+**

---

## 📊 Features

### Dashboard Principal
- ✅ Selector interactivo de partidos por temporada
- ✅ Búsqueda por Match ID
- ✅ Visualización de heatmaps (Original | Reconstruido | Comparación)
- ✅ Score de anomalía con barra de progreso
- ✅ Indicadores visuales animados
- ✅ Descargar imágenes en PNG

### Ranking de Anomalías
- ✅ Top 15 partidos más anómalos
- ✅ Tabla interactiva sorteable
- ✅ Filtros por temporada
- ✅ Scores normalizados (0-100%)

### Estadísticas
- ✅ Distribución del dataset (Train/Test/Explore)
- ✅ Información arquitectónica del modelo
- ✅ Detalles técnicos y parámetros
- ✅ Explicación paso a paso del sistema

---

## 🎨 Diseño

**Colores Barcelona:**
- 🔴 Rojo: `#cb3b0c`
- 🟡 Amarillo: `#ffc600`
- ⚫ Negro: `#0f1419`
- 🟠 Naranja: `#ff4d00`

**Responsive:** Mobile → Tablet → Desktop

---

## 📡 API Endpoints

```bash
# Health Check
GET /api/health

# Temporadas
GET /api/seasons

# Partidos
GET /api/matches?season_id=25

# Predicción (Main)
POST /api/predict?match_id=123456

# Top Anomalías
GET /api/top-anomalies?limit=15

# Estadísticas
GET /api/statistics
```

Ver documentación completa en la carpeta `docs/`

---

## 📚 Documentación

- **[QUICK_START.md](docs/QUICK_START.md)** - Guía rápida de inicio
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Documentación técnica completa
- **Notebook**: ver [notebook/README.md](notebook/README.md) para el análisis y entrenamiento

> Nota: la referencia de API y la documentación de arquitectura se añadirán próximamente en la carpeta `docs/`.

---

## 🔬 Modelo & Datos

### Autoencoder Convolucional
- **Input**: Heatmaps 64×64 de pases normalizados
- **Encoder**: Conv2D (64→32→16 filtros) + MaxPooling
- **Latent**: Representación comprimida
- **Decoder**: UpSampling + Conv2D (16→32→64 filtros)
- **Output**: Heatmap reconstruido 64×64×1
- **Parámetros**: 49,761
- **Loss**: MSE
- **Optimizer**: Adam (lr=1e-4)

### Dataset
- **Partidos**: 475 (históricos 2007-2017 + test 2017-2019)
- **Pases**: 30,000+ registros
- **Temporadas**: 14 (2007/2008 a 2020/2021)
- **Split**: Train (272) | Test (104) | Explore (99)

### Normalización
```
1. Raíz cuadrada: √x
2. Percentil 99: p99 = 1.414
3. Clip: [0, 1]
4. Reshape: (N, 64, 64, 1)
```

---

## 🎯 Flujo de Uso

1. **Abre http://localhost:3000** en el navegador
2. **Selecciona temporada** (ej: 2011/2012)
3. **Busca partido** (por Match ID o lista)
4. **Sistema procesa**:
   - Genera heatmap 64×64
   - Normaliza con √x y p99
   - Pasa por autoencoder
   - Calcula MSE de reconstrucción
5. **Visualiza resultados**:
   - 🔴 Anomaly Score (0-100%)
   - 📊 Tres heatmaps (Original | Reconstruido | Comparación)
   - 📝 Interpretación táctica

---

## 🧪 Testing

```bash
# Backend health check
curl http://localhost:8000/api/health

# Obtener temporadas
curl http://localhost:8000/api/seasons

# Predecir partido
curl -X POST "http://localhost:8000/api/predict?match_id=123456"
```

---

## 🐛 Troubleshooting

### Puerto 8000 en uso
```bash
# Cambiar puerto en backend/api.py (última línea):
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Puerto 3000 en uso
```bash
npm run dev -- -p 3001
```

### API no conecta
```bash
# Verificar que FastAPI está corriendo:
curl http://localhost:8000/api/health

# Verificar logs del servidor
# Verificar CORS en DevTools (F12)
```

### Modelo no carga
```bash
# Verificar archivo existe:
ls data/models/autoencoder_barca_model.h5

# Reinstalar TensorFlow:
pip install --upgrade tensorflow
```

---

## 📦 Dependencias Principales

### Backend
```
fastapi==0.104.1
uvicorn==0.24.0
tensorflow==2.15.0
numpy==2.4.6
pandas==2.1.3
matplotlib==3.10.9
```

### Frontend
```
next==14.0.0
react==18.2.0
typescript==5.3.0
tailwindcss==3.3.0
axios==1.6.0
lucide-react==0.294.0
```

---

## 🚀 Deployment

### Vercel (Frontend)
```bash
cd frontend
vercel deploy
```

### Railway/Heroku (Backend)
```bash
# Crear Dockerfile
# Configurar variables de entorno
# Deploy
```

---

## 📞 Soporte

Para problemas:
1. Revisa `docs/DEPLOYMENT.md`
2. Consulta `docs/API.md` para endpoints
3. Verifica logs: `http://localhost:8000/docs`
4. Abre DevTools: F12 → Network/Console

---

## 📜 Licencia

Proyecto académico para análisis táctico del FC Barcelona.

---

## 👨‍💻 Desarrollado con

- 🤖 **TensorFlow/Keras** - Machine Learning
- ⚡ **FastAPI** - Backend moderno
- ⚛️ **React 18** - UI moderna
- 🎨 **Tailwind CSS** - Styling
- 📊 **Matplotlib/NumPy** - Visualización

---

**Made with ❤️ for Barcelona Tactical Analysis**

```
   ___  ____  ___  ________
  / _ )/ __ \/   |/ ____/  |
 / _  / / / / /| / /   / /|
/ __  / /_/ / ___ / /___/ ___ 
/_/ |_/\____/_/  |_\____/_/  |_|

⚽ TACTICAL AUDIT SYSTEM ⚽
```
