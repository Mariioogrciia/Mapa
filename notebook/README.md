# Barcelona Tactical Audit - Notebook

Análisis completo de la detección de anomalías tácticas con autoencoder.

## 📊 Contenido

```
notebook/
├── entrenamiento.ipynb       # Pipeline completo (39 celdas)
└── README.md                 # Este archivo
```

## 🎯 Estructura del Notebook

1. **Carga y separación** - Train/Test/Explore sin data leakage
2. **Diagnóstico de datos** - Estadísticas de mapas de calor
3. **Arquitectura** - Autoencoder convolucional (49,761 parámetros)
4. **Entrenamiento** - 50 épocas, batch_size=4
5. **Auditoría táctica** - Resultados en test set
6. **Métricas ampliadas** - Distribuciones y rankings
7. **Comparación Train/Test** - Validación de diferencias
8. **Análisis Explore** - Detección de anomalías en temporadas nuevas
9. **Orientación del campo** - Determinación de ataques (izq/der)

## 📈 Resultados Clave

- **Partidos entrenamiento**: 272 (2007-2017)
- **Partidos test**: 104 (2017-2019)
- **Partidos exploración**: 99 (2019-2021)
- **Anomalías detectadas**: 11/99 (11.1%)
- **Umbral 95%**: MSE = 0.074042
- **Cambio máximo**: 23.9% en distribución de pases

## 🔍 Análisis

### Normalización
```
√x → percentil 99 (p99=1.414) → clip [0,1]
```

### Modelo
```
Input: 64×64×1 heatmaps
Encoder: Conv2D(64→32→16) + MaxPool
Latent: Compressed representation
Decoder: UpSample + Conv2D(16→32→64)
Output: 64×64×1 reconstruction
```

### Interpretación
- Barcelona ataca hacia la **DERECHA** (más pases allí)
- Izquierda = Portería propia
- Derecha = Portería enemiga
- Cambio principal en zona atacante (derecha) en 2019-2021

## ▶️ Ejecutar

```bash
# Abrir en Jupyter
jupyter notebook entrenamiento.ipynb

# O usar VS Code
# Abre el archivo y ejecuta las celdas una por una
```

## 📚 Más Info

Ver documentación: [docs/](../docs/)
