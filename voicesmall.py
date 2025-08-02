import keyboard
import threading
import time
import os
import sys
import pyperclip
import pyaudio
import wave
import tempfile
from faster_whisper import WhisperModel
import audioop

class WhisperSmallVoice:
    def __init__(self):
        # Estados del programa
        self.activated = False
        self.speak_mode = False
        self.accumulated_text = ""
        
        # Configuración de audio optimizada
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.frames = []
        self.continuous_recording = False
        self.recording_thread = None
        
        # Configuración VAD (Voice Activity Detection)
        self.voice_threshold = 500  # Umbral más sensible
        self.silence_duration = 1.5  # Pausa más corta
        self.min_speech_duration = 0.1  # Solo 100ms para detectar ⚡
        self.pre_buffer_duration = 1.0  # Buffer de 1s antes de detectar voz
        self.is_speaking = False
        self.silence_chunks = 0
        self.speech_chunks = 0
        self.pre_buffer = []  # Buffer circular para capturar inicio
        
        # Configurar Whisper Base
        self.setup_whisper_small()
        
        print("=" * 70)
        print("  VOICE TO CLAUDE - WHISPER SMALL + VAD")
        print("=" * 70)
        print("🔴 DESACTIVADO - El script ignora todas las teclas")
        print("")
        print("🎯 MODELO: Whisper Small (244MB)")
        print("⚡ VELOCIDAD: ~5-8s (más lento)")
        print("🎯 PRECISIÓN: ~94% (mayor precisión + puntuación)")
        print("🎤 VAD: Detección inteligente de voz (no pierde palabras)")
        print("📱 OFFLINE: Sin internet requerido")
        print("")
        print("PARA ACTIVAR:")
        print("• Presiona Ctrl+L para ACTIVAR/DESACTIVAR el script")
        print("")
        print("CUANDO ESTÉ ACTIVADO (🟢):")
        print("• SPACE = Modo manual (mantener para hablar)")
        print("• 's' = Modo speak persistente")
        print("• ENTER = Copiar en modo speak")
        print("• 'q' = Salir del programa")
        print("")
        print("🔴 Inicia DESACTIVADO - Ctrl+L para activar")
        print("=" * 70)
    
    def setup_whisper_small(self):
        """Configura Whisper Small para máxima velocidad"""
        try:
            print("🔄 Cargando Whisper Small...")
            
            # Configuración optimizada para balance
            self.model = WhisperModel(
                "small",                    # 🎯 Modelo small - mayor precisión
                device="cpu",               # CPU compatible
                compute_type="int8",        # 🚀 Máxima optimización
                download_root="./whisper_models",
                num_workers=1,              # 🚀 Minimal overhead
                cpu_threads=1               # 🚀 Un solo thread = más rápido
            )
            
            print("✅ Whisper Small cargado correctamente")
            print("🚀 Optimizado para velocidad máxima")
            print("🎯 Incluye puntuación automática")
            
        except Exception as e:
            print(f"❌ Error cargando Whisper Small: {e}")
            print("💡 Intenta: pip install faster-whisper")
            sys.exit(1)
    
    def transcribe_audio_small(self, audio_file):
        """Transcribe con Whisper Small ultra-optimizado"""
        try:
            start_time = time.time()
            print(f"🔄 Transcribiendo con Whisper Small...")
            
            # Configuración para máxima velocidad
            segments, info = self.model.transcribe(
                audio_file,
                language="es",              # Español fijo
                beam_size=1,               # 🚀 Beam mínimo = más rápido
                temperature=0.0,           # Determinístico
                best_of=1,                 # 🚀 Un solo intento
                patience=1.0,              # 🚀 Mínima paciencia
                length_penalty=1.0,        # Sin penalties complejos
                repetition_penalty=1.0,    
                no_repeat_ngram_size=0,    # 🚀 Sin filtros pesados
                suppress_blank=True,       
                suppress_tokens=[-1],      
                without_timestamps=True,   # 🚀 Sin timestamps = más rápido
                max_initial_timestamp=0.0,
                word_timestamps=False,     # 🚀 Sin word timing
                prepend_punctuations="\"'([{", 
                append_punctuations="\"')]}.,!?;:",
                vad_filter=False           # 🚀 Sin VAD para velocidad
            )
            
            # Combinar texto
            text = ""
            for segment in segments:
                text += segment.text
            
            elapsed = time.time() - start_time
            print(f"⚡ Transcrito en {elapsed:.2f}s", flush=True)
            
            return text.strip()
            
        except Exception as e:
            print(f"❌ Error transcribiendo: {e}")
            return None
    
    def save_audio_to_file(self, frames):
        """Guarda audio de manera eficiente"""
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_filename = temp_file.name
            
            with wave.open(temp_filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(frames))
            
            return temp_filename
            
        except Exception as e:
            print(f"❌ Error guardando audio: {e}")
            return None
    
    def copy_text(self, text):
        """Copia texto al clipboard"""
        try:
            pyperclip.copy(text)
            print(f"\n✅ COPIADO: {text}", flush=True)
            print("📋 Ctrl+V en Claude", flush=True)
            print("-" * 50, flush=True)
            # Forzar actualización de terminal
            import sys
            sys.stdout.flush()
        except Exception as e:
            print(f"❌ Error copiando: {e}", flush=True)
    
    def copy_and_clear_accumulated(self):
        """Copia texto acumulado y lo borra"""
        if self.accumulated_text.strip():
            self.copy_text(self.accumulated_text.strip())
            self.accumulated_text = ""
            return True
        return False
    
    def show_status(self):
        """Muestra el estado actual"""
        if not self.activated:
            status = "🔴 DESACTIVADO"
            commands = "Ctrl+L para activar"
        elif self.speak_mode:
            status = "🟢 ACTIVADO - 🗣️ MODO SPEAK (WHISPER SMALL)"
            commands = "ENTER=copiar | 's'=salir speak | Ctrl+L=desactivar"
        else:
            status = "🟢 ACTIVADO - 🎤 MANUAL (WHISPER SMALL)"
            commands = "SPACE=hablar | 's'=speak | 'q'=salir | Ctrl+L=desactivar"
        
        print(f"\n{status}")
        print(f"🎯 Modelo: Whisper Small (mayor precisión + puntuación)")
        print(f"Comandos: {commands}")
        print("-" * 50)
    
    def record_audio_quick(self, max_duration=15):
        """Grabación rápida y eficiente"""
        try:
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            self.frames = []
            self.is_recording = True
            
            print(f"🎤 Grabando... (máx {max_duration}s)")
            print("-" * 40)
            
            start_time = time.time()
            
            while (self.is_recording and 
                   time.time() - start_time < max_duration):
                
                try:
                    data = self.stream.read(self.chunk, exception_on_overflow=False)
                    self.frames.append(data)
                    
                    # Progreso simple
                    elapsed = time.time() - start_time
                    print(f"\r⏱️ {elapsed:.1f}s", end="", flush=True)
                    
                    # Condiciones de parada
                    if self.speak_mode:
                        if not self.speak_mode:
                            break
                    else:
                        if not keyboard.is_pressed('space') or not self.activated:
                            break
                
                except Exception as e:
                    print(f"\nError: {e}")
                    break
            
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            self.is_recording = False
            
            duration = len(self.frames) * self.chunk / self.rate
            print(f"\n📁 Audio: {duration:.1f}s")
            return len(self.frames) > 8  # Mínimo para procesar
            
        except Exception as e:
            print(f"❌ Error grabando: {e}")
            return False
    
    def process_audio_small(self, for_speak_mode=False):
        """Procesa audio con Whisper Small"""
        if not self.frames:
            print("❌ No hay audio")
            return
        
        duration = len(self.frames) * self.chunk / self.rate
        if duration < 0.5:
            print("⚠️ Audio muy corto")
            return
        
        print(f"⚡ Procesando {duration:.1f}s con Whisper Small...")
        
        # Guardar audio
        audio_file = self.save_audio_to_file(self.frames)
        if not audio_file:
            return
        
        # Transcribir
        text = self.transcribe_audio_small(audio_file)
        
        # Limpiar
        try:
            os.unlink(audio_file)
        except:
            pass
        
        if text and len(text.strip()) > 1:
            if for_speak_mode:
                self.accumulated_text += text + " "
                print(f"➕ Agregado: {text}")
                print(f"📝 Total: {self.accumulated_text}")
            else:
                self.copy_text(text)
        else:
            print("⚠️ No se transcribió texto válido")
    
    def detect_voice_level(self, data):
        """Detecta el nivel de audio para VAD"""
        try:
            rms = audioop.rms(data, 2)  # RMS del audio
            return rms
        except:
            return 0
    
    def start_continuous_recording(self):
        """Inicia grabación continua con VAD (Voice Activity Detection)"""
        def record_continuously():
            try:
                self.stream = self.audio.open(
                    format=self.format,
                    channels=self.channels,
                    rate=self.rate,
                    input=True,
                    frames_per_buffer=self.chunk
                )
                
                self.frames = []
                self.continuous_recording = True
                self.is_speaking = False
                self.silence_chunks = 0
                self.speech_chunks = 0
                self.pre_buffer = []
                
                chunks_per_second = self.rate // self.chunk
                max_silence_chunks = int(self.silence_duration * chunks_per_second)
                min_speech_chunks = int(self.min_speech_duration * chunks_per_second)
                pre_buffer_chunks = int(self.pre_buffer_duration * chunks_per_second)
                
                print("🎤 VAD optimizado - Buffer de pre-grabación activo")
                print("🔇 Esperando voz... (captura palabras completas)")
                
                while self.continuous_recording and self.speak_mode and self.activated:
                    try:
                        data = self.stream.read(self.chunk, exception_on_overflow=False)
                        
                        # Detectar nivel de voz
                        voice_level = self.detect_voice_level(data)
                        
                        # Mantener buffer circular pre-grabación
                        self.pre_buffer.append(data)
                        if len(self.pre_buffer) > pre_buffer_chunks:
                            self.pre_buffer.pop(0)  # Mantener solo último segundo
                        
                        if voice_level > self.voice_threshold:
                            # Hay voz
                            self.silence_chunks = 0
                            self.speech_chunks += 1
                            
                            if not self.is_speaking and self.speech_chunks >= min_speech_chunks:
                                # ⚡ EMPEZAR A GRABAR INCLUYENDO PRE-BUFFER
                                self.is_speaking = True
                                # 🔧 ACUMULAR en lugar de sobrescribir
                                if len(self.frames) == 0:
                                    # Primera detección: incluir pre-buffer
                                    self.frames = self.pre_buffer.copy()
                                    print(f"\n🗣️ Voz detectada - Grabando (con pre-buffer)...")
                                else:
                                    # Continuación: NO sobrescribir frames existentes
                                    print(f"\n🗣️ Voz continúa - Acumulando...")
                            
                            if self.is_speaking:
                                self.frames.append(data)
                                
                                # Mostrar duración total acumulada cada segundo
                                if len(self.frames) % chunks_per_second == 0:
                                    duration = len(self.frames) / chunks_per_second
                                    print(f"\r🎤 Grabando... {duration:.1f}s total acumulado (ENTER=procesar todo)", end="", flush=True)
                        
                        else:
                            # Silencio
                            self.speech_chunks = 0
                            
                            if self.is_speaking:
                                self.silence_chunks += 1
                                
                                # Si hay mucho silencio, parar grabación PERO mantener frames
                                if self.silence_chunks >= max_silence_chunks:
                                    print(f"\n⏸️ Pausa detectada - Audio acumulado ({len(self.frames)/chunks_per_second:.1f}s)")
                                    self.is_speaking = False
                                    self.silence_chunks = 0
                                    
                                    # Mostrar estado de espera - frames se mantienen para acumular
                                    print("🔇 Esperando más voz... (ENTER=procesar todo acumulado)")
                                else:
                                    # Seguir grabando durante pausa corta
                                    if self.is_speaking:
                                        self.frames.append(data)
                            else:
                                # Mostrar que está esperando voz
                                if len(self.frames) == 0:  # Solo si no hay audio acumulado
                                    if (self.silence_chunks % (chunks_per_second * 3)) == 0:  # Cada 3s
                                        print(f"\r🔇 Esperando voz... (nivel: {voice_level})", end="", flush=True)
                    
                    except Exception as e:
                        print(f"\nError grabando: {e}")
                        break
                
                if self.stream:
                    self.stream.stop_stream()
                    self.stream.close()
                    self.stream = None
                
            except Exception as e:
                print(f"❌ Error en grabación continua: {e}")
        
        # Ejecutar en hilo separado
        self.recording_thread = threading.Thread(target=record_continuously)
        self.recording_thread.daemon = True
        self.recording_thread.start()
    
    def stop_continuous_recording(self):
        """Para grabación continua"""
        self.continuous_recording = False
        if self.recording_thread:
            self.recording_thread.join(timeout=2)
        
        # Procesar audio final si hay algo
        if self.frames:
            print("\n💾 Procesando audio final...")
            self.process_and_copy_current_audio()
    
    def process_and_copy_current_audio(self):
        """Procesa audio actual, copia y reinicia grabación"""
        if not self.frames:
            print("⚠️ No hay audio para procesar")
            return
        
        # Copiar frames actuales
        current_frames = self.frames.copy()
        
        # Reiniciar frames para continuar grabando
        self.frames = []
        
        # Procesar en hilo separado para no bloquear grabación
        def process_async():
            # Crear archivo temporal
            audio_file = self.save_audio_to_file(current_frames)
            if audio_file:
                text = self.transcribe_audio_small(audio_file)
                try:
                    os.unlink(audio_file)
                except:
                    pass
                
                if text and text.strip():
                    self.copy_text(text.strip())
                    print("\n🎤 Continuando grabación... (ENTER=copiar)", end="", flush=True)
                else:
                    print("\n⚠️ No se transcribió texto")
        
        process_thread = threading.Thread(target=process_async)
        process_thread.daemon = True
        process_thread.start()
    
    def start_manual_mode(self):
        """Modo manual con Whisper Small"""
        if not self.activated or self.speak_mode:
            return
        
        success = self.record_audio_quick(max_duration=60)
        
        if success:
            self.process_audio_small(for_speak_mode=False)
        else:
            print("❌ No se grabó suficiente audio")
    
    def start_listening(self):
        """Loop principal"""
        
        try:
            while True:
                if keyboard.is_pressed('ctrl+l'):
                    self.activated = not self.activated
                    self.show_status()
                    
                    while keyboard.is_pressed('ctrl+l'):
                        time.sleep(0.1)
                
                if self.activated:
                    
                    if keyboard.is_pressed('s'):
                        if not self.speak_mode:
                            # Activar modo speak
                            self.speak_mode = True
                            print("\n🗣️ MODO SPEAK ACTIVADO")
                            print("Habla libremente - ENTER para copiar y continuar")
                            print("-" * 50)
                            
                            # Empezar grabación continua
                            self.start_continuous_recording()
                            
                            while keyboard.is_pressed('s'):
                                time.sleep(0.1)
                        else:
                            # Salir de modo speak
                            print("\n🔄 Saliendo de modo speak...")
                            self.stop_continuous_recording()
                            
                            self.speak_mode = False
                            self.show_status()
                            
                            while keyboard.is_pressed('s'):
                                time.sleep(0.1)
                    
                    elif keyboard.is_pressed('enter') and self.speak_mode:
                        # En modo speak: procesar TODO lo acumulado hasta ahora
                        duration = len(self.frames) / (self.rate // self.chunk) if self.frames else 0
                        print(f"\n⚡ Procesando {duration:.1f}s de audio acumulado...")
                        self.process_and_copy_current_audio()
                        
                        while keyboard.is_pressed('enter'):
                            time.sleep(0.1)
                    
                    elif keyboard.is_pressed('space') and not self.speak_mode:
                        # Modo manual
                        manual_thread = threading.Thread(target=self.start_manual_mode)
                        manual_thread.start()
                        manual_thread.join()
                        
                        self.show_status()
                    
                    elif keyboard.is_pressed('q'):
                        print("\n👋 Saliendo...")
                        break
                
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            print("\n👋 Saliendo...")
        finally:
            if self.stream:
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                except:
                    pass
            self.audio.terminate()

if __name__ == "__main__":
    voice = WhisperSmallVoice()
    voice.start_listening()