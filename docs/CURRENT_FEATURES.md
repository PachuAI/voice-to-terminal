# Funcionalidades Actuales - Voice-to-Terminal v1.0

## 🎯 Descripción General

Voice-to-Terminal es un asistente de voz especializado para desarrolladores que trabajan con Claude Code. Convierte comandos de voz en texto y los copia automáticamente al clipboard para uso inmediato en Claude Code u otros editores.

## 🚀 Funcionalidades Core

### 1. Reconocimiento de Voz Offline
- **Motor**: OpenAI Whisper con faster-whisper
- **Idioma**: Español optimizado
- **Calidad**: Offline, sin dependencia de internet después de instalación
- **Modelos disponibles**: Base (74MB) y Small (244MB)

### 2. Detección Automática de Voz (VAD)
- **Funcionalidad**: Detecta automáticamente cuándo empiezas y paras de hablar
- **Pre-buffer**: Captura 1 segundo previo para no perder palabras iniciales
- **Acumulación inteligente**: Mantiene múltiples segmentos de voz separados por pausas
- **Configuración**: Umbral 500, pausa de 1.5s, detección mínima 100ms

### 3. Sistema de Control Avanzado
- **Hotkey global**: Ctrl+L para activar/desactivar (evita conflictos con terminal)
- **Modo Manual**: Space para grabar mientras se mantiene presionado
- **Modo Speak**: 's' para grabación continua con VAD automático
- **Procesamiento**: Enter para transcribir y copiar todo lo acumulado
- **Salida**: 'q' para cerrar la aplicación

### 4. Integración Automática con Clipboard
- **Auto-copia**: Transcripción automática al clipboard
- **Notificación visual**: Muestra el texto copiado en terminal
- **Integración**: Ctrl+V directo en Claude Code o cualquier editor
- **Buffer flush**: Optimizado para mostrar resultados inmediatamente

## 🔧 Características Técnicas

### Configuración de Audio Optimizada
```
- Formato: 16-bit PCM
- Canales: Mono
- Frecuencia: 16kHz (óptima para reconocimiento de voz)
- Buffer: 1024 samples por chunk
```

### Threading Architecture
- **Hilo principal**: Manejo de controles de teclado
- **Hilo de grabación**: Captura continua de audio sin bloqueos
- **Hilo de procesamiento**: Transcripción asíncrona

### Optimizaciones de Performance
- **Whisper config**: beam_size=1, temperatura=0.0, sin timestamps
- **Memoria**: Gestión automática de archivos temporales
- **CPU**: Compute_type="int8" para máxima eficiencia

## 📊 Comparativa de Modelos

### Whisper Base (voicebase.py)
- **Tamaño**: 74MB
- **Velocidad**: 3-4 segundos
- **Precisión**: ~92%
- **RAM**: ~200MB
- **Uso ideal**: Desarrollo diario, comandos frecuentes
- **Ventajas**: Rápido, eficiente, bajo uso de recursos

### Whisper Small (voicesmall.py)
- **Tamaño**: 244MB  
- **Velocidad**: 5-8 segundos
- **Precisión**: ~94%
- **RAM**: ~400MB
- **Uso ideal**: Documentación técnica, términos específicos
- **Ventajas**: Mayor precisión, mejor con terminología técnica

## 🎮 Flujos de Uso

### Flujo Típico - Modo Manual
1. Ejecutar `voicebase` desde cualquier terminal
2. Presionar Ctrl+L para activar
3. Mantener Space y hablar
4. Soltar Space para transcribir
5. Texto aparece en terminal y se copia automáticamente
6. Ctrl+V en Claude Code

### Flujo Avanzado - Modo Speak
1. Ejecutar `voicesmall` para mayor precisión
2. Presionar Ctrl+L para activar
3. Presionar 's' para modo speak continuo
4. Hablar libremente (pausas automáticas detectadas)
5. Hablar más (se acumula con lo anterior)
6. Presionar Enter para procesar todo lo acumulado
7. Ctrl+V en Claude Code

### Flujo de Desarrollo con Cursor/VS Code
1. Abrir Cursor en proyecto de desarrollo
2. Terminal separada: `voicebase`
3. Ctrl+L para activar asistente
4. Desarrollar normalmente en Cursor
5. Cuando necesites dictar: Space + hablar
6. Ctrl+V inmediato en Cursor
7. Continuar desarrollo sin interrupciones

## 🛡️ Características de Seguridad

### Control de Estado
- **Estado desactivado**: Ignora todas las teclas excepto Ctrl+L
- **Activación explícita**: Usuario controla cuándo está escuchando
- **Terminal separada**: No interfiere con el desarrollo principal
- **Sin persistencia**: No guarda audio ni transcripciones

### Gestión de Archivos
- **Archivos temporales**: Eliminación automática después de procesamiento
- **Memoria**: Liberación automática de buffers de audio
- **Modelos**: Descarga única, almacenamiento local

## 🚀 Instalación y Configuración

### Instalación Local
```bash
git clone https://github.com/PachuAI/voice-to-terminal.git
cd voice-to-terminal
pip install -r requirements.txt
python voicebase.py
```

### Instalación Global (Recomendado)
```bash
# Los scripts .bat ya están incluidos
# Funcionan globalmente desde cualquier carpeta
voicebase    # Desde cualquier terminal
voicesmall   # Desde cualquier terminal
```

## 📈 Casos de Uso Reales

### 1. Desarrollo de Código
- **Escenario**: Dictando funciones complejas a Claude Code
- **Modelo**: Small para términos técnicos precisos
- **Ventaja**: No interrumpe el flujo de pensamiento

### 2. Documentación Técnica
- **Escenario**: Escribiendo README o comentarios extensos
- **Modelo**: Small para terminología específica
- **Ventaja**: Velocidad de dictado vs escritura manual

### 3. Debugging Rápido
- **Escenario**: Comandos cortos y frecuentes
- **Modelo**: Base para respuesta inmediata
- **Ventaja**: Interacción fluida sin delays

### 4. Revisión de Código
- **Escenario**: Comentarios y sugerencias de refactoring
- **Modelo**: Base para feedback rápido
- **Ventaja**: Comentarios más naturales y detallados

## 🔮 Estado de Desarrollo

### ✅ Completado (v1.0)
- Reconocimiento de voz offline con 2 modelos
- VAD optimizado con pre-buffer
- Sistema de controles completo
- Integración automática con clipboard
- Instalación global
- Documentación completa

### 🚧 En Planificación
- Interfaz gráfica para configuración
- Métricas de precisión en tiempo real
- Soporte multi-idioma
- Integración directa con editores
- Configuración personalizable de VAD
- Comandos de voz (no solo dictado)

## 🎯 Filosofía de Diseño

### Principios Core
1. **Simplicidad**: Controles intuitivos, setup mínimo
2. **Performance**: Optimizado para uso diario sin lag
3. **Confiabilidad**: Offline, sin dependencias externas
4. **Flexibilidad**: Múltiples modelos según necesidad
5. **Integración**: Funciona con cualquier editor/terminal

### Target User
- **Desarrolladores**: Que usan Claude Code frecuentemente
- **Content Creators**: Documentando procesos de desarrollo
- **Educators**: Enseñando programación en vivo
- **Accessibility**: Usuarios que prefieren voz sobre teclado

---

**Esta documentación refleja el estado actual (v1.0) del proyecto. Para roadmap futuro y planes de desarrollo, ver próximos documentos de planificación.**