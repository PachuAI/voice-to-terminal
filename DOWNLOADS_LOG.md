# 📁 Registro de Descargas - Voice Assistant

## 🗂️ Modelos y Archivos Descargados

### ✅ VOSK (en uso)
- **vosk-model-small-es-0.42/** (~40MB) - Modelo actual
- **vosk-model-large-es-0.22/** (~1.8GB) - ✅ **DESCARGADO** Modelo mejorado

### 🗑️ WHISPER (lento - candidato a eliminar)
- **whisper_models/** (~769MB) - Modelos faster-whisper
  - Ubicación: `./whisper_models/`
  - Estado: Funciona pero muy lento (15-20s)

### 📦 DEPENDENCIAS INSTALADAS

#### En Uso Activo:
- `vosk` - Motor principal
- `pyaudio` - Captura audio
- `keyboard` - Hotkeys
- `pyperclip` - Auto-copia
- `rich` - UI mejorada (futuro)

#### Instaladas pero No Usadas:
- `RealtimeSTT` - Conflictos con numpy ❌
- `faster-whisper` - Funciona pero lento ❌
- `SpeechRecognition` - Solo para backup
- `textual` - UI avanzada (futuro)

## 🎯 Stack Final Propuesto:
```
CORE: Vosk Large + PyAudio + Keyboard + PyPerclip
UI: Rich (para dashboard futuro)
BACKUP: SpeechRecognition (solo emergencias)
```

## 🗑️ Para Eliminar Después:
1. `whisper_models/` carpeta completa
2. `vosk-model-small-es-0.42/` (reemplazar por large)
3. Archivos: `voice_faster_whisper*.py`
4. Dependencias: `RealtimeSTT`, `faster-whisper`

## 📊 Espacio Total:
- **Actual:** ~850MB (small + whisper)
- **Final:** ~1.8GB (solo large)
- **Ahorro:** Eliminar ~800MB de Whisper