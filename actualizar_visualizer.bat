@echo off
REM ===================================================================
REM Script de Actualizacion Automatica para Ontology2DB
REM Ejecutar desde la raiz del proyecto: actualizar_visualizer.bat
REM ===================================================================

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║     ACTUALIZACION DEL VISUALIZADOR - ONTOLOGY2DB          ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Verificar que estamos en el directorio correcto
if not exist "ontology2db\visualizer.py" (
    echo ❌ ERROR: No se encuentra ontology2db\visualizer.py
    echo    Asegurate de ejecutar este script desde la raiz del proyecto
    echo    Estructura esperada:
    echo      ontology2db\
    echo        ├── ontology2db\
    echo        │   └── visualizer.py
    echo        └── examples\
    pause
    exit /b 1
)

echo [✓] Directorio correcto detectado
echo.

REM ===================================================================
REM PASO 1: Verificar que el archivo tiene los cambios
REM ===================================================================
echo [1/7] Verificando que visualizer.py tiene los cambios...

findstr /C:"_format_cardinality" ontology2db\visualizer.py >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: El archivo visualizer.py NO tiene los cambios nuevos
    echo    El metodo _format_cardinality no existe
    echo.
    echo    ACCION REQUERIDA:
    echo    1. Abre ontology2db\visualizer.py
    echo    2. BORRA TODO el contenido
    echo    3. COPIA TODO el codigo del Artifact "visualizer-fixed"
    echo    4. GUARDA el archivo
    echo    5. Ejecuta este script de nuevo
    echo.
    pause
    exit /b 1
)

findstr /C:"title=tooltip" ontology2db\visualizer.py >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: El archivo tiene cambios parciales
    echo    Falta el codigo de tooltips
    echo.
    echo    ACCION REQUERIDA:
    echo    Asegurate de copiar TODO el codigo del artifact, no solo partes
    echo.
    pause
    exit /b 1
)

echo [✓] Archivo visualizer.py contiene los cambios nuevos
echo.

REM ===================================================================
REM PASO 2: Limpiar cache de Python
REM ===================================================================
echo [2/7] Limpiando cache de Python...

if exist "ontology2db\__pycache__" (
    rmdir /S /Q "ontology2db\__pycache__" 2>nul
    echo [✓] Cache de ontology2db limpiado
)

if exist "examples\__pycache__" (
    rmdir /S /Q "examples\__pycache__" 2>nul
    echo [✓] Cache de examples limpiado
)

if exist "ontology2db\ontology2db\__pycache__" (
    rmdir /S /Q "ontology2db\ontology2db\__pycache__" 2>nul
    echo [✓] Cache interno limpiado
)

del /Q "ontology2db\*.pyc" 2>nul
del /Q "examples\*.pyc" 2>nul

echo [✓] Cache de Python completamente limpiado
echo.

REM ===================================================================
REM PASO 3: Eliminar archivos generados antiguos
REM ===================================================================
echo [3/7] Eliminando archivos generados antiguos...

if exist "examples\ontology_graph.html" (
    del /Q "examples\ontology_graph.html"
    echo [✓] ontology_graph.html antiguo eliminado
)

if exist "examples\ontology_graph.png" (
    del /Q "examples\ontology_graph.png"
    echo [✓] ontology_graph.png antiguo eliminado
)

if exist "examples\generated_models.py" (
    del /Q "examples\generated_models.py"
    echo [✓] generated_models.py antiguo eliminado
)

if exist "examples\example.db" (
    del /Q "examples\example.db"
    echo [✓] example.db antiguo eliminado
)

echo [✓] Archivos antiguos eliminados
echo.

REM ===================================================================
REM PASO 4: Activar entorno virtual
REM ===================================================================
echo [4/7] Activando entorno virtual...

if not exist "venv\Scripts\activate.bat" (
    echo ❌ ERROR: No se encuentra venv\Scripts\activate.bat
    echo    El entorno virtual no existe o no esta en la ubicacion esperada
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Verificar activacion
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)

echo [✓] Entorno virtual activado
echo.

REM ===================================================================
REM PASO 5: Reinstalar el paquete
REM ===================================================================
echo [5/7] Reinstalando el paquete ontology2db...

echo    Desinstalando version anterior...
pip uninstall ontology2db -y >nul 2>&1

echo    Instalando version actualizada...
pip install -e . >nul 2>&1

REM Verificar instalacion
pip show ontology2db >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: No se pudo instalar el paquete
    echo    Intenta manualmente: pip install -e .
    pause
    exit /b 1
)

echo [✓] Paquete reinstalado correctamente
echo.

REM ===================================================================
REM PASO 6: Verificar que el codigo nuevo se cargo
REM ===================================================================
echo [6/7] Verificando que el codigo nuevo se cargo...

python -c "from ontology2db.visualizer import OntologyVisualizer; import sys; sys.exit(0 if hasattr(OntologyVisualizer, '_format_cardinality') else 1)" 2>nul

if errorlevel 1 (
    echo ❌ ERROR: El codigo nuevo NO se cargo
    echo    Python sigue usando el codigo antiguo
    echo.
    echo    Posibles causas:
    echo    1. El archivo no se guardo correctamente
    echo    2. Hay multiples instalaciones de Python
    echo.
    echo    Intenta:
    echo    pip uninstall ontology2db -y
    echo    pip install -e . --force-reinstall
    pause
    exit /b 1
)

echo [✓] Codigo nuevo cargado correctamente en Python
echo.

REM ===================================================================
REM PASO 7: Generar nueva visualizacion
REM ===================================================================
echo [7/7] Generando nueva visualizacion...

cd examples
python example.py

if not exist "ontology_graph.html" (
    echo ❌ ERROR: No se genero ontology_graph.html
    echo    Revisa los errores en la salida anterior
    cd ..
    pause
    exit /b 1
)

cd ..

echo [✓] Nueva visualizacion generada
echo.

REM ===================================================================
REM RESUMEN Y VERIFICACION
REM ===================================================================
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║              ✓ ACTUALIZACION COMPLETADA                   ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📊 RESUMEN:
echo    [✓] Archivo visualizer.py actualizado
echo    [✓] Cache de Python limpiado
echo    [✓] Archivos antiguos eliminados
echo    [✓] Paquete reinstalado
echo    [✓] Codigo nuevo verificado
echo    [✓] Nueva visualizacion generada
echo.
echo 🌐 SIGUIENTE PASO:
echo    Abre examples\ontology_graph.html en tu navegador
echo.
echo    IMPORTANTE: Abre en modo incognito o presiona Ctrl+Shift+R
echo    para evitar cache del navegador
echo.
echo 📋 VERIFICAR EN EL NAVEGADOR:
echo    1. Los nodos solo muestran el nombre (sin atributos)
echo    2. Al hacer hover sobre nodo ^→ aparece popup con atributos
echo    3. Las relaciones se ven como: [1]  writes  [0..*]
echo    4. NO deberias ver \n ni [1..0..n]
echo    5. Al hacer hover sobre flecha ^→ aparece popup
echo.

REM Preguntar si abrir el navegador
set /p "ABRIR=¿Abrir en el navegador ahora? (s/n): "
if /i "!ABRIR!"=="s" (
    echo.
    echo Abriendo en modo incognito...
    
    REM Intentar Chrome
    where chrome >nul 2>&1
    if not errorlevel 1 (
        start chrome --incognito "examples\ontology_graph.html"
        goto :navegador_abierto
    )
    
    REM Intentar Edge
    where msedge >nul 2>&1
    if not errorlevel 1 (
        start msedge -inprivate "examples\ontology_graph.html"
        goto :navegador_abierto
    )
    
    REM Intentar Firefox
    where firefox >nul 2>&1
    if not errorlevel 1 (
        start firefox -private-window "examples\ontology_graph.html"
        goto :navegador_abierto
    )
    
    REM Si ninguno funciona, abrir normalmente
    start "" "examples\ontology_graph.html"
    echo ⚠️  Se abrio en navegador normal. Presiona Ctrl+Shift+R para recargar
    
    :navegador_abierto
    echo [✓] Navegador abierto
)

echo.
echo 🎉 ¡LISTO! Verifica el grafo en el navegador
echo.
echo 🆘 Si aun ves el grafo antiguo:
echo    1. Presiona Ctrl + Shift + R en el navegador
echo    2. O cierra el navegador completamente y abre el HTML de nuevo
echo.

pause