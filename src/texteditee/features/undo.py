from typing import Protocol, List
from dataclasses import dataclass


class Action(Protocol):
    def execute(self) -> None: ...
    def undo(self) -> None: ...


@dataclass
class InsertCharAction:
    buffer: 'Buffer'
    line: int
    col: int
    char: str
    
    def execute(self) -> None:
        self.buffer.insert_char(self.line, self.col, self.char)
    
    def undo(self) -> None:
        self.buffer.delete_char(self.line, self.col)


@dataclass
class DeleteCharAction:
    buffer: 'Buffer'
    line: int
    col: int
    deleted_char: str = ''
    
    def execute(self) -> None:
        self.deleted_char = self.buffer.delete_char(self.line, self.col)
    
    def undo(self) -> None:
        self.buffer.insert_char(self.line, self.col, self.deleted_char)


@dataclass
class InsertLineAction:
    buffer: 'Buffer'
    line: int
    text: str = ''
    
    def execute(self) -> None:
        self.buffer.insert_line(self.line, self.text)
    
    def undo(self) -> None:
        self.buffer.delete_line(self.line)


@dataclass
class DeleteLineAction:
    buffer: 'Buffer'
    line: int
    deleted_text: str = ''
    
    def execute(self) -> None:
        self.deleted_text = self.buffer.delete_line(self.line)
    
    def undo(self) -> None:
        self.buffer.insert_line(self.line, self.deleted_text)


@dataclass
class CompositeAction:
    actions: List[Action]
    
    def execute(self) -> None:
        for action in self.actions:
            action.execute()
    
    def undo(self) -> None:
        for action in reversed(self.actions):
            action.undo()


class UndoManager:
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self._undo_stack: List[Action] = []
        self._redo_stack: List[Action] = []
        self._current_group: List[Action] = []
        self._grouping = False
    
    def start_group(self) -> None:
        self._grouping = True
        self._current_group = []
    
    def end_group(self) -> None:
        if self._grouping and self._current_group:
            action = CompositeAction(self._current_group)
            self._undo_stack.append(action)
            self._redo_stack.clear()
            
            if len(self._undo_stack) > self.max_history:
                self._undo_stack.pop(0)
        
        self._grouping = False
        self._current_group = []
    
    def record(self, action: Action) -> None:
        if self._grouping:
            self._current_group.append(action)
        else:
            self._undo_stack.append(action)
            self._redo_stack.clear()
            
            if len(self._undo_stack) > self.max_history:
                self._undo_stack.pop(0)
    
    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        
        action = self._undo_stack.pop()
        action.undo()
        self._redo_stack.append(action)
        return True
    
    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        
        action = self._redo_stack.pop()
        action.execute()
        self._undo_stack.append(action)
        return True
    
    def can_undo(self) -> bool:
        return len(self._undo_stack) > 0
    
    def can_redo(self) -> bool:
        return len(self._redo_stack) > 0
    
    def clear(self) -> None:
        self._undo_stack.clear()
        self._redo_stack.clear()
        self._current_group.clear()
        self._grouping = False
