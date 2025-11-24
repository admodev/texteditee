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
        self.last_theme_name = None
        self._apply_theme_background()
    
    def _apply_theme_background(self) -> None:
        bg_color = self.theme.get_color('background')
        bg_map = {
            'black': '\x1b[40m',
            'blue': '\x1b[44m',
            'white': '\x1b[47m',
            '#272822': '\x1b[40m',
            '#002B36': '\x1b[40m',
        }
        
        bg_code = bg_map.get(bg_color, '\x1b[40m')
        print(bg_code, end='', flush=True)
        
    def render_buffer(self, buffer: 'Buffer', viewport: 'Viewport', 
                     cursor: 'Cursor', mode: 'Mode') -> None:
        current_theme = self.theme.current_theme.name
        if current_theme != self.last_theme_name:
            self._apply_theme_background()
            self.last_theme_name = current_theme
            
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
            line_num_color = self.theme.get_color('line_number')
            color_map = {
                'cyan': self.term.cyan,
                'yellow': self.term.yellow,
                'bright_black': self.term.bright_black,
                'white': self.term.white,
                'red': self.term.red,
                'green': self.term.green,
                'magenta': self.term.magenta,
                'blue': self.term.blue,
                '#90908A': self.term.bright_black,
                '#586E75': self.term.bright_black,
            }
            color_func = color_map.get(line_num_color, self.term.cyan)
            output += color_func(line_num_str) + ' '
        
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
        
        status_bg = self.theme.get_color('status_bg')
        status_fg = self.theme.get_color('status_fg')
        
        bg_map = {
            'black': 'black',
            'blue': 'blue',
            'white': 'white',
            '#3E3D32': 'black',
            '#073642': 'black',
        }
        fg_map = {
            'white': self.term.white,
            '#F8F8F2': self.term.white,
            '#839496': self.term.white,
        }
        
        bg_name = bg_map.get(status_bg, 'blue')
        fg_func = fg_map.get(status_fg, self.term.white)
        
        try:
            bg_func = getattr(self.term, f'on_{bg_name}')
            status_formatted = bg_func(fg_func(status_line[:self.term.width]))
        except (AttributeError, TypeError):
            status_formatted = self.term.on_blue(self.term.white(status_line[:self.term.width]))
        
        with self.term.location(0, status_y):
            print(status_formatted)
    
    def _colorize(self, text: str, color_name: str) -> str:
        color_attr_map = {
            'keyword': 'keyword',
            'function': 'function',
            'class': 'class_name',
            'string': 'string',
            'comment': 'comment',
            'number': 'number',
            'operator': 'operator',
            'builtin': 'builtin',
            'decorator': 'decorator',
            'default': 'foreground',
        }
        
        attr_name = color_attr_map.get(color_name, 'foreground')
        color = self.theme.get_color(attr_name)
        
        color_map = {
            'black': self.term.black,
            'red': self.term.red,
            'green': self.term.green,
            'yellow': self.term.yellow,
            'blue': self.term.blue,
            'magenta': self.term.magenta,
            'cyan': self.term.cyan,
            'white': self.term.white,
            'bright_black': self.term.bright_black,
            'bright_red': self.term.bright_red,
            'bright_green': self.term.bright_green,
            'bright_yellow': self.term.bright_yellow,
            'bright_blue': self.term.bright_blue,
            'bright_magenta': self.term.bright_magenta,
            'bright_cyan': self.term.bright_cyan,
            'bright_white': self.term.bright_white,
            '#F92672': self.term.magenta,
            '#A6E22E': self.term.green,
            '#66D9EF': self.term.cyan,
            '#E6DB74': self.term.yellow,
            '#75715E': self.term.bright_black,
            '#AE81FF': self.term.magenta,
            '#268BD2': self.term.blue,
            '#B58900': self.term.yellow,
            '#2AA198': self.term.cyan,
            '#859900': self.term.green,
            '#D33682': self.term.magenta,
            '#DC322F': self.term.red,
            '#CB4B16': self.term.yellow,
            '#F8F8F2': self.term.white,
            '#839496': self.term.white,
        }
        
        if color in color_map:
            return color_map[color](text)
        return text
    
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
