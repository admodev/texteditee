from enum import Enum, auto


class Mode(Enum):
    NORMAL = auto()
    INSERT = auto()
    VISUAL = auto()
    VISUAL_LINE = auto()
    VISUAL_BLOCK = auto()
    COMMAND = auto()
    SEARCH = auto()
    REPLACE = auto()
    
    def __str__(self) -> str:
        return {
            Mode.NORMAL: 'NORMAL',
            Mode.INSERT: '-- EDIT --',
            Mode.VISUAL: '-- VISUAL --',
            Mode.VISUAL_LINE: '-- VISUAL LINE --',
            Mode.VISUAL_BLOCK: '-- VISUAL BLOCK --',
            Mode.COMMAND: 'COMMAND',
            Mode.SEARCH: 'SEARCH',
            Mode.REPLACE: '-- REPLACE --',
        }[self]


class ModeManager:
    def __init__(self):
        self._mode = Mode.NORMAL
        self._previous_mode = Mode.NORMAL
        
    @property
    def current(self) -> Mode:
        return self._mode
    
    @property
    def previous(self) -> Mode:
        return self._previous_mode
    
    def set_mode(self, mode: Mode) -> None:
        self._previous_mode = self._mode
        self._mode = mode
    
    def is_normal(self) -> bool:
        return self._mode == Mode.NORMAL
    
    def is_insert(self) -> bool:
        return self._mode == Mode.INSERT
    
    def is_visual(self) -> bool:
        return self._mode in (Mode.VISUAL, Mode.VISUAL_LINE, Mode.VISUAL_BLOCK)
    
    def is_command(self) -> bool:
        return self._mode == Mode.COMMAND
    
    def is_search(self) -> bool:
        return self._mode == Mode.SEARCH
    
    def to_normal(self) -> None:
        self.set_mode(Mode.NORMAL)
    
    def to_insert(self) -> None:
        self.set_mode(Mode.INSERT)
    
    def to_visual(self) -> None:
        self.set_mode(Mode.VISUAL)
    
    def to_visual_line(self) -> None:
        self.set_mode(Mode.VISUAL_LINE)
    
    def to_visual_block(self) -> None:
        self.set_mode(Mode.VISUAL_BLOCK)
    
    def to_command(self) -> None:
        self.set_mode(Mode.COMMAND)
    
    def to_search(self) -> None:
        self.set_mode(Mode.SEARCH)
    
    def to_replace(self) -> None:
        self.set_mode(Mode.REPLACE)
