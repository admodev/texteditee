# TextEditee

A professional vim-style terminal code editor built with Python 3.12+

## Features

✨ **Modal Editing** - Full vim-style modal editing (Normal, Edit, Visual, Command modes)  
⌨️ **Vim Keybindings** - Comprehensive vim keybindings for efficient text editing  
🎨 **Syntax Highlighting** - Multi-language syntax highlighting powered by Pygments  
↩️ **Undo/Redo** - Unlimited undo/redo with action grouping  
🔍 **Search & Replace** - Powerful search with regex support  
📋 **Clipboard Integration** - Seamless system clipboard integration  
🎯 **Line Numbers** - Optional line number display  
⚡ **Fast & Lightweight** - Efficient gap buffer implementation  
🌈 **Themes** - Multiple color schemes  
📦 **Cross-Platform** - Works on Windows, macOS, and Linux

## Installation

### From Binary

**Note**: Binaries need to be built first (see [Building from Source](#building-from-source) below).

Once built, you'll have:

- **Windows**: `dist\TextEditee-Setup.exe` (installer) or `dist\texteditee.exe` (standalone)
- **macOS**: `dist/texteditee` (standalone binary)
- **Linux**: `dist/texteditee` (standalone binary)

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/texteditee.git
cd texteditee

# Install dependencies
pip install -r requirements.txt

# Run the editor
python -m src.texteditee.main [filename]
```

### Install as Python Package

```bash
pip install -e .
texteditee [filename]
```

## Usage

### Basic Commands

```bash
# Open a file
texteditee myfile.txt

# Open editor without a file
texteditee
```

### Vim Keybindings

#### Normal Mode

**Navigation:**

- `h`, `j`, `k`, `l` - Move left, down, up, right
- `w`, `b`, `e` - Word forward, backward, end
- `0`, `$`, `^` - Line start, end, first non-blank
- `gg`, `G` - First line, last line
- `{number}G` - Go to line number

**Editing:**

- `i`, `a` - Edit before/after cursor
- `I`, `A` - Edit at line start/end
- `o`, `O` - Open line below/above
- `x` - Delete character
- `dd` - Delete line
- `D` - Delete to line end
- `yy` - Yank (copy) line
- `p`, `P` - Paste after/before

**Undo/Redo:**

- `u` - Undo
- `Ctrl+r` - Redo

**Search:**

- `/` - Search forward
- `?` - Search backward
- `n`, `N` - Next/previous match

**Visual Mode:**

- `v` - Character-wise visual mode
- `V` - Line-wise visual mode

#### Command Mode

Press `:` to enter command mode:

- `:w` - Save file
- `:w filename` - Save as filename
- `:q` - Quit (fails if unsaved changes)
- `:q!` - Force quit (discard changes)
- `:wq` or `:x` - Save and quit
- `:e filename` - Open file
- `:{number}` - Go to line number
- `:s/pattern/replacement/` - Substitute on current line
- `:{start},{end}s/pattern/replacement/` - Substitute on range

#### Edit Mode

- `Esc` - Return to normal mode
- `Backspace` - Delete previous character
- `Enter` - New line
- `Tab` - Insert spaces (4)

## Configuration

### Settings

Use `:set` commands:

- `:set number` - Show line numbers
- `:set nonumber` - Hide line numbers

### Themes

Available themes:

- `default` - Classic terminal colors
- `monokai` - Monokai color scheme

## Building from Source

### Prerequisites

- Python 3.12+
- pip
- PyInstaller (for building binaries)
- NSIS (Windows, for installer)
- dpkg-deb (Linux, for DEB packages)
- rpmbuild (Linux, for RPM packages)
- hdiutil (macOS, for DMG)

### Build Instructions

#### Windows

```bash
cd installers
build_windows.bat
```

Output: `dist\TextEditee-Setup.exe`

#### Linux

```bash
cd installers
chmod +x build_linux.sh
./build_linux.sh
```

Output: `dist/texteditee`

#### macOS

```bash
cd installers
chmod +x build_macos.sh
./build_macos.sh
```

Output: `dist/texteditee`

## Architecture

TextEditee follows clean architecture principles:

- **Core** - Buffer management, cursor, modes, viewport
- **Input** - Keyboard handling, command parsing, key bindings
- **UI** - Terminal rendering, themes, status line
- **Features** - Syntax highlighting, search, undo/redo, clipboard
- **FS** - File operations, buffer management

### Key Design Patterns

- **Gap Buffer** - Efficient text editing with O(1) insertions
- **Command Pattern** - Undo/redo and key bindings
- **Strategy Pattern** - Different editing modes
- **Singleton Pattern** - Clipboard and configuration

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black src/

# Type checking
mypy src/

# Linting
ruff check src/
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Inspired by Vim and Neovim
- Built with [Blessed](https://github.com/jquast/blessed) for terminal handling
- Syntax highlighting by [Pygments](https://pygments.org/)

## Why TextEditee?

Because Python can be a great choice for almost any use case, including building professional-grade terminal editors. TextEditee proves that Python's ecosystem and modern language features make it suitable for creating fast, efficient, and user-friendly development tools.
