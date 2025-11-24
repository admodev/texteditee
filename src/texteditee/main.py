from blessed import Terminal
from typing import Optional
import sys

from .core.buffer import Buffer
from .core.cursor import Cursor
from .core.mode import Mode, ModeManager
from .core.viewport import Viewport
from .ui.renderer import Renderer
from .ui.theme import ThemeManager
from .input.key_bindings import KeyBindingRegistry, setup_default_bindings
from .input.command_parser import CommandParser
from .features.undo import UndoManager
from .features.search import SearchEngine
from .features.clipboard import Clipboard


class Editor:
    def __init__(self, filename: Optional[str] = None):
        self.term = Terminal()
        self.buffer = Buffer(filename or '')
        self.cursor = Cursor(self.buffer)
        self.mode_manager = ModeManager()
        self.viewport = Viewport(self.buffer, self.term.height - 2, self.term.width)
        self.theme_manager = ThemeManager()
        self.renderer = Renderer(self.term, self.theme_manager)
        self.key_bindings = KeyBindingRegistry()
        self.command_parser = CommandParser()
        self.undo_manager = UndoManager()
        self.search_engine = SearchEngine()
        self.clipboard = Clipboard()
        
        self.running = True
        self.message = ''
        self.command_line = ''
        self.command_cursor = 0
        
        setup_default_bindings(self.key_bindings, self)
        self._register_commands()
        
        if filename:
            try:
                self.buffer.load_from_file(filename)
                self.renderer.highlighter.set_file(filename)
            except Exception as e:
                self.message = f'Error loading file: {e}'
    
    def _register_commands(self) -> None:
        self.command_parser.register('q', lambda e: e.quit())
        self.command_parser.register('q!', lambda e: e.force_quit())
        self.command_parser.register('w', lambda e, *args: e.save(args[0] if args else ''))
        self.command_parser.register('wq', lambda e, *args: (e.save(args[0] if args else ''), e.quit()))
        self.command_parser.register('x', lambda e: (e.save() if e.buffer.modified else None, e.quit()))
        self.command_parser.register('e', lambda e, *args: e.open_file(args[0] if args else ''))
        self.command_parser.register('set', lambda e, *args: e.set_option(args[0] if args else ''))
        self.command_parser.register('setheme', lambda e, *args: e.set_theme(args[0] if args else ''))
    
    def run(self) -> None:
        with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor():
            while self.running:
                self.viewport.scroll_to_cursor(self.cursor.line, self.cursor.col)
                self.renderer.render_buffer(
                    self.buffer, self.viewport, self.cursor, self.mode_manager.current
                )
                
                if self.message:
                    self.renderer.show_message(self.message)
                    self.message = ''
                
                if self.mode_manager.is_command():
                    self.renderer.render_command_line(':', self.command_line, self.command_cursor)
                
                pending = self.key_bindings.get_pending_display()
                if pending:
                    self.renderer.show_message(pending)
                
                key = self.term.inkey(timeout=None)
                self._handle_key(key)
    
    def _handle_key(self, key) -> None:
        if self.mode_manager.is_command():
            self._handle_command_key(key)
        elif self.mode_manager.is_insert():
            self._handle_insert_key(key)
        else:
            self._handle_normal_key(key)
    
    def _handle_normal_key(self, key) -> None:
        key_name = key.name if key.name else str(key)
        
        result = self.key_bindings.handle_key(key_name, 'normal')
        if result:
            handler, count = result
            try:
                handler(self, count)
            except Exception as e:
                self.message = f'Error: {e}'
    
    def _handle_insert_key(self, key) -> None:
        if key.name == 'KEY_ESCAPE':
            self.exit_insert_mode()
        elif key.name == 'KEY_BACKSPACE':
            if self.cursor.col > 0:
                self.cursor.move_left()
                self.buffer.delete_char(self.cursor.line, self.cursor.col)
            elif self.cursor.line > 0:
                prev_line_len = len(self.buffer.get_line(self.cursor.line - 1))
                self.buffer.join_lines(self.cursor.line - 1)
                self.cursor.move_to(self.cursor.line - 1, prev_line_len)
        elif key.name == 'KEY_ENTER':
            self.buffer.insert_char(self.cursor.line, self.cursor.col, '\n')
            self.cursor.move_to(self.cursor.line + 1, 0)
        elif key.name == 'KEY_TAB':
            for _ in range(4):
                self.buffer.insert_char(self.cursor.line, self.cursor.col, ' ')
                self.cursor.move_right()
        elif key.is_sequence:
            pass
        else:
            self.buffer.insert_char(self.cursor.line, self.cursor.col, str(key))
            self.cursor.move_right()
    
    def _handle_command_key(self, key) -> None:
        if key.name == 'KEY_ESCAPE':
            self.mode_manager.to_normal()
            self.command_line = ''
            self.command_cursor = 0
        elif key.name == 'KEY_ENTER':
            self._execute_command()
        elif key.name == 'KEY_BACKSPACE':
            if self.command_cursor > 0:
                self.command_line = (self.command_line[:self.command_cursor - 1] + 
                                   self.command_line[self.command_cursor:])
                self.command_cursor -= 1
        elif key.name == 'KEY_LEFT':
            self.command_cursor = max(0, self.command_cursor - 1)
        elif key.name == 'KEY_RIGHT':
            self.command_cursor = min(len(self.command_line), self.command_cursor + 1)
        elif not key.is_sequence:
            self.command_line = (self.command_line[:self.command_cursor] + 
                               str(key) + self.command_line[self.command_cursor:])
            self.command_cursor += 1
    
    def _execute_command(self) -> None:
        cmd = self.command_parser.parse(self.command_line)
        if cmd:
            try:
                cmd.handler(self, *cmd.args)
            except Exception as e:
                self.message = f'Error: {e}'
        else:
            self.message = f'Unknown command: {self.command_line}'
        
        self.mode_manager.to_normal()
        self.command_line = ''
        self.command_cursor = 0
    
    def enter_insert_mode(self) -> None:
        self.mode_manager.to_insert()
    
    def enter_insert_mode_after(self) -> None:
        self.cursor.move_right()
        self.mode_manager.to_insert()
    
    def insert_at_line_start(self) -> None:
        self.cursor.move_to_first_non_blank()
        self.mode_manager.to_insert()
    
    def insert_at_line_end(self) -> None:
        self.cursor.move_to_line_end()
        self.mode_manager.to_insert()
    
    def open_line_below(self) -> None:
        self.buffer.insert_line(self.cursor.line + 1, '')
        self.cursor.move_to(self.cursor.line + 1, 0)
        self.mode_manager.to_insert()
    
    def open_line_above(self) -> None:
        self.buffer.insert_line(self.cursor.line, '')
        self.cursor.move_to(self.cursor.line, 0)
        self.mode_manager.to_insert()
    
    def exit_insert_mode(self) -> None:
        if self.cursor.col > 0:
            self.cursor.move_left()
        self.mode_manager.to_normal()
    
    def enter_command_mode(self) -> None:
        self.mode_manager.to_command()
        self.command_line = ''
        self.command_cursor = 0
    
    def enter_visual_mode(self) -> None:
        self.mode_manager.to_visual()
    
    def enter_visual_line_mode(self) -> None:
        self.mode_manager.to_visual_line()
    
    def delete_char(self, count: int = 1) -> None:
        for _ in range(count):
            self.buffer.delete_char(self.cursor.line, self.cursor.col)
    
    def delete_line(self, count: int = 1) -> None:
        lines = []
        for _ in range(count):
            lines.append(self.buffer.delete_line(self.cursor.line))
        self.clipboard.copy(lines)
    
    def delete_to_line_end(self) -> None:
        line = self.buffer.get_line(self.cursor.line)
        deleted = line[self.cursor.col:]
        for _ in range(len(deleted)):
            self.buffer.delete_char(self.cursor.line, self.cursor.col)
        self.clipboard.copy(deleted)
    
    def yank_line(self, count: int = 1) -> None:
        lines = []
        for i in range(count):
            if self.cursor.line + i < self.buffer.line_count:
                lines.append(self.buffer.get_line(self.cursor.line + i))
        self.clipboard.copy(lines)
    
    def paste_after(self, count: int = 1) -> None:
        for _ in range(count):
            lines = self.clipboard.paste()
            if len(lines) == 1:
                for char in lines[0]:
                    self.cursor.move_right()
                    self.buffer.insert_char(self.cursor.line, self.cursor.col, char)
            else:
                for i, line in enumerate(lines):
                    self.buffer.insert_line(self.cursor.line + i + 1, line)
    
    def paste_before(self, count: int = 1) -> None:
        for _ in range(count):
            lines = self.clipboard.paste()
            if len(lines) == 1:
                for char in lines[0]:
                    self.buffer.insert_char(self.cursor.line, self.cursor.col, char)
                    self.cursor.move_right()
            else:
                for i, line in enumerate(lines):
                    self.buffer.insert_line(self.cursor.line + i, line)
    
    def undo(self) -> None:
        if self.undo_manager.undo():
            self.message = 'Undone'
        else:
            self.message = 'Nothing to undo'
    
    def redo(self) -> None:
        if self.undo_manager.redo():
            self.message = 'Redone'
        else:
            self.message = 'Nothing to redo'
    
    def start_search(self) -> None:
        self.message = 'Search not yet implemented'
    
    def start_search_backward(self) -> None:
        self.message = 'Search not yet implemented'
    
    def find_next(self) -> None:
        self.message = 'Search not yet implemented'
    
    def find_previous(self) -> None:
        self.message = 'Search not yet implemented'
    
    def goto_line(self, line: int) -> None:
        self.cursor.move_to(line, 0)
    
    def save(self, filename: str = '') -> None:
        try:
            self.buffer.save_to_file(filename)
            self.message = f'"{self.buffer.filename}" written'
        except Exception as e:
            self.message = f'Error saving: {e}'
    
    def open_file(self, filename: str) -> None:
        if self.buffer.modified:
            self.message = 'No write since last change (use :e! to override)'
            return
        
        try:
            self.buffer.load_from_file(filename)
            self.renderer.highlighter.set_file(filename)
            self.cursor.move_to(0, 0)
            self.message = f'"{filename}" loaded'
        except Exception as e:
            self.message = f'Error loading: {e}'
    
    def set_option(self, option: str) -> None:
        if option == 'number':
            self.renderer.show_line_numbers = True
        elif option == 'nonumber':
            self.renderer.show_line_numbers = False
        else:
            self.message = f'Unknown option: {option}'
    
    def quit(self) -> None:
        if self.buffer.modified:
            self.message = 'No write since last change (use :q! to override)'
        else:
            self.running = False
    
    def force_quit(self) -> None:
        self.running = False
    
    def interrupt(self) -> None:
        self.key_bindings.clear_pending()
        self.mode_manager.to_normal()
    
    def set_theme(self, theme_name: str) -> None:
        if self.theme_manager.set_theme(theme_name):
            self.message = f'Theme changed to: {theme_name}'
        else:
            available = ', '.join(self.theme_manager.list_themes())
            self.message = f'Unknown theme. Available: {available}'


def main() -> None:
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    editor = Editor(filename)
    
    try:
        editor.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f'Fatal error: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
