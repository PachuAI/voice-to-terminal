# Guía Técnica - Voice-to-Terminal

## 🏗️ Arquitectura del Sistema

### Componentes Principales

1. **Motor de Reconocimiento**: Whisper (faster-whisper)
2. **Detección de Voz**: VAD (Voice Activity Detection) personalizado
3. **Gestión de Audio**: PyAudio para captura en tiempo real
4. **Control de Estado**: Keyboard para hotkeys globales
5. **Integración**: Pyperclip para clipboard automático

### Flujo de Procesamiento

```
Audio Input → Pre-buffer → VAD Detection → Audio Accumulation → Whisper Processing → Clipboard Copy
```

## 🔧 Configuración Técnica

### Parámetros de Audio
```python
# Configuración optimizada para reconocimiento de voz
chunk = 1024              # Tamaño de buffer por lectura
format = pyaudio.paInt16  # 16-bit PCM
channels = 1              # Mono
rate = 16000             # 16kHz (óptimo para speech)
```

### Configuración VAD
```python
voice_threshold = 500      # Umbral de detección de voz
silence_duration = 1.5     # Segundos de silencio para pausa
min_speech_duration = 0.1  # Mínima duración para detectar voz
pre_buffer_duration = 1.0  # Buffer previo para capturar inicio
```

### Configuración Whisper
```python
# Base Model
model = WhisperModel(
    "base",                    # 74MB, balance velocidad/precisión
    device="cpu",              
    compute_type="int8",       # Optimización máxima
    beam_size=1,              # Velocidad sobre precisión
    temperature=0.0,          # Determinístico
    language="es"             # Español fijo
)

# Small Model  
model = WhisperModel(
    "small",                   # 244MB, mayor precisión
    # ... mismos parámetros optimizados
)
```

## 🧠 Algoritmo VAD (Voice Activity Detection)

### Funcionamiento

1. **Pre-buffer Circular**: Mantiene 1 segundo de audio previo
2. **Detección por RMS**: Calcula energía del audio en tiempo real
3. **Umbral Adaptativo**: 500 como valor base optimizado
4. **Estados de Transición**:
   - `silence` → `voice`: Incluye pre-buffer
   - `voice` → `silence`: Mantiene grabación por 1.5s
   - `silence` larga: Para grabación, mantiene frames

### Código Clave
```python
def detect_voice_level(self, data):
    """Detecta el nivel de audio para VAD"""
    rms = audioop.rms(data, 2)  # RMS del audio
    return rms

# En el loop principal:
if voice_level > self.voice_threshold:
    # Voz detectada
    if not self.is_speaking:
        # Primera detección: incluir pre-buffer
        self.frames = self.pre_buffer.copy()
    self.frames.append(data)
else:
    # Silencio: contar chunks silenciosos
    if self.is_speaking:
        self.silence_chunks += 1
        if self.silence_chunks >= max_silence_chunks:
            # Pausa larga: detener grabación, mantener frames
            self.is_speaking = False
```

## 🎛️ Sistema de Control

### Hotkeys Globales
- **Ctrl+L**: Toggle activación (evita conflictos con terminal)
- **Space**: Modo manual (mientras se mantiene presionado)
- **S**: Toggle modo speak continuo
- **Enter**: Procesar audio acumulado (en modo speak)
- **Q**: Salir del programa

### Estados del Sistema
1. **Desactivado**: Ignora todas las teclas excepto Ctrl+L
2. **Manual**: Graba mientras Space está presionado
3. **Speak**: Grabación continua con VAD automático

## 🚀 Optimizaciones de Performance

### Whisper Optimizations
```python
# Configuración para máxima velocidad
segments, info = model.transcribe(
    audio_file,
    beam_size=1,               # Mínimo beam search
    best_of=1,                 # Un solo intento
    patience=1.0,              # Mínima paciencia
    without_timestamps=True,   # Sin timestamps = más rápido
    word_timestamps=False,     # Sin word timing
    vad_filter=False          # VAD interno desactivado
)
```

### Threading Strategy
- **Main Thread**: Manejo de keyboard input
- **Recording Thread**: Captura de audio continua
- **Processing Thread**: Transcripción asíncrona

### Memory Management
- Archivos temporales automáticamente eliminados
- Buffers limitados en tamaño
- Garbage collection de objetos PyAudio

## 📊 Comparativa de Modelos

### Whisper Base vs Small

| Aspecto | Base | Small |
|---------|------|-------|
| **Archivo** | 74MB | 244MB |
| **RAM** | ~200MB | ~400MB |
| **Latencia** | 3-4s | 5-8s |
| **Precisión** | ~92% | ~94% |
| **Términos técnicos** | Buena | Excelente |
| **Puntuación** | Básica | Mejorada |

### Casos de Uso Recomendados

**Base (voicebase.py)**:
- Uso general diario
- Comandos cortos y frecuentes
- Prioridad en velocidad
- Hardware limitado

**Small (voicesmall.py)**:
- Transcripción de código técnico
- Documentación detallada
- APIs y nombres específicos
- Máxima precisión requerida

## 🐛 Troubleshooting

### Problemas Comunes

1. **Audio no se detecta**:
   - Verificar micrófono en sistema
   - Ajustar `voice_threshold` (reducir valor)
   - Comprobar `pyaudio` instalación

2. **Texto no aparece en terminal**:
   - Problema de buffering resuelto con `flush=True`
   - Verificar que `pyperclip` funcione

3. **Modelos no descargan**:
   - Verificar conexión internet
   - Crear carpeta `whisper_models/` manualmente
   - Verificar permisos de escritura

4. **Performance lenta**:
   - Usar modelo Base en lugar de Small
   - Verificar CPU usage
   - Cerrar aplicaciones innecesarias

### Debug Mode
```python
# Agregar prints para debugging
print(f"Voice level: {voice_level}, Threshold: {self.voice_threshold}")
print(f"Recording: {self.is_speaking}, Frames: {len(self.frames)}")
```

## 🔮 Roadmap Técnico

### V2.0 Planificado
- [ ] Configuración GUI para ajustar VAD
- [ ] Soporte multi-idioma dinámico
- [ ] Métricas de precisión en tiempo real
- [ ] Integración con más editores
- [ ] API REST para integración externa

### V2.1 Futuro
- [ ] Modelo custom fine-tuned para términos de programación
- [ ] Corrección automática de términos técnicos
- [ ] Integración con LSP para autocompletado contextual
- [ ] Soporte para comandos de voz (no solo dictado)

## 📈 Métricas y Benchmarks

### Tests de Precisión
Ver `TESTS_PRECISION.md` para casos de prueba estandarizados y resultados de benchmarks comparativos entre modelos.

### Performance Benchmarks
- **Latencia media Base**: 3.2s ± 0.8s
- **Latencia media Small**: 6.1s ± 1.2s
- **Precisión técnica Base**: 87% en términos de programación
- **Precisión técnica Small**: 93% en términos de programación