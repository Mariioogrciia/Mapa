# Barcelona Tactical Audit - Frontend

Frontend moderno con **Next.js 14**, **React 18** y **Tailwind CSS** para análisis táctico de Barcelona.

## 🚀 Inicio Rápido

### Instalación

```bash
cd frontend
npm install
```

### Desarrollo

```bash
npm run dev
```

Accede a `http://localhost:3000`

### Build

```bash
npm run build
npm start
```

## 📁 Estructura

```
frontend/
├── app/
│   ├── layout.tsx          # Layout principal
│   ├── page.tsx            # Dashboard principal
│   ├── globals.css         # Estilos globales
│   └── not-found.tsx       # Página 404
├── components/
│   ├── Header.tsx          # Encabezado
│   ├── MatchSelector.tsx   # Selector de partidos
│   ├── AnomalyScore.tsx    # Indicador de anomalía
│   ├── HeatmapViewer.tsx   # Visualizador de heatmaps
│   ├── TopAnomalies.tsx    # Ranking de anomalías
│   └── Statistics.tsx      # Estadísticas
├── tailwind.config.js
├── postcss.config.js
├── tsconfig.json
└── next.config.js
```

## 🎨 Diseño

- **Color scheme**: Rojo y amarillo (Barcelona)
- **Dark mode**: Tema oscuro profesional
- **Responsive**: Mobile-friendly
- **Componentes**: Botones, cards, gráficos interactivos

## 🔗 API Integration

La aplicación se conecta a la API FastAPI en `http://localhost:8000`:

- `GET /api/seasons` - Obtener temporadas
- `GET /api/matches` - Obtener partidos
- `POST /api/predict` - Predicción de partido
- `GET /api/top-anomalies` - Top anomalías
- `GET /api/statistics` - Estadísticas

## 📦 Dependencias Principales

- **next**: Framework React moderno
- **axios**: Cliente HTTP
- **recharts**: Gráficos y visualizaciones
- **lucide-react**: Iconos
- **tailwindcss**: Utility-first CSS

## 🛠️ Variables de Entorno

Crea un archivo `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```
