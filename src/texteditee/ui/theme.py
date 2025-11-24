from dataclasses import dataclass
from typing import Dict


@dataclass
class ColorScheme:
    name: str
    background: str
    foreground: str
    cursor: str
    selection: str
    line_number: str
    status_bg: str
    status_fg: str
    keyword: str
    function: str
    class_name: str
    string: str
    comment: str
    number: str
    operator: str
    builtin: str
    decorator: str
    error: str
    warning: str


THEMES: Dict[str, ColorScheme] = {
    'default': ColorScheme(
        name='default',
        background='black',
        foreground='white',
        cursor='white',
        selection='blue',
        line_number='cyan',
        status_bg='blue',
        status_fg='white',
        keyword='yellow',
        function='green',
        class_name='cyan',
        string='magenta',
        comment='bright_black',
        number='red',
        operator='white',
        builtin='cyan',
        decorator='yellow',
        error='red',
        warning='yellow',
    ),
    'monokai': ColorScheme(
        name='monokai',
        background='#272822',
        foreground='#F8F8F2',
        cursor='#F8F8F0',
        selection='#49483E',
        line_number='#90908A',
        status_bg='#3E3D32',
        status_fg='#F8F8F2',
        keyword='#F92672',
        function='#A6E22E',
        class_name='#66D9EF',
        string='#E6DB74',
        comment='#75715E',
        number='#AE81FF',
        operator='#F92672',
        builtin='#66D9EF',
        decorator='#A6E22E',
        error='#F92672',
        warning='#E6DB74',
    ),
}


class ThemeManager:
    def __init__(self):
        self.current_theme = THEMES['default']
    
    def set_theme(self, name: str) -> bool:
        if name in THEMES:
            self.current_theme = THEMES[name]
            return True
        return False
    
    def get_color(self, element: str) -> str:
        return getattr(self.current_theme, element, self.current_theme.foreground)
    
    def list_themes(self) -> list[str]:
        return list(THEMES.keys())
