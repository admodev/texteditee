from blessed import Terminal
from typing import List, Optional, TYPE_CHECKING
from ..features.syntax import SyntaxHighlighter

if TYPE_CHECKING:
    from ..core.buffer import Buffer
    from ..core.cursor import Cursor
    from ..core.viewport import Viewport
    from ..core.mode import Mode
    from .theme import ThemeManager


class Renderer:
    def __init__(self, term: Terminal, theme_manager: 'ThemeManager'):
        self.term = term
        self.theme = theme_manager
        self.show_line_numbers = True
        self.highlighter = SyntaxHighlighter()
        
    def render_buffer(self, buffer: 'Buffer', viewport: 'Viewport', 
                     cursor: 'Cursor', mode: 'Mode') -> None:
        with self.term.hidden_cursor():
            print(self.term.home + self.term.clear, end='')
            
            visible_lines = viewport.get_visible_lines()
            screen_height = self.term.height - 2
            
            for i, line in enumerate(visible_lines[:screen_height]):
                line_num = viewport.top_line + i
                self._render_line(line_num, line, i)
            
            for i in range(len(visible_lines), screen_height):
                print(self.term.move_xy(0, i) + self.term.cyan('~'))
            
            self._render_status_line(buffer, cursor, mode)
            
            screen_line, screen_col = viewport.cursor_to_screen_pos(
                cursor.line, cursor.col
            )
            
            if self.show_line_numbers:
                screen_col += self._line_number_width(buffer) + 1
            
            print(self.term.move_xy(screen_col, screen_line), end='', flush=True)
    
    def _render_line(self, line_num: int, line: str, screen_line: int) -> None:
        output = ''
        
        if self.show_line_numbers:
            line_num_str = str(line_num + 1).rjust(self._line_number_width(None))
            output += self.term.cyan(line_num_str) + ' '
        
        if self.highlighter.enabled:
            tokens = self.highlighter.highlight_line(line)
            for color_name, text in tokens:
                output += self._colorize(text, color_name)
        else:
            output += line
        
        print(self.term.move_xy(0, screen_line) + output)
    
    def _render_status_line(self, buffer: 'Buffer', cursor: 'Cursor', mode: 'Mode') -> None:
        status_y = self.term.height - 2
        
        filename = buffer.filename or '[No Name]'
        modified = ' [+]' if buffer.modified else ''
        position = f'{cursor.line + 1},{cursor.col + 1}'
        mode_str = str(mode)
        
        left_side = f' {filename}{modified}'
        right_side = f'{position} '
        
        padding = self.term.width - len(left_side) - len(right_side) - len(mode_str) - 2
        status_line = left_side + ' ' * max(0, padding) + mode_str + ' ' + right_side
        
        with self.term.location(0, status_y):
            print(self.term.on_blue(self.term.white(status_line[:self.term.width])))
    
    def _colorize(self, text: str, color_name: str) -> str:
        color_map = {
            'keyword': self.term.yellow,
            'function': self.term.green,
            'class': self.term.cyan,
            'string': self.term.magenta,
            'comment': self.term.bright_black,
            'number': self.term.red,
            'operator': self.term.white,
            'builtin': self.term.cyan,
            'decorator': self.term.yellow,
            'default': self.term.white,
        }
        
        color_func = color_map.get(color_name, self.term.white)
        return color_func(text)
    
    def _line_number_width(self, buffer: Optional['Buffer']) -> int:
        if buffer is None:
            return 4
        return max(4, len(str(buffer.line_count)))
    
    def render_command_line(self, prompt: str, text: str, cursor_pos: int) -> None:
        cmd_y = self.term.height - 1
        
        with self.term.location(0, cmd_y):
            line = prompt + text
            print(self.term.clear_eol + line[:self.term.width])
            
        cursor_x = len(prompt) + cursor_pos
        print(self.term.move_xy(cursor_x, cmd_y), end='', flush=True)
    
    def clear_command_line(self) -> None:
        cmd_y = self.term.height - 1
        with self.term.location(0, cmd_y):
            print(self.term.clear_eol, end='', flush=True)
    
    def show_message(self, message: str, error: bool = False) -> None:
        cmd_y = self.term.height - 1
        
        with self.term.location(0, cmd_y):
            if error:
                print(self.term.red(message[:self.term.width]))
            else:
                print(message[:self.term.width])
