@echo off
cd /d "%~dp0streamlit_app"
echo Iniciando DataTrust... se abrira solo en el navegador en unos segundos.
echo NO CIERRES ESTA VENTANA mientras quieras seguir viendo la app.
echo Para apagarlo, cierra esta ventana o pulsa Ctrl+C.
echo.
"C:\Users\Massiel\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m streamlit run app.py
pause
