# Instalación Global - Voice-to-Terminal

## 🌐 Ejecutar desde cualquier carpeta

### Opción 1: Scripts .bat (RECOMENDADO - Windows)

1. **Copiar scripts al PATH del sistema:**
```cmd
# Copiar a una carpeta que esté en PATH (ej: C:\Windows\System32)
copy "C:\voice-assistant\voicebase.bat" "C:\Windows\System32\"
copy "C:\voice-assistant\voicesmall.bat" "C:\Windows\System32\"
```

2. **Usar desde cualquier terminal:**
```cmd
# Desde cualquier carpeta:
voicebase    # Inicia modelo base
voicesmall   # Inicia modelo small
```

### Opción 2: Agregar carpeta al PATH

1. **Agregar C:\voice-assistant al PATH:**
   - Win + R → `sysdm.cpl` → Avanzado → Variables de entorno
   - En "Variables del sistema" → PATH → Editar
   - Agregar: `C:\voice-assistant`

2. **Usar desde cualquier terminal:**
```cmd
voicebase.bat    # Desde cualquier carpeta
voicesmall.bat   # Desde cualquier carpeta
```

### Opción 3: Alias en PowerShell

1. **Crear perfil de PowerShell:**
```powershell
# Verificar si existe perfil
Test-Path $PROFILE

# Si no existe, crearlo
New-Item -Path $PROFILE -Type File -Force

# Editar perfil
notepad $PROFILE
```

2. **Agregar al perfil:**
```powershell
# Agregar estas líneas al perfil
function voicebase { 
    Set-Location "C:\voice-assistant"
    python voicebase.py 
}

function voicesmall { 
    Set-Location "C:\voice-assistant"
    python voicesmall.py 
}
```

3. **Recargar perfil:**
```powershell
. $PROFILE
```

### Opción 4: Scripts Python con entry points

1. **Crear setup.py:**
```python
from setuptools import setup

setup(
    name="voice-to-terminal",
    version="1.0.0",
    py_modules=["voicebase", "voicesmall"],
    entry_points={
        'console_scripts': [
            'voicebase=voicebase:main',
            'voicesmall=voicesmall:main',
        ],
    },
)
```

2. **Instalar globalmente:**
```cmd
pip install -e .
```

## 🎯 Recomendación

Para tu caso de uso (desarrollo de contenido con Cursor):

1. **Usar Opción 1** (.bat en System32) - Más simple
2. **Terminal separada siempre** - No interfiere con el desarrollo
3. **Hotkey Ctrl+L** - Control total sobre cuándo está activo

## 📋 Uso Típico

```cmd
# En Cursor/VS Code:
cd mi-proyecto-react

# En terminal separada (desde cualquier lugar):
voicebase

# Ctrl+L para activar
# Hablar → ENTER → Ctrl+V en Cursor
```

## 🔧 Troubleshooting

- **"No se reconoce el comando"**: Verificar PATH o ubicación del .bat
- **Python no encontrado**: Verificar instalación de Python en PATH
- **Permisos**: Ejecutar terminal como administrador para copiar a System32