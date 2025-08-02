# Voice-to-Terminal 🎤➡️🖥️

**Asistente de voz para Claude Code** - Convierte tu voz en texto y lo copia automáticamente al clipboard para usar con Claude Code sin necesidad de escribir.

## 🚀 Inicio Rápido

```bash
# Modelo balanceado (recomendado)
python voicebase.py

# Modelo de alta precisión
python voicesmall.py
```

## 🎯 Características

- **🎤 Reconocimiento de voz offline** con Whisper
- **🔄 Detección automática de voz (VAD)** - no pierde palabras
- **📋 Integración directa con clipboard** - Ctrl+V en Claude
- **⚡ Dos modelos optimizados**: Base (rápido) y Small (preciso)
- **🎮 Controles intuitivos**: Ctrl+L para activar, Space para hablar

## 📊 Comparativa de Modelos

| Modelo | Tamaño | Velocidad | Precisión | Uso Recomendado |
|--------|--------|-----------|-----------|------------------|
| **Base** | 74MB | ~3-4s | ~92% | Uso general, balance velocidad/precisión |
| **Small** | 244MB | ~5-8s | ~94% | Máxima precisión, términos técnicos |

## 🎮 Controles

### Activación
- **Ctrl+L** - Activar/Desactivar script

### Cuando está activado
- **Space** - Modo manual (mantener para hablar)
- **S** - Modo speak continuo
- **Enter** - Procesar y copiar (en modo speak)
- **Q** - Salir

## ⚙️ Instalación

1. **Clonar repositorio:**
```bash
git clone https://github.com/PachuAI/voice-to-terminal.git
cd voice-to-terminal
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Ejecutar:**
```bash
# Desde la carpeta del proyecto:
python voicebase.py  # Modelo base
python voicesmall.py # Modelo small

# O instalar globalmente (recomendado):
# Ver INSTALL_GLOBAL.md para instalación global
```

4. **Uso global (opcional):**
```bash
# Después de instalación global, desde cualquier carpeta:
voicebase    # Modelo base
voicesmall   # Modelo small
```

## 🔧 Requisitos

- Python 3.7+
- Micrófono funcional
- Windows/Linux/MacOS
- Conexión a internet (solo primera descarga de modelos)

## 📁 Estructura del Proyecto

```
voice-to-terminal/
├── voicebase.py          # Modelo Whisper Base (balance)
├── voicesmall.py         # Modelo Whisper Small (precisión)
├── voicebase.bat         # Script global Windows (base)
├── voicesmall.bat        # Script global Windows (small)
├── requirements.txt      # Dependencias Python
├── docs/                # Documentación detallada
│   ├── TECHNICAL_GUIDE.md    # Guía técnica completa
│   └── CURRENT_FEATURES.md   # Funcionalidades actuales
├── INSTALL_GLOBAL.md     # Instalación global
├── whisper_models/      # Modelos descargados (auto-generado)
└── README.md           # Este archivo
```

## 🛠️ Desarrollo

Este proyecto está diseñado para **crear contenido educativo** sobre desarrollo de herramientas de IA. 

### Próximas funcionalidades planificadas:
- 🎨 Interfaz gráfica mejorada
- 🔧 Configuración personalizable
- 📊 Métricas de precisión en tiempo real
- 🌐 Soporte multi-idioma
- 🎯 Integración con más editores

## 📺 Contenido y Tutoriales

Este proyecto forma parte de una serie de contenido sobre **desarrollo de herramientas de IA**. Todos los videos y tutoriales estarán disponibles en:

- 📹 **YouTube**: [Próximamente]
- 📝 **Blog**: [Próximamente]
- 🐦 **Twitter**: [@PachuAI](https://twitter.com/PachuAI)

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Este es un proyecto educativo perfecto para aprender sobre:

- Procesamiento de audio
- Machine Learning con Whisper
- Desarrollo de herramientas CLI
- Integración con APIs

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles.

## 🙏 Reconocimientos

- **OpenAI Whisper** - Motor de reconocimiento de voz
- **faster-whisper** - Implementación optimizada
- **Claude Code** - Inspiración y caso de uso principal

---

**¿Te gusta el proyecto? ⭐ Dale una estrella y sígueme para más herramientas de IA!**