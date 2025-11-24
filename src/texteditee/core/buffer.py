from typing import List


class GapBuffer:
    def __init__(self, initial_size: int = 1024):
        self._buffer: List[str] = [''] * initial_size
        self._gap_start = 0
        self._gap_end = initial_size
        
    @property
    def gap_size(self) -> int:
        return self._gap_end - self._gap_start
    
    @property
    def size(self) -> int:
        return len(self._buffer) - self.gap_size
    
    def _expand(self, min_size: int = 0) -> None:
        new_size = max(len(self._buffer) * 2, len(self._buffer) + min_size)
        new_buffer = [''] * new_size
        
        new_buffer[:self._gap_start] = self._buffer[:self._gap_start]
        new_gap_end = new_size - (len(self._buffer) - self._gap_end)
        new_buffer[new_gap_end:] = self._buffer[self._gap_end:]
        
        self._buffer = new_buffer
        self._gap_end = new_gap_end
    
    def _move_gap(self, position: int) -> None:
        if position < self._gap_start:
            distance = self._gap_start - position
            self._buffer[self._gap_end - distance:self._gap_end] = \
                self._buffer[position:self._gap_start]
            self._gap_start = position
            self._gap_end -= distance
        elif position > self._gap_start:
            distance = position - self._gap_start
            self._buffer[self._gap_start:self._gap_start + distance] = \
                self._buffer[self._gap_end:self._gap_end + distance]
            self._gap_start = position
            self._gap_end += distance
    
    def insert(self, position: int, char: str) -> None:
        if self.gap_size == 0:
            self._expand()
        
        self._move_gap(position)
        self._buffer[self._gap_start] = char
        self._gap_start += 1
    
    def delete(self, position: int) -> str:
        if position >= self.size:
            return ''
        
        self._move_gap(position)
        if self._gap_end < len(self._buffer):
            deleted = self._buffer[self._gap_end]
            self._gap_end += 1
            return deleted
        return ''
    
    def get_text(self) -> str:
        return ''.join(self._buffer[:self._gap_start] + 
                      self._buffer[self._gap_end:])
    
    def get_char(self, position: int) -> str:
        if position < 0 or position >= self.size:
            return ''
        
        if position < self._gap_start:
            return self._buffer[position]
        else:
            return self._buffer[position + self.gap_size]


class Buffer:
    def __init__(self, filename: str = ''):
        self.filename = filename
        self._lines: List[GapBuffer] = [GapBuffer()]
        self.modified = False
        
    @property
    def line_count(self) -> int:
        return len(self._lines)
    
    def get_line(self, line_num: int) -> str:
        if 0 <= line_num < len(self._lines):
            return self._lines[line_num].get_text()
        return ''
    
    def get_all_lines(self) -> List[str]:
        return [line.get_text() for line in self._lines]
    
    def get_char(self, line: int, col: int) -> str:
        if 0 <= line < len(self._lines):
            return self._lines[line].get_char(col)
        return ''
    
    def insert_char(self, line: int, col: int, char: str) -> None:
        if char == '\n':
            self.split_line(line, col)
        else:
            if 0 <= line < len(self._lines):
                self._lines[line].insert(col, char)
                self.modified = True
    
    def delete_char(self, line: int, col: int) -> str:
        if 0 <= line < len(self._lines):
            deleted = self._lines[line].delete(col)
            self.modified = True
            return deleted
        return ''
    
    def split_line(self, line: int, col: int) -> None:
        if 0 <= line < len(self._lines):
            current_line = self._lines[line].get_text()
            left_part = current_line[:col]
            right_part = current_line[col:]
            
            new_left = GapBuffer()
            for char in left_part:
                new_left.insert(new_left.size, char)
            
            new_right = GapBuffer()
            for char in right_part:
                new_right.insert(new_right.size, char)
            
            self._lines[line] = new_left
            self._lines.insert(line + 1, new_right)
            self.modified = True
    
    def join_lines(self, line: int) -> None:
        if 0 <= line < len(self._lines) - 1:
            current = self._lines[line].get_text()
            next_line = self._lines[line + 1].get_text()
            
            new_line = GapBuffer()
            for char in current + next_line:
                new_line.insert(new_line.size, char)
            
            self._lines[line] = new_line
            del self._lines[line + 1]
            self.modified = True
    
    def delete_line(self, line: int) -> str:
        if 0 <= line < len(self._lines):
            deleted = self._lines[line].get_text()
            del self._lines[line]
            if len(self._lines) == 0:
                self._lines = [GapBuffer()]
            self.modified = True
            return deleted
        return ''
    
    def insert_line(self, line: int, text: str = '') -> None:
        new_line = GapBuffer()
        for char in text:
            new_line.insert(new_line.size, char)
        
        if line <= len(self._lines):
            self._lines.insert(line, new_line)
        else:
            self._lines.append(new_line)
        self.modified = True
    
    def load_from_file(self, filename: str) -> None:
        self.filename = filename
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
            
            self._lines = []
            for line_text in lines:
                line = GapBuffer()
                for char in line_text:
                    line.insert(line.size, char)
                self._lines.append(line)
            
            if not self._lines:
                self._lines = [GapBuffer()]
            
            self.modified = False
        except FileNotFoundError:
            self._lines = [GapBuffer()]
            self.modified = False
    
    def save_to_file(self, filename: str = '') -> None:
        if filename:
            self.filename = filename
        
        if not self.filename:
            raise ValueError("No filename specified")
        
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.get_all_lines()))
        
        self.modified = False
