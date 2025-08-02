# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Voice-to-Text Assistant** specifically designed for interacting with Claude Code via voice commands. The main goal is to enable users to speak their prompts instead of typing them, with automatic transcription and clipboard copying for seamless integration with Claude Code sessions.

## Core Architecture

### Voice Recognition Engine
The project uses **OpenAI Whisper** with faster-whisper implementation:

- **Whisper Base** - 74MB, 3-4s latency, ~92% accuracy (balance)
- **Whisper Small** - 244MB, 5-8s latency, ~94% accuracy (precision)

### Key Components Architecture

**Control System:**
- `Ctrl+L` activation/deactivation to prevent interference between terminals
- Multiple modes: Manual (SPACE key) and Speak (continuous recording with VAD)
- Automatic clipboard integration for seamless Claude Code workflow

**Audio Processing Pipeline:**
```
Audio Input → VAD Detection → Pre-buffer → Whisper Processing → Clipboard Copy → Claude Code
```

**Threading Model:**
- Main thread handles keyboard input detection
- Separate threads for audio recording to prevent blocking
- Background processing for transcription without interrupting user flow

## Current State & Production Versions

### Primary Production Files
- **`voicebase.py`** - Whisper Base model, optimized for speed/balance
- **`voicesmall.py`** - Whisper Small model, optimized for precision

### Global Execution
```bash
# From anywhere in terminal:
voicebase    # Launch Base model
voicesmall   # Launch Small model
```

### Development Commands

**Setup:**
```bash
# Install dependencies
pip install -r requirements.txt

# Models download automatically on first run
python voicebase.py
```

**Testing:**
```bash
# Test production versions
python voicebase.py   # Base model
python voicesmall.py  # Small model

# Test globally
voicebase     # From any directory
voicesmall    # From any directory
```

## Technical Specifications

### Audio Configuration
- **Sample Rate:** 16kHz (optimal for speech recognition)
- **Channels:** Mono
- **Format:** 16-bit PCM
- **Chunk Size:** 1024 samples

### VAD (Voice Activity Detection)
- **Threshold:** 500 (voice detection sensitivity)
- **Silence Duration:** 1.5s (pause detection)
- **Pre-buffer:** 1.0s (captures words before detection)
- **Min Speech:** 0.1s (minimum voice duration)

### Model Performance Benchmarks
- **Whisper Base:** ~92% accuracy, ~3-4s latency, 74MB
- **Whisper Small:** ~94% accuracy, ~5-8s latency, 244MB

### Control Scheme
**Universal Controls:**
- `Ctrl+L` - Activate/deactivate script (prevents terminal interference)
- `q` - Quit application

**When Activated:**
- `SPACE` - Manual mode (hold to record, release to transcribe)
- `s` - Toggle speak mode (continuous recording with VAD)
- `ENTER` - In speak mode: process accumulated audio, copy to clipboard

## File Organization

### Core Production Scripts
- `voicebase.py` - Main production script (Whisper Base)
- `voicesmall.py` - High precision script (Whisper Small)
- `voicebase.bat` - Global Windows launcher (Base)
- `voicesmall.bat` - Global Windows launcher (Small)

### Documentation
- `docs/TECHNICAL_GUIDE.md` - Complete technical documentation
- `docs/CURRENT_FEATURES.md` - Detailed current functionality
- `docs/TESTS_PRECISION.md` - Model comparison and testing
- `INSTALL_GLOBAL.md` - Global installation guide
- `README.md` - User-facing documentation

### Configuration
- `requirements.txt` - Python dependencies
- `whisper_models/` - Downloaded Whisper models (auto-created)

## Development Workflow

### For Content Creation
The project is designed for **educational content creation** about AI tool development:

1. **MVP Complete** - Functional voice-to-text assistant
2. **Documentation Ready** - All processes documented
3. **Improvement Pipeline** - Clear roadmap for enhancements
4. **Real Usage** - Daily use with Claude Code for development

### Typical Development Session
1. Open editor (Cursor/VS Code) in project directory
2. Open separate terminal for voice assistant
3. Launch: `voicebase` (from any directory)
4. Activate with `Ctrl+L`
5. Use voice commands seamlessly with development workflow

### Content Roadmap
- **Week 1:** Tool usage and basic improvements
- **Future:** GUI development, advanced features, integrations
- **Documentation:** Process videos, tutorial content

## Known Limitations & Solutions

### Current Limitations
- **Windows Focus:** Optimized for Windows (cross-platform possible)
- **Spanish Only:** Language hardcoded (multi-language planned)
- **Terminal Based:** No GUI yet (GUI in roadmap)

### Planned Improvements
- [ ] Graphical configuration interface
- [ ] Multi-language support
- [ ] Real-time accuracy metrics
- [ ] Editor integrations beyond clipboard
- [ ] Voice commands (not just dictation)

## Important Notes

- **Separate Terminal Required:** Voice assistant must run in separate terminal from Claude Code to prevent hotkey conflicts
- **Offline Operation:** After initial model download, works completely offline
- **Global Access:** Can be launched from any directory after setup
- **Educational Focus:** Designed for learning and content creation about AI tool development