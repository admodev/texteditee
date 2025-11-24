# TextEditee Quick Start Guide

## Installation

### Option 1: Run from Source (Recommended for Development)

```bash
# Clone or navigate to the repository
cd texteditee

# Install dependencies
python -m pip install -r requirements.txt

# Run the editor
python -m src.texteditee.main [filename]
```

### Option 2: Install as Package

```bash
# Install in development mode
pip install -e .

# Run from anywhere
texteditee [filename]
# or
te [filename]
```

### Option 3: Build Binary (For Distribution)

**Windows:**

```bash
cd installers
build_windows.bat
# Output: dist\TextEditee-Setup.exe
```

**Linux/macOS:**

```bash
cd installers
chmod +x build_linux.sh  # or build_macos.sh
./build_linux.sh         # or ./build_macos.sh
# Output: dist/texteditee
```

## First Steps

### 1. Open a File

```bash
# Open existing file
python -m src.texteditee.main test_file.py

# Open new file
python -m src.texteditee.main mynewfile.txt
```

### 2. Basic Editing

1. **Start in Normal Mode** - You can navigate but not type
2. **Press `i`** to enter Edit Mode
3. **Type your text**
4. **Press `Esc`** to return to Normal Mode
5. **Type `:w`** and press `Enter` to save
6. **Type `:q`** and press `Enter` to quit

### 3. Essential Commands

**Navigation (Normal Mode):**

- `h` `j` `k` `l` - Left, Down, Up, Right
- `w` - Next word
- `b` - Previous word
- `0` - Start of line
- `$` - End of line
- `gg` - First line
- `G` - Last line

**Editing (Normal Mode):**

- `i` - Edit before cursor
- `a` - Edit after cursor
- `o` - Open new line below
- `x` - Delete character
- `dd` - Delete line
- `yy` - Copy line
- `p` - Paste

**File Operations (Command Mode):**

- `:w` - Save
- `:q` - Quit
- `:wq` - Save and quit
- `:q!` - Quit without saving

## Example Workflow

### Edit a Python File

```bash
# 1. Open file
python -m src.texteditee.main hello.py

# 2. Navigate to where you want to edit
#    Use j/k to move down/up
#    Use w/b to move by words

# 3. Enter Edit mode
#    Press 'i'

# 4. Type your code
#    def hello():
#        print("Hello, World!")

# 5. Exit Edit mode
#    Press Esc

# 6. Save and quit
#    Type :wq and press Enter
```

### Search and Replace

```bash
# 1. Open file
python -m src.texteditee.main myfile.txt

# 2. Search for text
#    Press / and type your search term
#    Press Enter

# 3. Navigate matches
#    Press n for next match
#    Press N for previous match

# 4. Replace on current line
#    Type :s/old/new/
#    Press Enter
```

## Keyboard Cheat Sheet

### Normal Mode

```
Movement:
  h j k l     - Left, Down, Up, Right
  w b e       - Word forward, backward, end
  0 ^ $       - Line start, first non-blank, end
  gg G        - First line, last line

Editing:
  i a I A     - Edit modes
  o O         - Open line below/above
  x dd D      - Delete char/line/to-end
  yy p P      - Yank/paste

Other:
  u Ctrl+r    - Undo/redo
  /           - Search
  :           - Command mode
  v V         - Visual mode
```

### Edit Mode

```
Esc         - Exit to Normal mode
Backspace   - Delete previous char
Enter       - New line
Tab         - Insert spaces (4)
```

### Command Mode

```
:w          - Save
:q          - Quit
:wq         - Save and quit
:q!         - Force quit
:e file     - Open file
:123        - Go to line 123
```

## Tips

1. **Stay in Normal Mode** - Only enter Edit Mode when typing
2. **Use Counts** - `5j` moves down 5 lines
3. **Learn Word Motions** - `w` and `b` are very efficient
4. **Practice** - Vim-style editing has a learning curve but becomes very fast

## Troubleshooting

### "Module not found" error

```bash
# Make sure you're in the project directory
cd texteditee

# Install dependencies
python -m pip install -r requirements.txt
```

### "pip not found" error

```bash
# Use python -m pip instead
python -m pip install -r requirements.txt
```

### Keys not working

- Make sure you're in the correct mode
- Check that your terminal supports the key sequences
- Try a different terminal emulator

## Next Steps

- Read the full [User Guide](docs/user_guide.md)
- Check out the [README](README.md) for more features
- See [CONTRIBUTING](CONTRIBUTING.md) to contribute

## Getting Help

- Check the documentation in `docs/`
- Open an issue on GitHub
- Read the source code (it's clean and well-commented!)

---

**Happy Editing! 🎉**
