@echo off
echo 🚀 Barcelona Tactical Audit - Full Stack Setup
echo ==============================================
echo.

REM 1. Backend Setup
echo 📦 Backend Setup (FastAPI)...
echo.
echo Instala dependencias:
echo   pip install -r requirements_api.txt
echo.
echo Inicia FastAPI:
echo   python api.py
echo.
echo La API estará disponible en http://localhost:8000
echo Documentación Swagger: http://localhost:8000/docs
echo.

REM 2. Frontend Setup
echo ⚡ Frontend Setup (Next.js)...
echo.
echo Navega a la carpeta frontend:
echo   cd frontend
echo.
echo Instala dependencias:
echo   npm install
echo.
echo Inicia desarrollo:
echo   npm run dev
echo.
echo El dashboard estará disponible en http://localhost:3000
echo.

echo ==============================================
echo ✅ Abre dos terminales y ejecuta:
echo.
echo Terminal 1 (Backend):
echo   python api.py
echo.
echo Terminal 2 (Frontend):
echo   cd frontend ^&^& npm install ^&^& npm run dev
echo.
echo ==============================================
