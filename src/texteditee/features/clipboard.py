import pyperclip
from typing import List


class Clipboard:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance
    
    def _init(self) -> None:
        self._internal_clipboard: List[str] = []
        self._use_system = True
    
    def copy(self, text: str | List[str]) -> None:
        if isinstance(text, str):
            self._internal_clipboard = [text]
        else:
            self._internal_clipboard = text.copy()
        
        if self._use_system:
            try:
                content = '\n'.join(self._internal_clipboard) if isinstance(self._internal_clipboard, list) else text
                pyperclip.copy(content)
            except:
                self._use_system = False
    
    def paste(self) -> List[str]:
        if self._use_system:
            try:
                content = pyperclip.paste()
                if content:
                    return content.split('\n')
            except:
                self._use_system = False
        
        return self._internal_clipboard.copy()
    
    def clear(self) -> None:
        self._internal_clipboard = []
        if self._use_system:
            try:
                pyperclip.copy('')
            except:
                pass
