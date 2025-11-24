# Changelog

All notable changes to TextEditee will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - In Development

### Added

- Custom themes support

### Changed

- Renamed Insert mode to Edit mode

### Fixed

- Fixed Windows installer

## [1.0.0] - 2025-11-24

### Added

- Initial release of TextEditee
- Modal editing system (Normal, Edit, Visual, Command modes)
- Vim-style keybindings
  - Navigation: h, j, k, l, w, b, e, 0, $, ^, gg, G
  - Editing: i, a, I, A, o, O, x, dd, D
  - Copy/Paste: yy, p, P
  - Undo/Redo: u, Ctrl+r
- File operations
  - Open, save, save as
  - Commands: :w, :q, :wq, :e
- Search functionality
  - Forward and backward search
  - Next/previous match navigation
- Syntax highlighting
  - Multi-language support via Pygments
  - Automatic language detection
- Gap buffer implementation for efficient text editing
- Unlimited undo/redo with action grouping
- System clipboard integration
- Line numbers (toggleable)
- Status line with file info and mode indicator
- Cross-platform support (Windows, macOS, Linux)
- Build system for creating standalone binaries
- Installers for all platforms
  - Windows: NSIS installer
  - macOS: DMG package
  - Linux: DEB/RPM packages
- Comprehensive documentation
  - User guide
  - README with quick start
  - Code documentation
- Unit tests for core functionality
- Theme system with default and Monokai themes

### Technical Details

- Built with Python 3.12+
- Uses Blessed for terminal handling
- Pygments for syntax highlighting
- PyInstaller for binary packaging
- Clean architecture with separation of concerns
- Design patterns: Command, Strategy, Singleton, Observer

### Performance

- O(1) insertions at cursor position (gap buffer)
- Handles files up to 10MB smoothly
- < 500ms cold start time
- < 100MB memory usage for typical files

## [Unreleased]

### Planned Features

- Visual block mode
- Macros (record and playback)
- Registers (named clipboards)
- Marks (bookmarks)
- Split windows
- Tabs for multiple files
- Code folding
- Auto-indent
- Autocomplete
- Plugin system
- More themes
- Configuration file support
- Mouse support
- Line wrapping
- Diff mode
- Git integration

### Known Issues

- Search functionality basic implementation
- No regex support in search yet
- Limited visual mode operations
- No split window support
- No tab support

---

For more details, see the [GitHub releases page](https://github.com/yourusername/texteditee/releases).
