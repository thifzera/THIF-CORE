@echo off
setlocal
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Falha na instalacao das dependencias.
    exit /b 1
)
echo Dependencias instaladas com sucesso.
