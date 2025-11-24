# TextEditee User Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Concepts](#basic-concepts)
3. [Modes](#modes)
4. [Navigation](#navigation)
5. [Editing](#editing)
6. [File Operations](#file-operations)
7. [Search and Replace](#search-and-replace)
8. [Visual Mode](#visual-mode)
9. [Advanced Features](#advanced-features)
10. [Customization](#customization)

## Getting Started

### Opening Files

```bash
# Open a specific file
texteditee myfile.txt

# Open the editor without a file
texteditee

# Open with alias
te myfile.py
```

### First Steps

1. When you open TextEditee, you start in **Normal Mode**
2. Press `i` to enter **Insert Mode** and start typing
3. Press `Esc` to return to **Normal Mode**
4. Type `:w` and press `Enter` to save
5. Type `:q` and press `Enter` to quit

## Basic Concepts

### Modal Editing

TextEditee uses vim-style modal editing:

- **Normal Mode**: Navigate and execute commands
- **Insert Mode**: Type text
- **Visual Mode**: Select text
- **Command Mode**: Execute ex commands

### The Cursor

The cursor shows your current position in the file. In Normal Mode, it's on a character. In Insert Mode, it's between characters.

## Modes

### Normal Mode

The default mode for navigation and commands.

**Enter from:**

- Insert Mode: Press `Esc`
- Visual Mode: Press `Esc`
- Command Mode: Press `Esc` or `Enter`

### Insert Mode

For typing text.

**Enter from Normal Mode:**

- `i` - Insert before cursor
- `a` - Insert after cursor
- `I` - Insert at beginning of line
- `A` - Insert at end of line
- `o` - Open new line below
- `O` - Open new line above

**Exit to Normal Mode:**

- Press `Esc`

### Visual Mode

For selecting text.

**Enter from Normal Mode:**

- `v` - Character-wise selection
- `V` - Line-wise selection

**Exit to Normal Mode:**

- Press `Esc`

### Command Mode

For executing commands.

**Enter from Normal Mode:**

- Press `:`

**Exit to Normal Mode:**

- Press `Esc` or `Enter` (after executing command)

## Navigation

### Basic Movement

```
h - Move left
j - Move down
k - Move up
l - Move right
```

### Word Movement

```
w - Next word start
b - Previous word start
e - Next word end
```

### Line Movement

```
0 - Start of line
^ - First non-blank character
$ - End of line
```

### File Movement

```
gg - First line of file
G  - Last line of file
{number}G - Go to line {number}
```

### Character Finding

```
f{char} - Find next {char} on current line
F{char} - Find previous {char} on current line
```

## Editing

### Inserting Text

```
i - Insert before cursor
a - Insert after cursor
I - Insert at line start
A - Insert at line end
o - Open line below
O - Open line above
```

### Deleting Text

```
x - Delete character under cursor
dd - Delete current line
D - Delete from cursor to end of line
{number}dd - Delete {number} lines
```

### Copying and Pasting

```
yy - Yank (copy) current line
{number}yy - Yank {number} lines
p - Paste after cursor
P - Paste before cursor
```

### Undo and Redo

```
u - Undo last change
Ctrl+r - Redo
```

## File Operations

### Saving Files

```
:w - Save current file
:w filename - Save as filename
:wq - Save and quit
:x - Save (if modified) and quit
```

### Opening Files

```
:e filename - Open file
```

### Quitting

```
:q - Quit (fails if unsaved changes)
:q! - Force quit (discard changes)
:wq - Save and quit
```

## Search and Replace

### Searching

```
/ - Search forward
? - Search backward
n - Next match
N - Previous match
```

### Replacing

```
:s/pattern/replacement/ - Replace on current line
:{start},{end}s/pattern/replacement/ - Replace on range
```

## Visual Mode

### Selection

1. Enter visual mode with `v` or `V`
2. Move cursor to select text
3. Perform operation (delete, yank, etc.)

### Operations in Visual Mode

```
d - Delete selection
y - Yank (copy) selection
```

## Advanced Features

### Line Numbers

```
:set number - Show line numbers
:set nonumber - Hide line numbers
```

### Syntax Highlighting

Syntax highlighting is automatic based on file extension.

### Multiple Counts

Many commands accept a count:

```
3w - Move forward 3 words
5dd - Delete 5 lines
10j - Move down 10 lines
```

### Combining Commands

Commands can be combined with counts and motions:

```
d3w - Delete 3 words
y5j - Yank 5 lines down
```

## Customization

### Configuration

TextEditee can be configured through command mode settings.

### Themes

Available themes:

- `default` - Classic terminal colors
- `monokai` - Monokai color scheme

## Tips and Tricks

### Efficient Editing

1. **Stay in Normal Mode** - Only enter Insert Mode when typing
2. **Use Counts** - `5j` is faster than pressing `j` five times
3. **Learn Word Motions** - `w`, `b`, `e` are very efficient
4. **Use Line Operations** - `dd`, `yy` work on whole lines

### Common Workflows

**Quick Edit:**

```
1. Open file: texteditee file.txt
2. Navigate to location
3. Press i to insert
4. Make changes
5. Press Esc
6. Type :wq to save and quit
```

**Search and Replace:**

```
1. Press /
2. Type search pattern
3. Press Enter
4. Press n to find next
5. Use :s/old/new/ to replace
```

**Copy and Paste:**

```
1. Navigate to line
2. Press yy to copy
3. Navigate to destination
4. Press p to paste
```

## Keyboard Reference

### Normal Mode

| Key        | Action                           |
| ---------- | -------------------------------- |
| h, j, k, l | Move left, down, up, right       |
| w, b, e    | Word forward, backward, end      |
| 0, ^, $    | Line start, first non-blank, end |
| gg, G      | First line, last line            |
| i, a       | Insert before, after             |
| I, A       | Insert at line start, end        |
| o, O       | Open line below, above           |
| x          | Delete character                 |
| dd         | Delete line                      |
| yy         | Yank line                        |
| p, P       | Paste after, before              |
| u          | Undo                             |
| Ctrl+r     | Redo                             |
| /          | Search                           |
| :          | Command mode                     |
| v, V       | Visual mode                      |

### Insert Mode

| Key       | Action                    |
| --------- | ------------------------- |
| Esc       | Exit to Normal mode       |
| Backspace | Delete previous character |
| Enter     | New line                  |
| Tab       | Insert spaces             |

### Command Mode

| Command     | Action        |
| ----------- | ------------- |
| :w          | Save          |
| :q          | Quit          |
| :wq         | Save and quit |
| :q!         | Force quit    |
| :e file     | Open file     |
| :{num}      | Go to line    |
| :s/old/new/ | Substitute    |

## Troubleshooting

### Editor Won't Start

- Check Python version: `python --version` (need 3.12+)
- Verify dependencies: `pip list | grep blessed`

### Keys Not Working

- Make sure you're in the correct mode
- Check terminal compatibility
- Try a different terminal emulator

### File Won't Save

- Check file permissions
- Verify disk space
- Use `:w!` to force save (if you have permissions)

## Getting Help

- GitHub: https://github.com/yourusername/texteditee
- Issues: https://github.com/yourusername/texteditee/issues
- Documentation: See README.md

---

**Happy Editing with TextEditee!**
