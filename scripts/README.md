# scripts/ - Scripts Utilitarios

## 📁 Contenido

```
scripts/
├── SETUP.bat                   # Setup automático Windows
├── SETUP.sh                    # Setup automático Unix/Mac
└── README.md                   # Este archivo
```

## ⚙️ Setup Automático

### Windows
```bash
scripts/SETUP.bat
```

Esto:
1. Imprime instrucciones de instalación
2. Sugiere comandos para ejecutar backend y frontend
3. Proporciona URLs de acceso

### Unix/Mac
```bash
bash scripts/SETUP.sh
```

Mismo comportamiento que Windows pero para sistemas Unix.

## 🛠️ Scripts Disponibles

### SETUP.bat / SETUP.sh
- **Propósito**: Guía interactiva de instalación
- **Uso**: Ejecuta una vez para ver instrucciones
- **Salida**: Pasos numerados para setup completo

## 🚀 Uso Típico

```bash
# 1. Clone/descarga el proyecto
git clone ... && cd Mapa

# 2. Ejecuta setup (te dará instrucciones)
scripts/SETUP.bat        # Windows
# o
bash scripts/SETUP.sh    # Unix/Mac

# 3. Sigue los pasos impresos en la consola
# Resultado: Backend y Frontend corriendo
```

## 📝 Scripts Futuros

- `train_model.py` - Reentrenamiento del autoencoder
- `export_data.py` - Exportación de resultados
- `validate_data.py` - Validación del dataset
- `benchmark.py` - Performance testing

---

Ver más: [docs/](../docs/)
