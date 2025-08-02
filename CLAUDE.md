# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Voice-to-Text Assistant** specifically designed for interacting with Claude Code via voice commands. The main goal is to enable users to speak their prompts instead of typing them, with automatic transcription and clipboard copying for seamless integration with Claude Code sessions.

## Core Architecture

### Voice Recognition Engines
The project experiments with multiple speech-to-text engines, each with different trade-offs:

1. **Vosk** (Primary) - Offline, fast, moderate accuracy
2. **Google Speech Recognition** - Online, good accuracy, includes punctuation
3. **Whisper/faster-whisper** - Offline, high accuracy, slower processing

### Key Components Architecture

**Control System:**
- `Ctrl+L` activation/deactivation to prevent interference between terminals
- Multiple modes: Manual (SPACE key) and Speak (continuous recording)
- Automatic clipboard integration for seamless Claude Code workflow

**Audio Processing Pipeline:**
```
Audio Input → Voice Recognition Engine → Text Processing → Clipboard Copy → Claude Code
```

**Threading Model:**
- Main thread handles keyboard input detection
- Separate threads for audio recording to prevent blocking
- Background processing for transcription without interrupting user flow

## Current State & Recommended Usage

### Primary Versions (Production Ready)
- **`voice_activated_large.py`** - Vosk Large model, best balance of speed/accuracy
- **`voice_debug.py`** - Google Speech Recognition fallback, requires internet
- **`voice_whisper_tiny.py`** - Latest Whisper Base experiment (in testing)

### Development Commands

**Setup:**
```bash
# Install dependencies
pip install -r requirements.txt

# Download Vosk models
python download_vosk_large.py

# For Whisper models (auto-download on first run)
python voice_whisper_tiny.py
```

**Model Management:**
```bash
# Check downloaded models
ls -la vosk-model-*/
ls -la whisper_models/

# Clean up unused models (see DOWNLOADS_LOG.md)
rm -rf vosk-model-small-es-0.42/  # After confirming large works
rm -rf whisper_models/            # If sticking with Vosk
```

**Testing:**
```bash
# Test current production version
python voice_activated_large.py

# Test experimental Whisper
python voice_whisper_tiny.py

# Test Google Speech fallback
python voice_debug.py
```

## Technical Specifications

### Audio Configuration
- **Sample Rate:** 16kHz (optimal for speech recognition)
- **Channels:** Mono
- **Format:** 16-bit PCM
- **Chunk Size:** 1024-4096 samples (varies by engine)

### Model Accuracy Benchmarks
- **Vosk Small:** ~75-80% accuracy, ~100-200ms latency
- **Vosk Large:** ~85-90% accuracy, ~300-500ms latency  
- **Google Speech:** ~90-95% accuracy, ~1-3s latency
- **Whisper Base:** ~90-92% accuracy, ~3-4s latency

### Control Scheme
**Universal Controls:**
- `Ctrl+L` - Activate/deactivate script (prevents terminal interference)
- `q` - Quit application

**When Activated:**
- `SPACE` - Manual mode (hold to record, release to transcribe)
- `s` - Toggle speak mode (continuous recording)
- `ENTER` - In speak mode: process current audio, copy to clipboard, restart recording

## Known Issues & Limitations

### Model-Specific Issues
- **Vosk:** No automatic punctuation, context-dependent word changes
- **Google Speech:** Requires internet, daily usage limits, occasional poor accuracy
- **Whisper:** High latency (3-15s depending on model size), large memory footprint

### Environment Dependencies
- **Windows:** Requires proper microphone permissions and audio drivers
- **Anaconda:** Known conflicts between numpy versions and some speech libraries
- **Terminal:** Script must run in separate terminal from Claude Code to prevent key conflicts

## File Organization

### Core Scripts
- `voice_activated_large.py` - Production Vosk version
- `voice_debug.py` - Google Speech fallback
- `voice_whisper_tiny.py` - Experimental Whisper implementation

### Utility Scripts
- `download_vosk_large.py` - Model downloader for Vosk
- `download_model.py` - Legacy Vosk small model downloader

### Documentation
- `DOWNLOADS_LOG.md` - Tracks all downloaded models and dependencies
- `TESTS_PRECISION.md` - Standardized tests for comparing model accuracy
- `README.md` - User-facing documentation (outdated)

### Development Notes
The project has gone through multiple iterations testing different speech recognition approaches. The `DOWNLOADS_LOG.md` file tracks which models/dependencies are currently used vs. experimental. Many Python files represent different experimental approaches and can be cleaned up once a final solution is chosen.

The activation system (`Ctrl+L`) is crucial for practical usage since the voice assistant runs in a separate terminal from Claude Code, preventing keyboard conflicts during normal typing.