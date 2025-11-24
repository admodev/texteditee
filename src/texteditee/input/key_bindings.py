from typing import Callable, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class KeyBinding:
    key: str
    handler: Callable
    mode: str = 'normal'
    description: str = ''


class KeyBindingRegistry:
    def __init__(self):
        self.bindings: Dict[Tuple[str, str], KeyBinding] = {}
        self.pending_keys = ''
        self.count = ''
    
    def register(self, key: str, handler: Callable, mode: str = 'normal', 
                description: str = '') -> None:
        binding = KeyBinding(key, handler, mode, description)
        self.bindings[(mode, key)] = binding
    
    def get(self, key: str, mode: str) -> Optional[KeyBinding]:
        return self.bindings.get((mode, key))
    
    def handle_key(self, key: str, mode: str) -> Optional[Tuple[Callable, int]]:
        if key.isdigit() and mode == 'normal' and (self.count or key != '0'):
            self.count += key
            return None
        
        full_key = self.pending_keys + key
        
        binding = self.get(full_key, mode)
        if binding:
            count = int(self.count) if self.count else 1
            self.pending_keys = ''
            self.count = ''
            return (binding.handler, count)
        
        possible_matches = [k for m, k in self.bindings.keys() 
                          if m == mode and k.startswith(full_key)]
        
        if possible_matches:
            self.pending_keys = full_key
            return None
        
        self.pending_keys = ''
        self.count = ''
        return None
    
    def clear_pending(self) -> None:
        self.pending_keys = ''
        self.count = ''
    
    def get_pending_display(self) -> str:
        display = ''
        if self.count:
            display += self.count
        if self.pending_keys:
            display += self.pending_keys
        return display


def setup_default_bindings(registry: KeyBindingRegistry, editor: 'Editor') -> None:
    registry.register('h', lambda e, c: e.cursor.move_left(c), 'normal', 'Move left')
    registry.register('j', lambda e, c: e.cursor.move_down(c), 'normal', 'Move down')
    registry.register('k', lambda e, c: e.cursor.move_up(c), 'normal', 'Move up')
    registry.register('l', lambda e, c: e.cursor.move_right(c), 'normal', 'Move right')
    
    registry.register('w', lambda e, c: e.cursor.move_word_forward(c), 'normal', 'Word forward')
    registry.register('b', lambda e, c: e.cursor.move_word_backward(c), 'normal', 'Word backward')
    registry.register('e', lambda e, c: e.cursor.move_word_end(c), 'normal', 'Word end')
    
    registry.register('0', lambda e, c: e.cursor.move_to_line_start(), 'normal', 'Line start')
    registry.register('$', lambda e, c: e.cursor.move_to_line_end(), 'normal', 'Line end')
    registry.register('^', lambda e, c: e.cursor.move_to_first_non_blank(), 'normal', 'First non-blank')
    
    registry.register('gg', lambda e, c: e.cursor.move_to(0, 0), 'normal', 'First line')
    registry.register('G', lambda e, c: e.goto_line(e.buffer.line_count - 1 if c == 1 else c - 1), 
                     'normal', 'Last line / Go to line')
    
    registry.register('i', lambda e, c: e.enter_insert_mode(), 'normal', 'Insert before cursor')
    registry.register('a', lambda e, c: e.enter_insert_mode_after(), 'normal', 'Insert after cursor')
    registry.register('I', lambda e, c: e.insert_at_line_start(), 'normal', 'Insert at line start')
    registry.register('A', lambda e, c: e.insert_at_line_end(), 'normal', 'Insert at line end')
    registry.register('o', lambda e, c: e.open_line_below(), 'normal', 'Open line below')
    registry.register('O', lambda e, c: e.open_line_above(), 'normal', 'Open line above')
    
    registry.register('x', lambda e, c: e.delete_char(c), 'normal', 'Delete character')
    registry.register('dd', lambda e, c: e.delete_line(c), 'normal', 'Delete line')
    registry.register('D', lambda e, c: e.delete_to_line_end(), 'normal', 'Delete to line end')
    
    registry.register('yy', lambda e, c: e.yank_line(c), 'normal', 'Yank line')
    registry.register('p', lambda e, c: e.paste_after(c), 'normal', 'Paste after')
    registry.register('P', lambda e, c: e.paste_before(c), 'normal', 'Paste before')
    
    registry.register('u', lambda e, c: e.undo(), 'normal', 'Undo')
    registry.register('KEY_CTRL_R', lambda e, c: e.redo(), 'normal', 'Redo')
    
    registry.register('/', lambda e, c: e.start_search(), 'normal', 'Search forward')
    registry.register('?', lambda e, c: e.start_search_backward(), 'normal', 'Search backward')
    registry.register('n', lambda e, c: e.find_next(), 'normal', 'Next match')
    registry.register('N', lambda e, c: e.find_previous(), 'normal', 'Previous match')
    
    registry.register(':', lambda e, c: e.enter_command_mode(), 'normal', 'Command mode')
    
    registry.register('v', lambda e, c: e.enter_visual_mode(), 'normal', 'Visual mode')
    registry.register('V', lambda e, c: e.enter_visual_line_mode(), 'normal', 'Visual line mode')
    
    registry.register('KEY_ESCAPE', lambda e, c: e.exit_insert_mode(), 'insert', 'Exit insert mode')
    
    registry.register('KEY_CTRL_C', lambda e, c: e.interrupt(), 'normal', 'Interrupt')
    registry.register('KEY_CTRL_C', lambda e, c: e.interrupt(), 'insert', 'Interrupt')
