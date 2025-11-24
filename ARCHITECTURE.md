# TextEditee Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         TextEditee v1.0.0                        │
│                  Professional Vim-Style Editor                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                          User Interface                          │
├─────────────────────────────────────────────────────────────────┤
│  Terminal (Blessed)                                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Line Numbers │ Editor Content (Syntax Highlighted)      │  │
│  │      1        │ def hello_world():                       │  │
│  │      2        │     print("Hello!")                      │  │
│  │      3        │                                          │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │  Status Line: filename.py [+] 2,5 -- EDIT --          │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │  Command Line: :w                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────┴───────────────────────────────────┐
│                        UI Layer (ui/)                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Renderer    │  │  Theme       │  │  StatusLine  │         │
│  │  - render()  │  │  - colors    │  │  - display() │         │
│  │  - update()  │  │  - schemes   │  │  - format()  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────┴───────────────────────────────────┐
│                     Input Layer (input/)                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌────────────────────────────────────┐  │
│  │  KeyBindings     │  │  CommandParser                     │  │
│  │  - handle_key()  │  │  - parse()                         │  │
│  │  - normal_mode   │  │  - :w, :q, :e, :s                  │  │
│  │  - edit_mode   │  │  - substitution                    │  │
│  │  - visual_mode   │  │  - goto line                       │  │
│  └──────────────────┘  └────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────┴───────────────────────────────────┐
│                      Core Engine (core/)                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Buffer      │  │  Cursor      │  │  Viewport    │         │
│  │  - Gap       │  │  - position  │  │  - scroll    │         │
│  │    Buffer    │  │  - move()    │  │  - visible   │         │
│  │  - edit()  │  │  - navigate()│  │  - render    │         │
│  │  - delete()  │  │              │  │    area      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  ModeManager                                             │  │
│  │  - Normal │ Edit │ Visual │ Command │ Search          │  │
│  │  - transitions and mode-specific behavior               │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────┴───────────────────────────────────┐
│                     Features Layer (features/)                   │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Syntax      │  │  Search      │  │  Undo/Redo   │         │
│  │  Highlighter │  │  Engine      │  │  Manager     │         │
│  │  (Pygments)  │  │  - regex     │  │  - Command   │         │
│  │              │  │  - replace   │  │    Pattern   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Clipboard (Singleton)                                   │  │
│  │  - System integration (pyperclip)                        │  │
│  │  - Internal clipboard fallback                           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────┴───────────────────────────────────┐
│                   File System Layer (fs/)                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌────────────────────────────────────┐  │
│  │  FileManager     │  │  BufferManager                     │  │
│  │  - load()        │  │  - multiple buffers                │  │
│  │  - save()        │  │  - buffer switching                │  │
│  │  - I/O ops       │  │  - session management              │  │
│  └──────────────────┘  └────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        Data Flow                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User Input (Keyboard)                                          │
│       │                                                          │
│       ▼                                                          │
│  Input Layer (KeyBindings/CommandParser)                        │
│       │                                                          │
│       ▼                                                          │
│  Core Engine (Buffer/Cursor/Mode)                               │
│       │                                                          │
│       ▼                                                          │
│  Features (Syntax/Search/Undo)                                  │
│       │                                                          │
│       ▼                                                          │
│  UI Layer (Renderer)                                            │
│       │                                                          │
│       ▼                                                          │
│  Terminal Display                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      Design Patterns                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Command Pattern:     Undo/Redo, Key Bindings                   │
│  Strategy Pattern:    Different Editing Modes                   │
│  Singleton Pattern:   Clipboard, Configuration                  │
│  Observer Pattern:    Buffer Change Notifications               │
│  Factory Pattern:     Buffer Creation                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    Key Data Structures                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Gap Buffer:      Efficient text editing (O(1) insertions)      │
│  Undo Stack:      Action history for undo/redo                  │
│  Key Registry:    Keybinding mappings                           │
│  Search Matches:  List of search results                        │
│  Syntax Tokens:   Highlighted code segments                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   Module Dependencies                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  main.py                                                         │
│    ├── core/        (buffer, cursor, mode, viewport)            │
│    ├── input/       (key_bindings, command_parser)              │
│    ├── ui/          (renderer, theme)                           │
│    ├── features/    (syntax, search, undo, clipboard)           │
│    └── fs/          (file_manager, buffer_manager)              │
│                                                                  │
│  External Dependencies:                                          │
│    ├── blessed      (terminal handling)                         │
│    ├── pygments     (syntax highlighting)                       │
│    ├── pyperclip    (clipboard integration)                     │
│    └── pyyaml       (configuration)                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### Core Layer

- **Buffer**: Text storage and manipulation using gap buffer
- **Cursor**: Position tracking and movement logic
- **Mode**: Modal editing state management
- **Viewport**: Visible area and scrolling

### Input Layer

- **KeyBindings**: Vim keybinding registry and handling
- **CommandParser**: Ex command parsing and execution

### UI Layer

- **Renderer**: Terminal output and screen updates
- **Theme**: Color schemes and styling
- **StatusLine**: Status bar display

### Features Layer

- **Syntax**: Code highlighting via Pygments
- **Search**: Text search and replace
- **Undo**: Undo/redo with action history
- **Clipboard**: System clipboard integration

### File System Layer

- **FileManager**: File I/O operations
- **BufferManager**: Multiple buffer management

## Interaction Flow

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│   User   │────▶│  Input   │────▶│   Core   │────▶│    UI    │
│ Keyboard │     │  Layer   │     │  Engine  │     │  Layer   │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
                       │                 │                │
                       ▼                 ▼                ▼
                 ┌──────────┐     ┌──────────┐     ┌──────────┐
                 │ Commands │     │ Features │     │ Terminal │
                 │  Parser  │     │  Layer   │     │ Display  │
                 └──────────┘     └──────────┘     └──────────┘
```
