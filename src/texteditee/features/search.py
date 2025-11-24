import re
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class SearchMatch:
    line: int
    col: int
    length: int


class SearchEngine:
    def __init__(self):
        self.pattern = ''
        self.regex = False
        self.case_sensitive = False
        self.whole_word = False
        self.matches: List[SearchMatch] = []
        self.current_match = -1
    
    def search(self, buffer: 'Buffer', pattern: str, 
               regex: bool = False, case_sensitive: bool = False,
               whole_word: bool = False) -> List[SearchMatch]:
        self.pattern = pattern
        self.regex = regex
        self.case_sensitive = case_sensitive
        self.whole_word = whole_word
        self.matches = []
        self.current_match = -1
        
        if not pattern:
            return self.matches
        
        flags = 0 if case_sensitive else re.IGNORECASE
        
        if regex:
            try:
                compiled_pattern = re.compile(pattern, flags)
            except re.error:
                return self.matches
        else:
            escaped_pattern = re.escape(pattern)
            if whole_word:
                escaped_pattern = r'\b' + escaped_pattern + r'\b'
            compiled_pattern = re.compile(escaped_pattern, flags)
        
        for line_num in range(buffer.line_count):
            line = buffer.get_line(line_num)
            for match in compiled_pattern.finditer(line):
                self.matches.append(SearchMatch(
                    line=line_num,
                    col=match.start(),
                    length=len(match.group())
                ))
        
        return self.matches
    
    def find_next(self, from_line: int, from_col: int) -> Optional[SearchMatch]:
        if not self.matches:
            return None
        
        for i, match in enumerate(self.matches):
            if match.line > from_line or (match.line == from_line and match.col > from_col):
                self.current_match = i
                return match
        
        if self.matches:
            self.current_match = 0
            return self.matches[0]
        
        return None
    
    def find_previous(self, from_line: int, from_col: int) -> Optional[SearchMatch]:
        if not self.matches:
            return None
        
        for i in range(len(self.matches) - 1, -1, -1):
            match = self.matches[i]
            if match.line < from_line or (match.line == from_line and match.col < from_col):
                self.current_match = i
                return match
        
        if self.matches:
            self.current_match = len(self.matches) - 1
            return self.matches[-1]
        
        return None
    
    def replace_current(self, buffer: 'Buffer', replacement: str) -> bool:
        if self.current_match < 0 or self.current_match >= len(self.matches):
            return False
        
        match = self.matches[self.current_match]
        line = buffer.get_line(match.line)
        
        for _ in range(match.length):
            buffer.delete_char(match.line, match.col)
        
        for i, char in enumerate(replacement):
            buffer.insert_char(match.line, match.col + i, char)
        
        return True
    
    def replace_all(self, buffer: 'Buffer', replacement: str) -> int:
        count = 0
        
        for match in reversed(self.matches):
            line = buffer.get_line(match.line)
            
            for _ in range(match.length):
                buffer.delete_char(match.line, match.col)
            
            for i, char in enumerate(replacement):
                buffer.insert_char(match.line, match.col + i, char)
            
            count += 1
        
        self.matches = []
        self.current_match = -1
        return count
    
    def clear(self) -> None:
        self.pattern = ''
        self.matches = []
        self.current_match = -1
