# ToneScript to WAV Generator 🎵

WAV file generator from telephone tones in ToneScript format.

## ✨ Features

- 🎯 Full ToneScript format support
- 📞 18 standard telephone tones (North America)
- 🔧 Complex pattern support
- 🎚 Automatic normalization

## 📦 Quick Start with uv

### Install uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Clone and Install

```bash
# Clone repository
git clone https://github.com/andrew-palamar/tonescript-generator.git
cd tonescript-generator

# Install dependencies with a single command
uv sync
```

### Activate Environment

```bash
# Automatic activation when running commands
uv run tonescript2wav --help

# Or activate manually
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate      # Windows
```

## 🚀 Usage

### Generate Single Tone

```bash
# Using uv run
uv run tonescript2wav "350@-19,440@-19;10(*/0/1+2)" output/dial_tone.wav

# Or after environment activation
tonescript2wav "480@-19,620@-19;10(.5/.5/1+2)" output/busy.wav --duration 5.0
```

### Generate All Tones

```bash
uv run test-tones
# or after environment activation
test-tones
```

## 📝 Project Commands

| Command                 | Description              |
| ----------------------- | ------------------------ |
| `uv sync`               | Install all dependencies |
| `uv run tonescript2wav` | Run generator            |
| `uv run test-tones`     | Generate all tones       |
| `uv pip list`           | Show installed packages  |
| `uv add numpy`          | Add new dependency       |

## 🏗 Project Structure

```
.
├── pyproject.toml          # Configuration and dependencies
├── README.md
├── src/
│   └── tonescript_generator/
│       ├── __init__.py
│       ├── core.py        # Core logic
│       ├── cli.py         # CLI interface
│       └── tester.py      # Tone tester
└── output/                # Generated WAV files
```

## 📝 ToneScript Format

### Basic Syntax
```
frequency1@level1,frequency2@level2;duration(on/off/components)
```

### Examples

- **Dial tone**: `350@-19,440@-19;10(*/0/1+2)`
- **Busy tone**: `480@-19,620@-19;10(.5/.5/1+2)`
- **Ringback tone**: `440@-19,480@-19;*(2/4/1+2)`

### Special Characters
- `*` - infinite duration
- `/` - subsection separator
- `+` - component combination
- `0` - silence (no sound)

## 🎛 Technical Details

- **Sample rate**: 48 kHz
- **Format**: WAV, PCM 16-bit
- **Maximum duration**: 60 seconds (for infinite tones)
- **dBm conversion**: with 6dB headroom to avoid clipping

## 📚 List of Supported Tones

1. Dial tone
2. Second dial tone
3. Outside dial tone
4. Prompt tone
5. Busy tone
6. Reorder tone
7. Howler tone
8. Ringback tone
9. Comfort tone
10. Special information tone SIT1
11. Special information tone SIT2
12. Special information tone SIT3
13. Special information tone SIT4
14. MWI Dial Tone
15. Call Forward Dial Tone
16. Holding tone
17. Conference call Tone
18. Call waiting tone

## 📄 License

MIT

## Reference

https://en.wikipedia.org/wiki/ToneScript
