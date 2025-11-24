from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .buffer import Buffer


class Cursor:
    def __init__(self, buffer: 'Buffer'):
        self.buffer = buffer
        self.line = 0
        self.col = 0
        self.desired_col = 0
        
    @property
    def position(self) -> tuple[int, int]:
        return (self.line, self.col)
    
    def move_to(self, line: int, col: int) -> None:
        self.line = max(0, min(line, self.buffer.line_count - 1))
        line_length = len(self.buffer.get_line(self.line))
        self.col = max(0, min(col, line_length))
        self.desired_col = self.col
    
    def move_up(self, count: int = 1) -> None:
        new_line = max(0, self.line - count)
        self.line = new_line
        self._adjust_col_to_desired()
    
    def move_down(self, count: int = 1) -> None:
        new_line = min(self.buffer.line_count - 1, self.line + count)
        self.line = new_line
        self._adjust_col_to_desired()
    
    def move_left(self, count: int = 1) -> None:
        self.col = max(0, self.col - count)
        self.desired_col = self.col
    
    def move_right(self, count: int = 1) -> None:
        line_length = len(self.buffer.get_line(self.line))
        self.col = min(line_length, self.col + count)
        self.desired_col = self.col
    
    def move_to_line_start(self) -> None:
        self.col = 0
        self.desired_col = 0
    
    def move_to_line_end(self) -> None:
        self.col = len(self.buffer.get_line(self.line))
        self.desired_col = self.col
    
    def move_to_first_non_blank(self) -> None:
        line = self.buffer.get_line(self.line)
        for i, char in enumerate(line):
            if not char.isspace():
                self.col = i
                self.desired_col = i
                return
        self.col = 0
        self.desired_col = 0
    
    def move_word_forward(self, count: int = 1) -> None:
        for _ in range(count):
            line = self.buffer.get_line(self.line)
            
            if self.col >= len(line):
                if self.line < self.buffer.line_count - 1:
                    self.line += 1
                    self.col = 0
                    self._skip_whitespace_forward()
                continue
            
            if line[self.col].isalnum() or line[self.col] == '_':
                while self.col < len(line) and (line[self.col].isalnum() or line[self.col] == '_'):
                    self.col += 1
            elif not line[self.col].isspace():
                while self.col < len(line) and not line[self.col].isspace() and \
                      not (line[self.col].isalnum() or line[self.col] == '_'):
                    self.col += 1
            
            self._skip_whitespace_forward()
        
        self.desired_col = self.col
    
    def move_word_backward(self, count: int = 1) -> None:
        for _ in range(count):
            if self.col == 0:
                if self.line > 0:
                    self.line -= 1
                    self.col = len(self.buffer.get_line(self.line))
                continue
            
            self.col -= 1
            line = self.buffer.get_line(self.line)
            
            while self.col > 0 and line[self.col].isspace():
                self.col -= 1
            
            if self.col > 0:
                if line[self.col].isalnum() or line[self.col] == '_':
                    while self.col > 0 and (line[self.col - 1].isalnum() or line[self.col - 1] == '_'):
                        self.col -= 1
                else:
                    while self.col > 0 and not line[self.col - 1].isspace() and \
                          not (line[self.col - 1].isalnum() or line[self.col - 1] == '_'):
                        self.col -= 1
        
        self.desired_col = self.col
    
    def move_word_end(self, count: int = 1) -> None:
        for _ in range(count):
            line = self.buffer.get_line(self.line)
            
            if self.col >= len(line) - 1:
                if self.line < self.buffer.line_count - 1:
                    self.line += 1
                    self.col = 0
                    line = self.buffer.get_line(self.line)
                else:
                    continue
            else:
                self.col += 1
            
            while self.col < len(line) and line[self.col].isspace():
                self.col += 1
            
            if self.col < len(line):
                if line[self.col].isalnum() or line[self.col] == '_':
                    while self.col < len(line) - 1 and \
                          (line[self.col + 1].isalnum() or line[self.col + 1] == '_'):
                        self.col += 1
                else:
                    while self.col < len(line) - 1 and \
                          not line[self.col + 1].isspace() and \
                          not (line[self.col + 1].isalnum() or line[self.col + 1] == '_'):
                        self.col += 1
        
        self.desired_col = self.col
    
    def find_char_forward(self, char: str, count: int = 1) -> bool:
        line = self.buffer.get_line(self.line)
        pos = self.col + 1
        
        for _ in range(count):
            found = line.find(char, pos)
            if found == -1:
                return False
            pos = found + 1
        
        self.col = pos - 1
        self.desired_col = self.col
        return True
    
    def find_char_backward(self, char: str, count: int = 1) -> bool:
        line = self.buffer.get_line(self.line)
        pos = self.col - 1
        
        for _ in range(count):
            found = line.rfind(char, 0, pos + 1)
            if found == -1:
                return False
            pos = found - 1
        
        self.col = pos + 1
        self.desired_col = self.col
        return True
    
    def _adjust_col_to_desired(self) -> None:
        line_length = len(self.buffer.get_line(self.line))
        self.col = min(self.desired_col, line_length)
    
    def _skip_whitespace_forward(self) -> None:
        line = self.buffer.get_line(self.line)
        while self.col < len(line) and line[self.col].isspace():
            self.col += 1
