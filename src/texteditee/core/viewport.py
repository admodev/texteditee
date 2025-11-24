from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .buffer import Buffer


class Viewport:
    def __init__(self, buffer: 'Buffer', height: int, width: int):
        self.buffer = buffer
        self.height = height
        self.width = width
        self.top_line = 0
        self.left_col = 0
        
    def resize(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
    
    def scroll_to_cursor(self, cursor_line: int, cursor_col: int) -> None:
        if cursor_line < self.top_line:
            self.top_line = cursor_line
        elif cursor_line >= self.top_line + self.height:
            self.top_line = cursor_line - self.height + 1
        
        if cursor_col < self.left_col:
            self.left_col = cursor_col
        elif cursor_col >= self.left_col + self.width:
            self.left_col = cursor_col - self.width + 1
    
    def scroll_up(self, count: int = 1) -> None:
        self.top_line = max(0, self.top_line - count)
    
    def scroll_down(self, count: int = 1) -> None:
        max_top = max(0, self.buffer.line_count - self.height)
        self.top_line = min(max_top, self.top_line + count)
    
    def scroll_left(self, count: int = 1) -> None:
        self.left_col = max(0, self.left_col - count)
    
    def scroll_right(self, count: int = 1) -> None:
        self.left_col += count
    
    def center_on_cursor(self, cursor_line: int) -> None:
        self.top_line = max(0, cursor_line - self.height // 2)
    
    def get_visible_lines(self) -> list[str]:
        lines = []
        for i in range(self.height):
            line_num = self.top_line + i
            if line_num < self.buffer.line_count:
                line = self.buffer.get_line(line_num)
                visible_part = line[self.left_col:self.left_col + self.width]
                lines.append(visible_part)
            else:
                lines.append('')
        return lines
    
    def cursor_to_screen_pos(self, cursor_line: int, cursor_col: int) -> tuple[int, int]:
        screen_line = cursor_line - self.top_line
        screen_col = cursor_col - self.left_col
        return (screen_line, screen_col)
