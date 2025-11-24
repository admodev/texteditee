from pygments import lex
from pygments.lexers import get_lexer_for_filename, get_lexer_by_name, TextLexer
from pygments.token import Token
from typing import List, Tuple, Optional
import os


class SyntaxHighlighter:
    def __init__(self):
        self.lexer = TextLexer()
        self.enabled = True
        
    def set_file(self, filename: str) -> None:
        if not filename:
            self.lexer = TextLexer()
            return
        
        try:
            self.lexer = get_lexer_for_filename(filename)
        except:
            ext = os.path.splitext(filename)[1]
            if ext:
                try:
                    self.lexer = get_lexer_by_name(ext[1:])
                except:
                    self.lexer = TextLexer()
            else:
                self.lexer = TextLexer()
    
    def highlight_line(self, line: str) -> List[Tuple[str, str]]:
        if not self.enabled:
            return [('', line)]
        
        tokens = []
        for token_type, value in lex(line, self.lexer):
            color = self._token_to_color(token_type)
            tokens.append((color, value))
        
        return tokens
    
    def _token_to_color(self, token_type: Token) -> str:
        if token_type in Token.Keyword:
            return 'keyword'
        elif token_type in Token.Name.Function:
            return 'function'
        elif token_type in Token.Name.Class:
            return 'class'
        elif token_type in Token.String:
            return 'string'
        elif token_type in Token.Comment:
            return 'comment'
        elif token_type in Token.Number:
            return 'number'
        elif token_type in Token.Operator:
            return 'operator'
        elif token_type in Token.Name.Builtin:
            return 'builtin'
        elif token_type in Token.Name.Decorator:
            return 'decorator'
        else:
            return 'default'
    
    def toggle(self) -> None:
        self.enabled = not self.enabled
